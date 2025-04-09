# config.py
"""Configuration settings and environment variables."""
import os

from dotenv import load_dotenv
import os

load_dotenv()  # This loads environment variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key!")

# Model configurations
CLASSIFIER_MODEL = "gpt-3.5-turbo"
AGENT_MODEL = "gpt-3.5-turbo"
VISION_MODEL = "OpenVINO/Phi-3.5-vision-instruct-int4-ov"

# System prompts
AGENT_SYSTEM_PROMPT = """
You are a food delivery support agent. Follow these critical rules:
1. NEVER provide specific delivery times, ETAs, or dates unless you have access to that data.
2. When asked about order arrival or ETA, acknowledge you need to check the system and indicate you'll use the ETA tool.
3. DO NOT make up information about delivery times - refer to tools instead.
4. For complaints or specific order information, indicate you need to check the appropriate systems.
5. Your primary role is to route customer inquiries to the appropriate tools, not to provide specific order information directly.
"""

# Constants
DEBUG = True  # Enable/disable debug logging