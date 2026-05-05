import requests
import json
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

'''
# from airflow.decorators import task
# from airflow.models import Variable
'''

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = os.getenv("CHANNEL_HANDLE")

'''
# API_KEY = Variable.get("API_KEY")
# CHANNEL_HANDLE = Variable.get("CHANNEL_HANDLE")
'''

maxResults = 50

#@task
def get_playlist_id():
    """
    Fetches the 'uploads' playlist ID for the YouTube channel specified by CHANNEL_HANDLE.
    
    Returns:
        str: The playlist ID containing the channel's uploaded videos.
    """
    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # print(json.dumps(data,indent=4))
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        raise e

#@task
def get_video_ids(playlistId):
    """
    Retrieves all video IDs from the specified YouTube playlist.
    
    Args:
        playlistId (str): The ID of the playlist to fetch videos from.
        
    Returns:
        list: A list of video IDs contained within the playlist.
    """
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    try:
        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            pageToken = data.get("nextPageToken")
            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e

#@task
def extract_video_data(video_ids):
    """
    Extracts detailed statistics and information for a list of YouTube video IDs.
    
    Args:
        video_ids (list): A list of YouTube video IDs to retrieve data for.
        
    Returns:
        list: A list of dictionaries, each containing statistics for a specific video.
    """
    extracted_data = []

    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id : video_id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                contentDetails = item["contentDetails"]
                statistics = item["statistics"]
                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "publishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount", None),
                    "likeCount": statistics.get("likeCount", None),
                    "commentCount": statistics.get("commentCount", None),
                }
                extracted_data.append(video_data)
        return extracted_data
    except requests.exceptions.RequestException as e:
        raise e

#@task
def save_to_json(extracted_data):
    """
    Saves the extracted YouTube video data into a JSON file with the current date.
    
    Args:
        extracted_data (list): The list of dictionaries containing video data to be saved.
    """
    file_path = f"./data/YT_data_{date.today()}.json"
    with open(file_path, "w", encoding="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)