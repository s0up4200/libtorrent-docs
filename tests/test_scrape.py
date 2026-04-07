import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import scrape


class FrontmatterTests(unittest.TestCase):
    def test_frontmatter_escapes_quotes(self) -> None:
        content = scrape.frontmatter(title='A "quoted" title', source="https://example.com")

        self.assertIn('title: "A \\"quoted\\" title"', content)


class ScrapeDocTests(unittest.TestCase):
    def test_reference_doc_uses_reference_title_and_omits_noise(self) -> None:
        html = """
        <html>
          <body>
            <div id="main">
              <p><a href="reference.html">home</a></p>
              <p>
                <a href="http://github.com/arvidn/libtorrent/issues/new?title=docs">
                  report issue
                </a>
              </p>
              <h1>dht_routing_bucket</h1>
              <p>Main content.</p>
            </div>
          </body>
        </html>
        """

        with patch("scrape.fetch", return_value=html):
            title, content = scrape.scrape_doc(
                "reference-Alerts.html",
                {"reference-Alerts.html": "Alerts"},
            )

        self.assertEqual(title, "Alerts")
        self.assertIn("Main content.", content)
        self.assertNotIn("[home]", content)
        self.assertNotIn("[]", content)
        self.assertNotIn("report issue", content)


class ScrapeBlogPostTests(unittest.TestCase):
    def test_scrape_blog_post_omits_reply_prompt(self) -> None:
        html = """
        <html>
          <body>
            <article>
              <h1 class="entry-title">BitTorrent v2</h1>
              <p>Main post content.</p>
              <p><span class="glyphicon glyphicon-folder-open"></span> Posted in protocol</p>
              <hr>
              <div id="respond" class="comment-respond">
                <h3 id="reply-title" class="comment-reply-title">
                  Leave a Reply
                  <small>
                    <a
                      rel="nofollow"
                      id="cancel-comment-reply-link"
                      href="/2020/09/bittorrent-v2/#respond"
                    >
                      Cancel reply
                    </a>
                  </small>
                </h3>
                <p class="must-log-in">
                  You must be
                  <a href="https://blog.libtorrent.org/wp-login.php">logged in</a>
                  to post a comment.
                </p>
              </div>
            </article>
          </body>
        </html>
        """

        with patch("scrape.fetch", return_value=html):
            result = scrape.scrape_blog_post(
                "https://blog.libtorrent.org/2020/09/bittorrent-v2/"
            )

        self.assertIsNotNone(result)
        _, _, content = result
        self.assertIn("Main post content.", content)
        self.assertNotIn("Leave a Reply", content)
        self.assertNotIn("Cancel reply", content)
        self.assertNotIn("You must be", content)
        self.assertNotIn("Posted in protocol", content)


class BuildIndexTests(unittest.TestCase):
    def test_build_index_sorts_docs_by_title(self) -> None:
        with TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            directory = tmp / "docs"
            directory.mkdir()
            (directory / "z.md").write_text('---\ntitle: "Zulu"\n---\n')
            (directory / "a.md").write_text('---\ntitle: "Alpha"\n---\n')

            scrape.build_index(
                directory,
                "libtorrent Documentation",
                directory / "index.md",
                sort_mode="title",
            )

            lines = (directory / "index.md").read_text().splitlines()
            self.assertEqual(lines[2], "- [Alpha](a.md)")
            self.assertEqual(lines[3], "- [Zulu](z.md)")

    def test_build_index_sorts_blog_by_newest_first(self) -> None:
        with TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            directory = tmp / "blog"
            directory.mkdir()
            (directory / "old.md").write_text(
                '---\ntitle: "Older"\ndate: "2011-11"\n---\n'
            )
            (directory / "new.md").write_text(
                '---\ntitle: "Newer"\ndate: "2022-06"\n---\n'
            )

            scrape.build_index(
                directory,
                "libtorrent Blog",
                directory / "index.md",
                sort_mode="date_desc",
            )

            lines = (directory / "index.md").read_text().splitlines()
            self.assertEqual(lines[2], "- [(2022-06) Newer](new.md)")
            self.assertEqual(lines[3], "- [(2011-11) Older](old.md)")


class MainTests(unittest.TestCase):
    def test_main_preserves_existing_output_when_scrape_fails(self) -> None:
        with TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            for name in ("docs", "blog", "images"):
                directory = root / name
                directory.mkdir()
                (directory / "sentinel.txt").write_text(f"old {name}")

            with (
                patch("builtins.print"),
                patch.object(scrape, "MIN_REFERENCE_PAGES", 1),
                patch.object(scrape, "MIN_BLOG_POSTS", 1),
                patch.object(
                    scrape,
                    "discover_reference_pages",
                    return_value=(["reference-Alerts.html"], {"reference-Alerts.html": "Alerts"}),
                ),
                patch.object(
                    scrape,
                    "discover_blog_posts",
                    return_value=["https://blog.libtorrent.org/2020/09/bittorrent-v2/"],
                ),
                patch.object(scrape, "scrape_doc", side_effect=RuntimeError("boom")),
            ):
                with self.assertRaises(RuntimeError):
                    scrape.main(output_root=root)

            self.assertEqual((root / "docs" / "sentinel.txt").read_text(), "old docs")
            self.assertEqual((root / "blog" / "sentinel.txt").read_text(), "old blog")
            self.assertEqual((root / "images" / "sentinel.txt").read_text(), "old images")


if __name__ == "__main__":
    unittest.main()
