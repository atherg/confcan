import requests
import json
import time
import numpy as np

# base_url = 'http://0.0.0.0:8080'
base_url = 'http://34.220.56.231:8080'
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

    data = {"board": np.random.randint(3, size=(6, 7)).tolist()}
#    print(data)

    check_board(data)
    

if __name__ == "__main__":
    main()