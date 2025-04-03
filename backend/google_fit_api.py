from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
SERVICE_ACCOUNT_FILE = 'your-service-account.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('fitness', 'v1', credentials=credentials)

def fetch_health_data():
    dataset_id = "start_time_ns-end_time_ns"
    data = service.users().dataSources().datasets().get(
        userId="me",
        dataSourceId="derived:com.google.heart_rate.bpm:com.google.android.gms:merge_heart_rate_bpm",
        datasetId=dataset_id
    ).execute()
    return json.dumps(data)