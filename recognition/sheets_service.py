import json
import gspread
from google.oauth2.service_account import Credentials
from config.settings import settings
from utils.logger import logger

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def _get_sheet():
    creds_json = json.loads(settings.google_service_account_json)
    creds = Credentials.from_service_account_info(creds_json, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(settings.google_sheets_id).sheet1