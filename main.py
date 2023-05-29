import requests
import json

def test():
    url = 'http://localhost:8000/post-data'
    headers = {'Content-Type': 'multipart/form-data'}
    data = {
        'data': (None, json.dumps({
            'judul': 'morgan',
            'deskripsi': 'morgan eror',
            'harga': 0.5
        }), 'application/json'),
        'nft_file': open('morgan.jpg', 'rb')
    }

    response = requests.post(url, files=data, headers=headers)
    print(response.json())

if __name__ == "__main__":
    test()
