import unittest

import dash_bootstrap_components as dbc

import app.__main__  # noqa: F401
from app.pages.home import layout


def _find_by_id(component, component_id: str):
    if getattr(component, "id", None) == component_id:
        return component

    children = getattr(component, "children", None)
    if children is None:
        return None

    if not isinstance(children, list):
        children = [children]

    for child in children:
        found = _find_by_id(child, component_id)
        if found is not None:
            return found

    return None


def _find_label_for(component, input_id: str):
    if (
        isinstance(component, dbc.Label)
        and getattr(component, "html_for", None) == input_id
    ):
        return component

    children = getattr(component, "children", None)
    if children is None:
        return None

    if not isinstance(children, list):
        children = [children]

    for child in children:
        found = _find_label_for(child, input_id)
        if found is not None:
            return found

    return None


def _flatten_text(component) -> str:
    if component is None:
        return ""

    if isinstance(component, str):
        return component

    children = getattr(component, "children", None)
    if children is None:
        return ""

    if not isinstance(children, list):
        children = [children]

    return "".join(_flatten_text(child) for child in children)


class HomePageTest(unittest.TestCase):
    def test_form_inputs_preserve_accessible_descriptions(self):
        search_input = _find_by_id(layout, "input")
        max_results_input = _find_by_id(layout, "max-results")
        search_label = _find_label_for(layout, "input")
        max_results_label = _find_label_for(layout, "max-results")

        self.assertIsInstance(search_input, dbc.Input)
        self.assertIsInstance(max_results_input, dbc.Input)
        self.assertIn(
            "Good searches are specific research areas", _flatten_text(search_label)
        )
        self.assertIn("Fetch 5 to 50 papers", _flatten_text(max_results_label))


if __name__ == "__main__":
    unittest.main()
