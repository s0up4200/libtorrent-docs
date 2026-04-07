# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "markdownify", "requests"]
# ///

"""Scrape libtorrent.org docs and blog into local markdown files."""

import hashlib
import json
import re
import shutil
import tempfile
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR / "docs"
BLOG_DIR = SCRIPT_DIR / "blog"
IMAGES_DIR = SCRIPT_DIR / "images"
BASE_URL = "https://libtorrent.org/"
BLOG_URL = "https://blog.libtorrent.org/"
MIN_REFERENCE_PAGES = 20
MIN_BLOG_POSTS = 20
MIN_DOC_PAGES = 40

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "libtorrent-docs-scraper/2.0"

# Seed list of known documentation pages
DOC_PAGES = [
    "building.html",
    "client_test.html",
    "contributing.html",
    "dht_extensions.html",
    "dht_sec.html",
    "dht_store.html",
    "examples.html",
    "extension_protocol.html",
    "features-ref.html",
    "fuzzing.html",
    "manual-ref.html",
    "projects.html",
    "python_binding.html",
    "reference.html",
    "security-audit.html",
    "streaming.html",
    "troubleshooting.html",
    "tuning-ref.html",
    "tutorial-ref.html",
    "udp_tracker_protocol.html",
    "upgrade_to_1.2-ref.html",
    "upgrade_to_2.0-ref.html",
    "utp.html",
]

# Track downloaded images to avoid re-downloading within a run
_downloaded_images: dict[str, str] = {}


class ScrapeError(RuntimeError):
    """Raised when scraping cannot produce a complete corpus."""


def fetch(url: str) -> str:
    """Fetch a URL with retry and politeness delay."""
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            time.sleep(0.5)
            return resp.text
        except requests.RequestException as err:
            last_error = err
            if attempt < 2:
                time.sleep(1)

    raise ScrapeError(f"failed to fetch {url}: {last_error}")


def fetch_binary(url: str) -> bytes:
    """Fetch binary content (images) with retry."""
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            time.sleep(0.3)
            return resp.content
        except requests.RequestException as err:
            last_error = err
            if attempt < 2:
                time.sleep(1)

    raise ScrapeError(f"failed to fetch image {url}: {last_error}")


def frontmatter(**fields: str) -> str:
    """Build YAML frontmatter block."""
    lines = ["---"]
    for key, val in fields.items():
        if val:
            lines.append(f"{key}: {json.dumps(val, ensure_ascii=False)}")
    lines.append("---\n\n")
    return "\n".join(lines)


def download_image(
    url: str,
    images_dir: Path,
    downloaded_images: dict[str, str] | None = None,
) -> str:
    """Download an image and return its local path relative to repo root."""
    cache = _downloaded_images if downloaded_images is None else downloaded_images
    if url in cache:
        return cache[url]

    parsed = urlparse(url)
    ext = Path(parsed.path).suffix or ".png"
    path_parts = [part for part in parsed.path.strip("/").split("/") if part]
    name = Path(path_parts[-1]).stem if path_parts else "image"
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    filename = f"{name}-{url_hash}{ext}"

    outpath = images_dir / filename
    outpath.write_bytes(fetch_binary(url))

    local_path = f"images/{filename}"
    cache[url] = local_path
    return local_path


def localize_images(
    content: str,
    nested_dir: bool,
    images_dir: Path,
    downloaded_images: dict[str, str] | None = None,
) -> str:
    """Find image URLs in markdown, download them, rewrite to local paths."""

    def replace_image(match: re.Match[str]) -> str:
        alt = match.group(1)
        url = match.group(2)
        if not url.startswith("http"):
            return match.group(0)
        local_path = download_image(url, images_dir, downloaded_images)
        rel = f"../{local_path}" if nested_dir else local_path
        return f"![{alt}]({rel})"

    content = re.sub(
        r"!\[([^\]]*)\]\((https?://[^\s)]+)(?:\s+\"[^\"]*\")?\)",
        replace_image,
        content,
    )
    content = re.sub(
        r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(https?://[^)]+\)",
        r"![\1](\2)",
        content,
    )
    return content


def clean_markdown(content: str) -> str:
    """Strip known navigation/report noise from generated markdown."""
    content = re.sub(r"^\[home\]\(reference\.md\)\n+", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\[\[report issue\]\([^)]+\)\]\n+", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\[\]\n+", "", content, flags=re.MULTILINE)
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()


