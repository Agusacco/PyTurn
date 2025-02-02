import os.path
from datetime import datetime
from tkinter import messagebox
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/calendar"]
GOOGLE_CALENDAR_TOKEN = os.getenv('GOOGLE_CALENDAR_TOKEN')
GOOGLE_CALENDAR_CLIENT_SECRET = os.getenv('GOOGLE_CALENDAR_CLIENT_SECRET')

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

def access_calendar():
    creds = authenticate_google_calendar()
    try:
        service = build('calendar', 'v3', credentials=creds)
        # Lista algunos eventos próximos para probar la conexión
        events_result = service.events().list(calendarId='primary', maxResults=100).execute()
        events = events_result.get('items', [])
        return events

    except Exception as error:
        messagebox.showerror("Error", f"No se pudo acceder al calendario.\n{error}")
        return []
  
def authenticate_google_calendar():
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