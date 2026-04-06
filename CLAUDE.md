# libtorrent-docs

Scraped mirror of libtorrent.org documentation and blog, stored as markdown for Claude to read and reference.

## Structure

```
libtorrent-docs/
├── docs/           # libtorrent.org documentation (~46 pages)
│   └── index.md    # Auto-generated listing of all docs
├── blog/           # blog.libtorrent.org posts (~30 posts, 2011–2022)
│   └── index.md    # Auto-generated listing with dates
├── images/         # Locally downloaded images from docs and blog
├── scrape.py       # Scraper script (PEP 723 inline deps, run via uv)
└── update.sh       # Entry point: ./update.sh
```

## Updating

```bash
./update.sh
```

Re-scrapes everything. Images are re-downloaded. Indexes are rebuilt. Use `git diff` after to see what changed upstream.

## How to answer questions about libtorrent

1. Start with `docs/index.md` or `blog/index.md` to find relevant files
2. Read the specific doc or blog post
3. Images are local — read them directly when diagrams or graphs are referenced
4. Key files for common topics:
   - Settings/configuration: `docs/reference-Settings.md`
   - Performance tuning: `docs/tuning-ref.md`
   - API overview: `docs/reference.md` (index of all reference pages)
   - Getting started: `docs/tutorial-ref.md`, `docs/building.md`
   - BitTorrent v2: `blog/2020-09-bittorrent-v2.md`

## Scraper details

- `scrape.py` uses `beautifulsoup4` + `markdownify` + `requests`
- Dependencies are declared inline (PEP 723) — `uv run` handles everything
- Auto-discovers `reference-*.html` pages from the reference index
- Blog posts are found by paginating through the blog listing
- Internal `.html` links are rewritten to `.md`
- Remote image URLs are downloaded to `images/` and rewritten to relative paths
