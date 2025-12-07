import requests
import os
import base64

def call_transcription_service(service_url, audio_file_path):
    """
    Calls the external transcription web service by sending a local audio file.

    Args:
        service_url (str): The URL of the deployed transcription function/webservice.
        audio_file_path (str): The local path to the audio file to be sent.
    """
    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at '{audio_file_path}'")
        return

    print(f"Attempting to connect to service at: {service_url}")
    print(f"Sending file: {audio_file_path}")

    # The server-side function expects the file data under the key 'audio' 
    # in the 'request.files' dictionary, which means we must send it as 
    # multipart/form-data with the key 'audio'.
    try:
        #gs_uri = "gs://dwh-rawdata/sample_audio.wav"
        gs_uri = "gs://customer_survey_audio/interview1_Kemper_Associate VP IT_CTS.wav"
        payload = {"gsuri":gs_uri} 
        response = requests.post(service_url, json=payload)

        # The service returns JSON, which we can parse and print
        data = response.json()
            
        print("\n--- Service Response ---")
        if 'text' in data:
            print(f"Transcription Successful:")
            print(data['text'])
        elif 'error' in data:
            print(f"Service Error:")
            print(data['error'])
        else:
            print("Unknown response format received.")
            print("------------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"\nError communicating with the service: {e}")
        # If the server returned a non-200 status code, print the content if available
        if response is not None:
             print(f"Server returned status code {response.status_code}")
             try:
                 print(f"Server response body: {response.text}")
             except:
                 pass
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    # --- Configuration ---
    
    # 1. *** IMPORTANT ***: Replace this with the actual URL of your deployed Cloud Function.
    SERVICE_URL = "https://speech2txtservice-821904618661.us-east1.run.app/transcribe_audio"
    
    # 2. Specify the path to the audio file you want to transcribe.
    #    Make sure this audio file exists and is in a compatible format (e.g., .webm).
    AUDIO_FILE_PATH = "sample_audio.wav" 
    
    # 3. Installation required: pip install requests

    # --- Execution ---
    #if SERVICE_URL.startswith("https://speech2txtservice"):
    #    print("Please update the SERVICE_URL variable with your actual deployed function URL.")
    #else:
    call_transcription_service(SERVICE_URL, AUDIO_FILE_PATH)
