# import sys
import os

# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import google.generativeai as genai
import dotenv

from setup import environment

dotenv.load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel(model_name=environment.GEMINI_MODEL_NAME)


def get_summarization(arxiv_data):
    prompt = f"""
    Below you can find a series of articles from arXiv for a specific topic.
    Checkout the provided abstracts and give me an insightful summary of the latest 
    developments in that field.

    {arxiv_data}

    Don't add the first sentence of yourself something like this:
    Okay, here's a summary of ...
    """
    response = model.generate_content(prompt)
    return response.text
