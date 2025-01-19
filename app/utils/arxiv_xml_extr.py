import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from apis.arxiv_api import get_arxiv_data
import xml.etree.ElementTree as ET


def xml_to_dic():
    xml = get_arxiv_data("machine learning")
    root = ET.fromstring(xml)
    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
    data = []
    for entry in entries:
        id = entry.find("{http://www.w3.org/2005/Atom}id").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        authors = [
            author.find("{http://www.w3.org/2005/Atom}name").text
            for author in entry.findall("{http://www.w3.org/2005/Atom}author")
        ]
        link = entry.find("{http://www.w3.org/2005/Atom}link[@title='pdf']").attrib[
            "href"
        ]
        category = entry.find("{http://arxiv.org/schemas/atom}primary_category").attrib[
            "term"
        ]
        data.append(
            {
                "id": id,
                "published": published,
                "title": title,
                "summary": summary,
                "authors": authors,
                "link": link,
                "category": category,
            }
        )
    return data
