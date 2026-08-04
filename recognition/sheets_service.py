import json
import gspread
from google.oauth2.service_account import Credentials
from config.settings import settings
from utils.logger import logger

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]