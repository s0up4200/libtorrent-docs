# libtorrent-docs

Scraped mirror of [libtorrent.org](https://libtorrent.org) documentation and [blog](https://blog.libtorrent.org) stored as markdown, for LLM reference.

## Structure

- **`docs/`** — ~47 documentation pages
- **`blog/`** — ~31 blog posts (2011–2022)
- **`images/`** — locally downloaded images referenced by docs and blog

Each directory has an `index.md` listing all files.

## Claude Code skill

`skill/SKILL.md` is a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) that teaches Claude how to navigate this repo and answer libtorrent questions. To use it, update the docs path inside `SKILL.md` to point at your local clone.

The canonical version of this skill lives in [soup/skills](https://github.com/s0up4200/skills) — the copy here may lag behind.

## Updating

```bash
./update.sh
```

Requires [uv](https://github.com/astral-sh/uv). Re-scrapes everything, re-downloads images, and rebuilds indexes.

The scraper now fails hard on incomplete discovery or fetches and only swaps generated output into place after a fully successful run.

## Testing

```bash
uv run python -m unittest discover -s tests -v
```

`pyproject.toml` is the canonical dependency source for both scraping and tests.

## License

Original code and repo-authored metadata in this repository are licensed under MIT. See `LICENSE`.

Mirrored third-party content under `docs/`, `blog/`, and `images/` is not relicensed by this repository. `docs/` mirrors libtorrent.org material from Arvid Norberg and contributors, and `blog/` mirrors blog.libtorrent.org posts by Arvid Norberg unless otherwise noted upstream. Copyright and licensing for that material remain with the upstream authors and rights holders. See `NOTICE`.
