import unittest

from app.components.article_card import render_article_card, render_article_cards
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
        link = body.children[0].children[0]
        authors = body.children[1].children[0]
        published = body.children[1].children[1]
        summary = body.children[2]

        self.assertEqual(card.className, "mb-3 shadow-sm")
        self.assertEqual(link.children, "Typed callback orchestration")
        self.assertEqual(link.href, "http://arxiv.org/pdf/2501.00001v1")
        self.assertEqual(link.target, "_blank")
        self.assertEqual(authors.children[1], "Authors: Ada Lovelace, Grace Hopper")
        self.assertEqual(published.children[1], "Published: 2025-01-01")
        self.assertEqual(summary.children[1], "Summary: A focused refactor.")

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
        link = body.children[0].children[0]
        authors = body.children[1].children[0]
        published = body.children[1].children[1]
        summary = body.children[2]

        self.assertEqual(link.href, "http://arxiv.org/abs/2501.00001v1")
        self.assertEqual(authors.children[1], "Authors: Unknown")
        self.assertEqual(published.children[1], "Published: Unknown")
        self.assertEqual(summary.children[1], "Summary: No summary available")

    def test_render_article_cards_renders_each_article(self):
        articles = [
            Article("1", "First", "Summary 1", [], None, None, None),
            Article("2", "Second", "Summary 2", [], None, None, None),
        ]

        cards = render_article_cards(articles)

        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0].children[0].children[0].children[0].children, "First")
        self.assertEqual(
            cards[1].children[0].children[0].children[0].children, "Second"
        )


if __name__ == "__main__":
    unittest.main()