def discover_reference_pages() -> tuple[list[str], dict[str, str]]:
    """Fetch reference.html and extract all reference-*.html links plus section titles."""
    html = fetch(urljoin(BASE_URL, "reference.html"))
    soup = BeautifulSoup(html, "html.parser")

    pages: set[str] = set()
    titles: dict[str, str] = {}

    for rubric in soup.select("p.rubric"):
        section_title = rubric.get_text(" ", strip=True)
        block = rubric.find_next_sibling()
        if not block:
            continue
        for link in block.select("a[href]"):
            href = link["href"].split("#")[0]
            if href.startswith("reference-") and href.endswith(".html"):
                pages.add(href)
                titles.setdefault(href, section_title)

    if len(pages) < MIN_REFERENCE_PAGES:
        raise ScrapeError(
            f"reference discovery incomplete: expected at least {MIN_REFERENCE_PAGES}, got {len(pages)}"
        )

    return sorted(pages), titles


def discover_blog_posts() -> list[str]:
    """Paginate through blog listing pages, collect all post URLs."""
    urls = set()
    page = 1

    while True:
        url = BLOG_URL if page == 1 else f"{BLOG_URL}page/{page}/"
        html = fetch(url)
        soup = BeautifulSoup(html, "html.parser")

        found = False
        for link in soup.find_all("a", href=True):
            href = link["href"].split("#")[0]
            if re.match(r"https?://blog\.libtorrent\.org/\d{4}/\d{2}/[\w-]+", href):
                urls.add(href.rstrip("/") + "/")
                found = True

        if not found:
            break

        next_link = soup.find("a", href=re.compile(rf"/page/{page + 1}/"))
        if not next_link:
            break
        page += 1

    if len(urls) < MIN_BLOG_POSTS:
        raise ScrapeError(
            f"blog discovery incomplete: expected at least {MIN_BLOG_POSTS}, got {len(urls)}"
        )

    return sorted(urls)


def rewrite_links(text: str) -> str:
    """Rewrite internal .html links to .md."""
    return re.sub(
        r"\]\(([a-zA-Z0-9_][a-zA-Z0-9_.-]*)\.html(#[^)]*)?\)",
        r"](\1.md\2)",
        text,
    )


def derive_doc_title(
    page: str,
    main: BeautifulSoup,
    reference_titles: dict[str, str] | None = None,
) -> str:
    """Pick a stable page title for docs."""
    if reference_titles and page in reference_titles:
        return reference_titles[page]

    title_el = main.select_one("h1")
    if title_el:
        return title_el.get_text(" ", strip=True)

    slug = page.removesuffix(".html")
    if slug.startswith("reference-"):
        slug = slug.removeprefix("reference-").replace("_", " ")
    return slug


