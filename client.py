import requests
import json
import time

base_url = 'http://0.0.0.0:8080'
HEADERS = {
    'user-agent': ('mazahacka'),
}

def check_board(data):
    endpoint = '/evaluate_board_state'
    params = 'data'
    url = f'{base_url}{endpoint}?{params}='+json.dumps(data)
    resp = requests.post(url, headers=HEADERS)
    if resp.status_code == 200:
        print(resp.text)
    else:
        print('something went wrong. return code: ', resp.status_code, resp)


def main():


    data = {
            "board": [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0],
            [0, 2, 2, 2, 1, 1, 0],
            [0, 1, 1, 1, 1, 2, 0],        
            ]
        }


    check_board(data)
    

if __name__ == "__main__":
    main()