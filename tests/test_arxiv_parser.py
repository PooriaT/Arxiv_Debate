import unittest

from app.models.article import Article
from app.services.arxiv_parser import ArxivParseError, parse_arxiv_feed


ATOM_FEED_OPEN = '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">'
FEED_CLOSE = "</feed>"


def _feed(entry_xml: str = "") -> str:
    return f"{ATOM_FEED_OPEN}{entry_xml}{FEED_CLOSE}"


class ArxivParserTest(unittest.TestCase):
    def test_parse_valid_xml_with_one_article(self):
        articles = parse_arxiv_feed(
            _feed(
                """
                <entry>
                    <id>http://arxiv.org/abs/2501.00001v1</id>
                    <published>2025-01-01T00:00:00Z</published>
                    <title>Typed XML parsing</title>
                    <summary>A safer parser.</summary>
                    <author><name>Ada Lovelace</name></author>
                    <author><name>Grace Hopper</name></author>
                    <link title="pdf" href="http://arxiv.org/pdf/2501.00001v1" />
                    <arxiv:primary_category term="cs.SE" />
                </entry>
                """
            )
        )

        self.assertEqual(len(articles), 1)
        self.assertIsInstance(articles[0], Article)
        self.assertEqual(articles[0].id, "http://arxiv.org/abs/2501.00001v1")
        self.assertEqual(articles[0].title, "Typed XML parsing")
        self.assertEqual(articles[0].summary, "A safer parser.")
        self.assertEqual(articles[0].authors, ["Ada Lovelace", "Grace Hopper"])
        self.assertEqual(articles[0].published, "2025-01-01T00:00:00Z")
        self.assertEqual(articles[0].pdf_url, "http://arxiv.org/pdf/2501.00001v1")
        self.assertEqual(articles[0].category, "cs.SE")

    def test_parse_valid_xml_with_no_entries(self):
        self.assertEqual(parse_arxiv_feed(_feed()), [])

    def test_parse_malformed_xml_raises_app_specific_error(self):
        with self.assertRaisesRegex(ArxivParseError, "malformed"):
            parse_arxiv_feed("<feed><entry></feed>")

    def test_parse_empty_xml_raises_app_specific_error(self):
        with self.assertRaisesRegex(ArxivParseError, "empty"):
            parse_arxiv_feed("   ")

    def test_parse_article_missing_pdf_link(self):
        articles = parse_arxiv_feed(
            _feed(
                """
                <entry>
                    <id>http://arxiv.org/abs/2501.00001v1</id>
                    <title>Missing PDF</title>
                    <summary>No PDF link in this entry.</summary>
                </entry>
                """
            )
        )

        self.assertIsNone(articles[0].pdf_url)

    def test_parse_article_missing_primary_category(self):
        articles = parse_arxiv_feed(
            _feed(
                """
                <entry>
                    <id>http://arxiv.org/abs/2501.00001v1</id>
                    <title>Missing Category</title>
                    <summary>No primary category in this entry.</summary>
                    <link title="pdf" href="http://arxiv.org/pdf/2501.00001v1" />
                </entry>
                """
            )
        )

        self.assertIsNone(articles[0].category)

    def test_parse_article_missing_author_list(self):
        articles = parse_arxiv_feed(
            _feed(
                """
                <entry>
                    <id>http://arxiv.org/abs/2501.00001v1</id>
                    <title>Missing Authors</title>
                    <summary>No author list in this entry.</summary>
                </entry>
                """
            )
        )

        self.assertEqual(articles[0].authors, [])

    def test_parse_article_missing_summary(self):
        articles = parse_arxiv_feed(
            _feed(
                """
                <entry>
                    <id>http://arxiv.org/abs/2501.00001v1</id>
                    <title>Missing Summary</title>
                </entry>
                """
            )
        )

        self.assertEqual(articles[0].summary, "")


if __name__ == "__main__":
    unittest.main()
