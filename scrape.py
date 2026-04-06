# /// script
# requires-python = ">=3.10"
# dependencies = ["beautifulsoup4", "markdownify", "requests"]
# ///

"""Scrape libtorrent.org docs and blog into local markdown files."""

import hashlib
import re
import shutil
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

SESSION = requests.Session()
SESSION.headers["User-Agent"] = "libtorrent-docs-scraper/1.0"

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


def fetch(url: str) -> str:
    """Fetch a URL with retry and politeness delay."""
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            time.sleep(0.5)
            return resp.text
        except requests.RequestException as e:
            if attempt == 2:
                print(f"  SKIP {url}: {e}")
                return ""
            time.sleep(1)
    return ""


def fetch_binary(url: str) -> bytes | None:
    """Fetch binary content (images) with retry."""
    for attempt in range(3):
        try:
            resp = SESSION.get(url, timeout=30)
            resp.raise_for_status()
            time.sleep(0.3)
            return resp.content
        except requests.RequestException as e:
            if attempt == 2:
                print(f"  SKIP image {url}: {e}")
                return None
            time.sleep(1)
    return None


def download_image(url: str) -> str | None:
    """Download an image and return its local path relative to repo root."""
    if url in _downloaded_images:
        return _downloaded_images[url]

    # Derive a stable filename from the URL
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix or ".png"
    # Use URL path to create a readable filename, with hash suffix for uniqueness
    path_parts = [p for p in parsed.path.strip("/").split("/") if p]
    if path_parts:
        name = path_parts[-1]
        # Strip extension, clean up
        name = Path(name).stem
    else:
        name = "image"
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    filename = f"{name}-{url_hash}{ext}"

    data = fetch_binary(url)
    if not data:
        return None

    outpath = IMAGES_DIR / filename
    outpath.write_bytes(data)
    local_path = f"images/{filename}"
    _downloaded_images[url] = local_path
    return local_path


def localize_images(content: str, from_dir: str) -> str:
    """Find image URLs in markdown, download them, rewrite to local paths."""

    def replace_image(m: re.Match) -> str:
        alt = m.group(1)
        url = m.group(2)
        # Skip non-http images (already local)
        if not url.startswith("http"):
            return m.group(0)
        local_path = download_image(url)
        if local_path:
            # Compute relative path from the markdown file's directory
            rel = f"../{local_path}" if from_dir else local_path
            return f"![{alt}]({rel})"
        return m.group(0)

    # Match ![alt](url) and ![alt](url "title") patterns
    content = re.sub(
        r"!\[([^\]]*)\]\((https?://[^\s)]+)(?:\s+\"[^\"]*\")?\)",
        replace_image,
        content,
    )
    # Unwrap linked images: [![alt](local-img)](remote-url) → ![alt](local-img)
    content = re.sub(
        r"\[!\[([^\]]*)\]\(([^)]+)\)\]\(https?://[^)]+\)",
        r"![\1](\2)",
        content,
    )
    return content


def discover_reference_pages() -> list[str]:
    """Fetch reference.html and extract all reference-*.html links."""
    html = fetch(urljoin(BASE_URL, "reference.html"))
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    pages = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].split("#")[0]
        if href.startswith("reference-") and href.endswith(".html"):
            pages.add(href)
    return sorted(pages)


def discover_blog_posts() -> list[str]:
    """Paginate through blog listing pages, collect all post URLs."""
    urls = set()
    page = 1
    while True:
        url = BLOG_URL if page == 1 else f"{BLOG_URL}page/{page}/"
        html = fetch(url)
        if not html:
            break
        soup = BeautifulSoup(html, "html.parser")
        found = False
        for a in soup.find_all("a", href=True):
            href = a["href"].split("#")[0]  # Strip fragments (#respond, #comments)
            if re.match(r"https?://blog\.libtorrent\.org/\d{4}/\d{2}/[\w-]+", href):
                urls.add(href.rstrip("/") + "/")
                found = True
        if not found:
            break
        # Check for next page
        next_link = soup.find("a", href=re.compile(rf"/page/{page + 1}/"))
        if not next_link:
            break
        page += 1
    return sorted(urls)


def rewrite_links(text: str) -> str:
    """Rewrite internal .html links to .md."""
    return re.sub(
        r"\]\(([a-zA-Z0-9_][a-zA-Z0-9_.-]*)\.html(#[^)]*)?\)",
        r"](\1.md\2)",
        text,
    )


def frontmatter(**fields: str) -> str:
    """Build YAML frontmatter block."""
    lines = ["---"]
    for key, val in fields.items():
        if val:
            lines.append(f'{key}: "{val}"')
    lines.append("---\n\n")
    return "\n".join(lines)


