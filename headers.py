from dotenv import load_dotenv
import os

load_dotenv()

AUTH_HEADERS = {
    "Authorization": f"Bearer {os.getenv('U_SCLID')}",
    "X-Session-ID": os.getenv("LO_UID"),
    "X-AF-Session": os.getenv("AF_SESSION"),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PocketBot/1.0",
    "X-Recaptcha-Token": os.getenv("G_RECAPTCHA")
}