def scrape_doc(
    page: str,
    reference_titles: dict[str, str] | None = None,
    images_dir: Path | None = None,
    downloaded_images: dict[str, str] | None = None,
) -> tuple[str, str]:
    """Extract content from a libtorrent.org doc page."""
    url = urljoin(BASE_URL, page)
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    main = soup.select_one("div#main") or soup.select_one("div.document") or soup.body
    if not main:
        raise ScrapeError(f"missing main content for {url}")

    for selector in ["table.docinfo", "div.contents", "div#footer"]:
        for element in main.select(selector):
            element.decompose()

    for element in main.find_all("div", style=re.compile(r"position\s*:\s*absolute")):
        element.decompose()

    for paragraph in main.select("p"):
        text = paragraph.get_text(" ", strip=True)
        hrefs = {link.get("href") for link in paragraph.select("a[href]")}
        if text == "home" and "reference.html" in hrefs:
            paragraph.decompose()

    for link in main.select('a[href*="github.com/arvidn/libtorrent/issues/new"]'):
        parent = link.parent
        if parent and parent.get_text(" ", strip=True) == "report issue":
            parent.decompose()
        else:
            link.decompose()

    title = derive_doc_title(page, main, reference_titles)
    output_images_dir = IMAGES_DIR if images_dir is None else images_dir

    content = md(str(main), heading_style="ATX", code_language="cpp")
    content = rewrite_links(content)
    content = localize_images(content, True, output_images_dir, downloaded_images)
    content = clean_markdown(content)

    return title, frontmatter(title=title, source=url) + content + "\n"


def scrape_blog_post(
    url: str,
    images_dir: Path | None = None,
    downloaded_images: dict[str, str] | None = None,
) -> tuple[str, str, str]:
    """Extract content from a blog.libtorrent.org post."""
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    post = (
        soup.select_one("article")
        or soup.select_one("div.post")
        or soup.select_one("div.blog-post")
        or soup.select_one("div.entry-content")
    )

    title_el = (
        soup.select_one("h1.entry-title")
        or soup.select_one("h1.page-header")
        or soup.select_one("h1")
    )
    title = title_el.get_text(" ", strip=True) if title_el else "Untitled"

    date_match = re.search(r"/(\d{4})/(\d{2})/", url)
    date = f"{date_match.group(1)}-{date_match.group(2)}" if date_match else ""

    if not post:
        post = soup.select_one("main") or soup.select_one("div#content") or soup.body
        if not post:
            raise ScrapeError(f"missing post content for {url}")

    for selector in [
        "nav",
        "footer",
        "div.sidebar",
        "div.blog-sidebar-right",
        "div.col-sm-3",
        "div.comments",
        "div#comments",
        "div.reply",
        "p.blog-post-meta",
    ]:
        for element in post.select(selector):
            element.decompose()

    for selector in ["div#respond", "div.comment-respond"]:
        for element in post.select(selector):
            element.decompose()

    for paragraph in post.select("p"):
        text = paragraph.get_text(" ", strip=True)
        if text.startswith("Posted in "):
            paragraph.decompose()

    for element in post.select("h1"):
        element.decompose()

    output_images_dir = IMAGES_DIR if images_dir is None else images_dir

    content = md(str(post), heading_style="ATX")
    content = localize_images(content, True, output_images_dir, downloaded_images)
    content = clean_markdown(content)

    return title, date, frontmatter(title=title, date=date, source=url) + content + "\n"


def slug_from_blog_url(url: str) -> str:
    """Extract a filename slug from a blog post URL."""
    match = re.search(r"/(\d{4})/(\d{2})/([\w-]+)/?$", url)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    return re.sub(r"[^\w-]", "-", url.split("//")[1]).strip("-")


def build_index(
    directory: Path,
    title: str,
    index_path: Path,
    sort_mode: str = "title",
) -> None:
    """Build an index.md listing all markdown files in a directory."""
    entries = []

    for file_path in directory.glob("*.md"):
        if file_path.name == "index.md":
            continue

        text = file_path.read_text(encoding="utf-8")
        title_match = re.search(r'^title:\s*"(.+?)"', text, re.MULTILINE)
        date_match = re.search(r'^date:\s*"(.+?)"', text, re.MULTILINE)

        display = title_match.group(1) if title_match else file_path.stem
        date = date_match.group(1) if date_match else ""
        prefix = f"({date}) " if date else ""

        entries.append(
            {
                "display": display,
                "date": date,
                "filename": file_path.name,
                "line": f"- [{prefix}{display}]({file_path.name})",
            }
        )

    if sort_mode == "date_desc":
        entries.sort(key=lambda item: item["display"].casefold())
        entries.sort(key=lambda item: item["date"], reverse=True)
    else:
        entries.sort(key=lambda item: item["display"].casefold())

    content = f"# {title}\n\n" + "\n".join(item["line"] for item in entries) + "\n"
    index_path.write_text(content, encoding="utf-8")


