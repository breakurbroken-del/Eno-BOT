import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# BOT
# ==========================
TOKEN = os.getenv("TOKEN")

# ==========================
# SETTINGS
# ==========================
MAX_WARNINGS = 20
TIMEZONE = "Asia/Kolkata"

# ==========================
# PROTECTED ROLES
# Add IDs here later
# ==========================
PROTECTED_ROLE_IDS = [
    # 123456789012345678,
    # 987654321098765432
]

# ==========================
# TIMEOUT LADDER
# Seconds
# ==========================
TIMEOUTS = {
    1: 0,
    2: 60,
    3: 300,
    4: 1800,
    5: 7200,
    6: 21600,
    7: 43200
}

# Warning 8-19 = 12 Hours
DEFAULT_TIMEOUT = 43200

# Warning 20 = Kick
KICK_AT = 20

# ==========================
# STATUS
# ==========================
STATUS_UPDATE_INTERVAL = 300

# ==========================
# DATABASE
# ==========================
DATABASE = "data/warnings.db"
