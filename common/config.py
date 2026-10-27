import os

# Do not provide a usable default. A deployment must supply a distinct secret.
A2A_API_KEY = os.getenv("A2A_API_KEY")
RESEARCH_URL = os.getenv("RESEARCH_URL", "http://127.0.0.1:8001")
WRITER_URL = os.getenv("WRITER_URL", "http://127.0.0.1:8002")
