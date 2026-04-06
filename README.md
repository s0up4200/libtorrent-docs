# libtorrent-docs

Scraped mirror of [libtorrent.org](https://libtorrent.org) documentation and [blog](https://blog.libtorrent.org) stored as markdown, for LLM reference.

## Structure

- **`docs/`** — ~47 documentation pages
- **`blog/`** — ~31 blog posts (2011–2022)
- **`images/`** — locally downloaded images referenced by docs and blog

Each directory has an `index.md` listing all files.

## Updating

```bash
./update.sh
```

Requires [uv](https://github.com/astral-sh/uv). Re-scrapes everything, re-downloads images, and rebuilds indexes.

## License

Original code and repo-authored metadata in this repository are licensed under MIT. See `LICENSE`.

Mirrored third-party content under `docs/`, `blog/`, and `images/` is not relicensed by this repository. Copyright and licensing for that material remain with the upstream authors and rights holders. See `NOTICE`.
