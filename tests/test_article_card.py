import unittest

from app.components.article_card import (
    ABSTRACT_PREVIEW_LENGTH,
    _format_authors,
    _format_category,
    _format_published,
    _truncate_text,
    render_article_card,
    render_article_cards,
)
from app.models.article import Article


class ArticleCardTest(unittest.TestCase):
    def test_render_article_card_uses_article_fields(self):
        article = Article(
            id="http://arxiv.org/abs/2501.00001v1",
            title="Typed callback orchestration",
            summary="A focused refactor.",
            authors=["Ada Lovelace", "Grace Hopper"],
            published="2025-01-01T00:00:00Z",
            pdf_url="http://arxiv.org/pdf/2501.00001v1",
            category="cs.SE",
        )

        card = render_article_card(article)
        body = card.children[0]
        title = body.children[0]
        metadata = body.children[1]
        abstract = body.children[2]
        action_area = body.children[3]
        read_pdf_button = action_area.children[0]

        self.assertEqual(card.className, "article-card mb-3 shadow-sm")
        self.assertEqual(title.children, "Typed callback orchestration")
        self.assertEqual(metadata.children[0].children[1], "Ada Lovelace, Grace Hopper")
        self.assertEqual(metadata.children[1].children, "cs.SE")
        self.assertEqual(metadata.children[2].children[1], "2025-01-01")
        self.assertEqual(metadata.children[3].children[1], "2501.00001v1")
        self.assertEqual(abstract.children, "A focused refactor.")
        self.assertEqual(read_pdf_button.children[1], "Read PDF")
        self.assertEqual(read_pdf_button.href, "http://arxiv.org/pdf/2501.00001v1")
        self.assertEqual(read_pdf_button.target, "_blank")

    def test_render_article_card_uses_fallbacks(self):
        article = Article(
            id="http://arxiv.org/abs/2501.00001v1",
            title="Sparse paper",
            summary="",
            authors=[],
            published=None,
            pdf_url=None,
            category=None,
        )

        card = render_article_card(article)
        body = card.children[0]
        metadata = body.children[1]
        abstract = body.children[2]
        action_area = body.children[3]
        arxiv_button = action_area.children[0]

        self.assertEqual(metadata.children[0].children[1], "Unknown authors")
        self.assertEqual(metadata.children[1].children[1], "Unknown date")
        self.assertEqual(metadata.children[2].children[1], "2501.00001v1")
        self.assertEqual(abstract.children, "No abstract available.")
        self.assertEqual(arxiv_button.children[1], "View on arXiv")
        self.assertEqual(arxiv_button.href, "http://arxiv.org/abs/2501.00001v1")

    def test_render_article_card_omits_broken_action_when_links_missing(self):
        article = Article(
            id="",
            title="Unlinked paper",
            summary="Short abstract.",
            authors=[],
            published=None,
            pdf_url=None,
            category=None,
        )

        card = render_article_card(article)
        action_area = card.children[0].children[3]

        self.assertEqual(action_area.children[0].children, "No article link available")

    def test_render_article_card_truncates_long_summary(self):
        article = Article(
            id="2501.00001v1",
            title="Long paper",
            summary="x" * (ABSTRACT_PREVIEW_LENGTH + 25),
            authors=["Ada Lovelace"],
            published="2025-01-01T00:00:00Z",
            pdf_url=None,
            category="cs.SE",
        )

        card = render_article_card(article)
        abstract = card.children[0].children[2]

        self.assertEqual(len(abstract.children), ABSTRACT_PREVIEW_LENGTH + 1)
        self.assertTrue(abstract.children.endswith("…"))

    def test_formatting_helpers_handle_readability_cases(self):
        self.assertEqual(_format_authors([]), "Unknown authors")
        self.assertEqual(
            _format_authors(["Ada", "Grace", "Katherine", "Margaret"]),
            "Ada, Grace, Katherine, +1 more",
        )
        self.assertEqual(_format_published(None), "Unknown date")
        self.assertEqual(_format_published("2025-01-01T12:00:00Z"), "2025-01-01")
        self.assertEqual(_format_category(" cs.SE "), "cs.SE")
        self.assertIsNone(_format_category(""))
        self.assertEqual(
            _truncate_text("\nA   compact abstract.\n"), "A compact abstract."
        )

    def test_render_article_cards_renders_each_article(self):
        articles = [
            Article("1", "First", "Summary 1", [], None, None, None),
            Article("2", "Second", "Summary 2", [], None, None, None),
        ]

        cards = render_article_cards(articles)

        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0].children[0].children[0].children, "First")
        self.assertEqual(cards[1].children[0].children[0].children, "Second")


if __name__ == "__main__":
    unittest.main()
