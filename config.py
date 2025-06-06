import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
API_KEYS = {
    "IMAGE_GEN": os.getenv("IMAGE_GEN_API_KEY", ""),
    "INSTAGRAM": os.getenv("INSTAGRAM_API_KEY", ""),
}

# Search Configuration
SEARCH_CONFIG = {
    "SEARCH_TERM": "outrageous tales about Anal Cunt",
    "TIMEOUT": 10,
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Scheduling Configuration
SCHEDULE_CONFIG = {
    "POSTS_PER_DAY": 3,
    "POST_TIMES": ["10:00", "14:00", "18:00"],
    "VIDEO_COMPILATION_TIME": "23:50"
}

# File Paths
PATHS = {
    "TEMP_IMAGES": "./temp/images",
    "TEMP_TEXT": "./temp/text",
    "DAILY_VIDEO": "./output/daily_video",
    "LOGS": "./logs"
}

# Ensure directories exist
for path in PATHS.values():
    os.makedirs(path, exist_ok=True)