def scrape_doc(page: str) -> tuple[str, str] | None:
    """Extract content from a libtorrent.org doc page."""
    url = urljoin(BASE_URL, page)
    html = fetch(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Find main content — try div#main first, fall back to document body
    main = soup.select_one("div#main") or soup.select_one("div.document") or soup.body
    if not main:
        return None

    # Remove noise elements
    for selector in ["table.docinfo", "div.contents", "div#footer"]:
        for el in main.select(selector):
            el.decompose()

    # Remove absolute-positioned ad divs
    for el in main.find_all("div", style=re.compile(r"position\s*:\s*absolute")):
        el.decompose()

    # Extract title
    title_el = main.select_one("h1")
    title = title_el.get_text(strip=True) if title_el else page.removesuffix(".html")

    # Convert to markdown
    content = md(str(main), heading_style="ATX", code_language="cpp")
    content = rewrite_links(content)
    content = localize_images(content, "docs")

    # Clean up excessive blank lines
    content = re.sub(r"\n{3,}", "\n\n", content).strip()

    return title, frontmatter(title=title, source=url) + content + "\n"


def scrape_blog_post(url: str) -> tuple[str, str, str] | None:
    """Extract content from a blog.libtorrent.org post."""
    html = fetch(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Find the post content
    post = (
        soup.select_one("article")
        or soup.select_one("div.post")
        or soup.select_one("div.blog-post")
        or soup.select_one("div.entry-content")
    )

    # Extract title
    title_el = (
        soup.select_one("h1.entry-title")
        or soup.select_one("h1.page-header")
        or soup.select_one("h1")
    )
    title = title_el.get_text(strip=True) if title_el else "Untitled"

    # Extract date from URL pattern /YYYY/MM/
    date_match = re.search(r"/(\d{4})/(\d{2})/", url)
    date = f"{date_match.group(1)}-{date_match.group(2)}" if date_match else ""

    if not post:
        # Fall back to main content area
        post = soup.select_one("main") or soup.select_one("div#content") or soup.body
        if not post:
            return None

    # Remove navigation, sidebar, footer elements
    for selector in [
        "nav",
        "footer",
        "div.sidebar",
        "div.blog-sidebar-right",
        "div.col-sm-3",
        "div.comments",
        "div#comments",
        "div.reply",
    ]:
        for el in post.select(selector):
            el.decompose()

    # Remove the title element from content (we add it via frontmatter)
    for el in post.select("h1"):
        el.decompose()

    # Convert to markdown
    content = md(str(post), heading_style="ATX")
    content = localize_images(content, "blog")
    content = re.sub(r"\n{3,}", "\n\n", content).strip()

    return title, date, frontmatter(title=title, date=date, source=url) + content + "\n"


def slug_from_blog_url(url: str) -> str:
    """Extract a filename slug from a blog post URL."""
    # URL pattern: /YYYY/MM/post-slug/
    m = re.search(r"/(\d{4})/(\d{2})/([\w-]+)/?$", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return re.sub(r"[^\w-]", "-", url.split("//")[1]).strip("-")


def build_index(
    directory: Path,
    title: str,
    index_path: Path,
) -> None:
    """Build an index.md listing all markdown files in a directory."""
    entries = []
    for f in sorted(directory.glob("*.md")):
        if f.name == "index.md":
            continue
        # Read frontmatter to get title and date
        text = f.read_text()
        fm_title = ""
        fm_date = ""
        fm_match = re.search(r'^title:\s*"(.+?)"', text, re.MULTILINE)
        if fm_match:
            fm_title = fm_match.group(1)
        date_match = re.search(r'^date:\s*"(.+?)"', text, re.MULTILINE)
        if date_match:
            fm_date = date_match.group(1)
        display = fm_title or f.stem
        prefix = f"({fm_date}) " if fm_date else ""
        entries.append(f"- [{prefix}{display}]({f.name})")

    content = f"# {title}\n\n" + "\n".join(entries) + "\n"
    index_path.write_text(content)


def main():
    # Phase 1: Discover all URLs
    print("Discovering documentation pages...")
    ref_pages = discover_reference_pages()
    all_doc_pages = sorted(set(DOC_PAGES + ref_pages))
    print(f"  Found {len(all_doc_pages)} doc pages ({len(ref_pages)} reference pages)")

    print("Discovering blog posts...")
    blog_posts = discover_blog_posts()
    print(f"  Found {len(blog_posts)} blog posts")

    # Phase 2: Clean output directories
    for d in [DOCS_DIR, BLOG_DIR, IMAGES_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)

    # Phase 3: Scrape and write docs
    print("Scraping documentation...")
    doc_count = 0
    for page in all_doc_pages:
        result = scrape_doc(page)
        if result:
            title, content = result
            slug = page.removesuffix(".html")
            outfile = DOCS_DIR / f"{slug}.md"
            outfile.write_text(content)
            doc_count += 1
            print(f"  {slug}.md")

    # Phase 4: Scrape and write blog posts
    print("Scraping blog posts...")
    blog_count = 0
    for url in blog_posts:
        result = scrape_blog_post(url)
        if result:
            title, date, content = result
            slug = slug_from_blog_url(url)
            outfile = BLOG_DIR / f"{slug}.md"
            outfile.write_text(content)
            blog_count += 1
            print(f"  {slug}.md")

    # Phase 5: Build indexes
    print("Building indexes...")
    build_index(DOCS_DIR, "libtorrent Documentation", DOCS_DIR / "index.md")
    build_index(BLOG_DIR, "libtorrent Blog", BLOG_DIR / "index.md")

    img_count = len(list(IMAGES_DIR.glob("*")))
    print(
        f"\nDone. Wrote {doc_count} docs + {blog_count} blog posts"
        f" + {img_count} images."
    )


if __name__ == "__main__":
    main()