def replace_output_dir(source: Path, destination: Path) -> None:
    """Replace a generated output directory only after a successful scrape."""
    backup = destination.with_name(f".{destination.name}.bak")

    if backup.exists():
        shutil.rmtree(backup)
    if destination.exists():
        destination.rename(backup)

    source.rename(destination)

    if backup.exists():
        shutil.rmtree(backup)


def main(output_root: Path | None = None) -> None:
    """Run a full scrape into temporary output directories, then swap on success."""
    root = SCRIPT_DIR if output_root is None else Path(output_root)
    docs_dir = root / "docs"
    blog_dir = root / "blog"
    images_dir = root / "images"

    _downloaded_images.clear()

    print("Discovering documentation pages...")
    ref_pages, reference_titles = discover_reference_pages()
    all_doc_pages = sorted(set(DOC_PAGES + ref_pages))
    if len(all_doc_pages) < MIN_DOC_PAGES:
        raise ScrapeError(
            f"doc discovery incomplete: expected at least {MIN_DOC_PAGES}, got {len(all_doc_pages)}"
        )
    print(f"  Found {len(all_doc_pages)} doc pages ({len(ref_pages)} reference pages)")

    print("Discovering blog posts...")
    blog_posts = discover_blog_posts()
    print(f"  Found {len(blog_posts)} blog posts")

    with tempfile.TemporaryDirectory(dir=root) as tempdir:
        temp_root = Path(tempdir)
        temp_docs = temp_root / "docs"
        temp_blog = temp_root / "blog"
        temp_images = temp_root / "images"

        for directory in [temp_docs, temp_blog, temp_images]:
            directory.mkdir(parents=True)

        print("Scraping documentation...")
        doc_count = 0
        for page in all_doc_pages:
            title, content = scrape_doc(
                page,
                reference_titles=reference_titles,
                images_dir=temp_images,
                downloaded_images=_downloaded_images,
            )
            slug = page.removesuffix(".html")
            outfile = temp_docs / f"{slug}.md"
            outfile.write_text(content, encoding="utf-8")
            doc_count += 1
            print(f"  {slug}.md")

        if doc_count != len(all_doc_pages):
            raise ScrapeError(
                f"doc scrape incomplete: expected {len(all_doc_pages)}, wrote {doc_count}"
            )

        print("Scraping blog posts...")
        blog_count = 0
        for url in blog_posts:
            title, date, content = scrape_blog_post(
                url,
                images_dir=temp_images,
                downloaded_images=_downloaded_images,
            )
            slug = slug_from_blog_url(url)
            outfile = temp_blog / f"{slug}.md"
            outfile.write_text(content, encoding="utf-8")
            blog_count += 1
            print(f"  {slug}.md")

        if blog_count != len(blog_posts):
            raise ScrapeError(
                f"blog scrape incomplete: expected {len(blog_posts)}, wrote {blog_count}"
            )

        print("Building indexes...")
        build_index(
            temp_docs,
            "libtorrent Documentation",
            temp_docs / "index.md",
            sort_mode="title",
        )
        build_index(
            temp_blog,
            "libtorrent Blog",
            temp_blog / "index.md",
            sort_mode="date_desc",
        )

        replace_output_dir(temp_docs, docs_dir)
        replace_output_dir(temp_blog, blog_dir)
        replace_output_dir(temp_images, images_dir)

    img_count = len(list(images_dir.glob("*")))
    print(
        f"\nDone. Wrote {doc_count} docs + {blog_count} blog posts"
        f" + {img_count} images."
    )


if __name__ == "__main__":
    main()
