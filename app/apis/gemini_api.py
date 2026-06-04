from app.services.summarizer import get_default_summarizer


def get_summarization(arxiv_data):
    return get_default_summarizer().summarize(arxiv_data)
