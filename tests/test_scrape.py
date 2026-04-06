import unittest
from unittest.mock import patch

import scrape


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


if __name__ == "__main__":
    unittest.main()
