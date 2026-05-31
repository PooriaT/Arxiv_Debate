import os

import dotenv

dotenv.load_dotenv()

GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-3.5-flash")
