import os
import requests
import time
from api_secrets import API_KEY_ASSEMBLYAI, API_KEY_LISTENNOTES

LISTENNOTES_EPISODE_ENDPOINT = 'https://listen-api.listennotes.com/api/v2/episodes'
ASSEMBLYAI_TRANSCRIPT_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'

def get_episode_details(episode_id):
    """Fetches metadata and audio URL from Listen Notes."""
    url = f"{LISTENNOTES_EPISODE_ENDPOINT}/{episode_id}"
    headers = {'X-ListenAPI-Key': API_KEY_LISTENNOTES}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Listen Notes API Error: {e}"

def get_full_transcript_data(audio_url):
    """Gets the full transcript object from AssemblyAI, including chapters and word timestamps."""
    headers = {'authorization': API_KEY_ASSEMBLYAI}
    try:
        post_response = requests.post(ASSEMBLYAI_TRANSCRIPT_ENDPOINT, json={'audio_url': audio_url, 'auto_chapters': True}, headers=headers)
        post_response.raise_for_status()
        transcript_id = post_response.json()['id']

        polling_url = f"{ASSEMBLYAI_TRANSCRIPT_ENDPOINT}/{transcript_id}"
        while True:
            get_response = requests.get(polling_url, headers=headers)
            get_response.raise_for_status()
            transcript_data = get_response.json()

            if transcript_data['status'] == 'completed':
                return transcript_data, None
            elif transcript_data['status'] == 'error':
                return None, f"AssemblyAI Transcription failed: {transcript_data.get('error')}"
            
            print("Transcription is still processing...")
            time.sleep(5)
    except requests.exceptions.RequestException as e:
        return None, f"AssemblyAI API Error: {e}"