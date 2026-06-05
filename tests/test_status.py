import unittest

import dash_bootstrap_components as dbc

from app.components.status import (
    render_arxiv_error,
    render_initial_state,
    render_invalid_max_results,
    render_loading_state,
    render_no_results_state,
    render_parser_error,
    render_summary_error,
    render_unexpected_error,
)


class StatusComponentTest(unittest.TestCase):
    def test_initial_state_is_card_with_guidance(self):
        component = render_initial_state()

        self.assertIsInstance(component, dbc.Card)
        body = component.children.children
        self.assertEqual(body[0].children[1].children, "Ready when you are")
        self.assertIn("Enter a research topic", body[1].children)

    def test_loading_state_is_friendly_alert(self):
        component = render_loading_state()

        self.assertIsInstance(component, dbc.Alert)
        self.assertEqual(component.color, "info")
        self.assertIn("Searching arXiv", component.children[0].children[1].children)

    def test_no_results_mentions_query(self):
        component = render_no_results_state("narrow topic")

        body = component.children.children
        self.assertEqual(body[0].children[1].children, "No matching papers found")
        self.assertIn("narrow topic", body[1].children)

    def test_error_states_use_helpful_alerts(self):
        components = [
            render_arxiv_error("Could not retrieve arXiv articles: timeout"),
            render_parser_error("Could not parse arXiv articles: malformed"),
            render_summary_error("AI summary unavailable: Gemini failed"),
            render_invalid_max_results(),
            render_unexpected_error(),
        ]

        for component in components:
            self.assertIsInstance(component, dbc.Alert)
            self.assertTrue(component.children[2].children)


if __name__ == "__main__":
    unittest.main()
