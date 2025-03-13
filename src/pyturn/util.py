import os.path
import configparser
from datetime import datetime
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/calendar",
          "https://www.googleapis.com/auth/spreadsheets"]
GOOGLE_CALENDAR_TOKEN = os.getenv('GOOGLE_CALENDAR_TOKEN')
GOOGLE_CALENDAR_CLIENT_SECRET = os.getenv('GOOGLE_CALENDAR_CLIENT_SECRET')

config = configparser.ConfigParser()
config.read(".config")

def format_event_date(event_date_str):
    # Convertir la fecha de formato ISO 8601 al formato deseado: DD/MM/YYYY HH:MM
    try:
        event_date = datetime.fromisoformat(event_date_str.replace("Z", "+00:00"))
        formatted_date = event_date.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        # Si la fecha no tiene hora, es solo una fecha (día completo)
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        formatted_date = event_date.strftime("%d/%m/%Y")
    return formatted_date

def access_sheet(function, range):
    creds = authenticate_google_credentials()
    try:
        has_result = False
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        #Load the pacient list.
        if function == "access_pacients":
            result = sheet.values().get(spreadsheetId=(config.get("CONFIG", "GOOGLE_SHEET_ID")),
                                        range=range).execute()
            has_result = True

        #Delete row from the sheet. 
        elif function == "delete_row":
            #sheet.values().batchClear(spreadsheetId=(config.get("CONFIG", "GOOGLE_SHEET_ID")),
                                        #body={"ranges": [range]}).execute()
            sheet.batchUpdate(
                spreadsheetId=config.get("CONFIG", "GOOGLE_SHEET_ID"),
                body={
                    "requests": [
                        {
                            "deleteDimension": {
                                "range": {
                                    "sheetId": 0,  # ID de la hoja dentro del documento
                                    "dimension": "ROWS",
                                    "startIndex": range - 1,  # Google Sheets usa base 0
                                    "endIndex": range  # Elimina solo esa fila
                                }
                            }
                        }
                    ]
                }
            ).execute()
            
        if has_result == True:
            values = result.get('values', [])
            return values                   

    except Exception as error:
        messagebox.showerror("Error", f"No se pudo acceder a la hoja de cálculo.\n{error}")
        return []

def access_calendar():
    creds = authenticate_google_credentials()
    try:
        service = build('calendar', 'v3', credentials=creds)
        # Lista algunos eventos próximos para probar la conexión
        events_result = service.events().list(calendarId='primary', maxResults=100).execute()
        events = events_result.get('items', [])
        return events

    except Exception as error:
        messagebox.showerror("Error", f"No se pudo acceder al calendario.\n{error}")
        return []
  
def authenticate_google_credentials():
    creds = None
    # Verifica si ya existen credenciales
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(GOOGLE_CALENDAR_TOKEN)
    # Si no hay credenciales válidas, se inicia el flujo de autenticación
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CALENDAR_CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para usarlas en el futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds