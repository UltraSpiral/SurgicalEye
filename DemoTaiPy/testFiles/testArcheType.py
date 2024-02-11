import requests
import json
from requests_toolbelt import MultipartEncoder
import os
from typing import Dict
from typing import List
import pprint


def get_file_type(filename: str) -> str:
    if filename.lower().endswith('.png'):
        return 'image/png'
    if filename.lower().endswith('.jpg') or filename.endswith('.jpeg'):
        return 'image/jpeg'
    if filename.lower().endswith('.mp4'):
        return 'video/mp4'


def post_files(filename: str, api_key: str) -> Dict:
    url = 'https://api.archetypeai.dev/v0.3/files'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    with open(filename, 'rb') as file_handle:
        encoder = MultipartEncoder({'file': (os.path.basename(filename), file_handle.read(), get_file_type(filename))})
        response = requests.post(url, data=encoder, headers={**auth_headers, 'Content-Type': encoder.content_type})
        response_data = response.json() if response.status_code == 200 else {}
        return response.status_code, response_data

def summarize(query: str, file_ids: List[str], api_key: str):
    url = 'https://api.archetypeai.dev/v0.3/summarize'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data

def describe(query: str, file_ids: List[str], api_key: str):
    url = 'https://api.archetypeai.dev/v0.3/describe'
    auth_headers = {"Authorization": f'Bearer {api_key}'}
    data_payload = {'query': query, 'file_ids': file_ids}
    response = requests.post(url, data=json.dumps(data_payload), headers=auth_headers)
    response_data = response.json() if response.status_code == 200 else {}
    return response.status_code, response_data



def main():
    # post_status_code, post_response_data = post_files("/Users/lucaszhang/Downloads/Surgical-Dataset/Images/All/images/bisturi1.jpg", 'gt51b6ea')
    post_status_code, post_response_data = post_files("exVid.mp4", 'gt51b6ea')
    print("post_status_code: " + str(post_status_code))
    print("post_response_data: " + str(post_response_data))

    #sum_status_code, sum_response_data = summarize("Describe the image", [post_response_data['file_id']], 'gt51b6ea')
    sum_status_code, sum_response_data = describe("Describe the image", [post_response_data['file_id']], 'gt51b6ea')
    print("sum_status_code: " + str(sum_status_code))
    print("sum_response_data: " + str(sum_response_data))

    
    print(sum_response_data)
    print(len(sum_response_data['results']))
    


    if 'results' in sum_response_data:
        for i in sum_response_data['results']:
            print('n/')
            try:
                pprint(i['description'])
            except KeyError as e:
                print('No description found')

            print('n/')
    else:
        print('No results found')

if __name__ == "__main__":
    main()


