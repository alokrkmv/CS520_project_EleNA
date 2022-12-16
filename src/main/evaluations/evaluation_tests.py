import requests
import time

HOST = "0.0.0.0"
PORT = "8000"
server_url = "http://" + HOST + ":" + PORT
min_response_times = [] 
max_response_times = [] 

_source = "115 Brittany Manor Drive, Amherst, MA, USA"
_percentage_length = "125"
destinations = ["162 Brittany Manor Drive, Amherst, MA, USA", 
"Amherst Golf Club, South Pleasant Street, Amherst, MA, USA", 
"Amherst Post Office, Amherst, MA, USA",
"Mahar Auditorium, Presidents Drive, Amherst, MA, USA",
"Worcester Commons, North Pleasant Street, Amherst, MA, USA",
"Immanuel Lutheran Church, North Pleasant Street, Amherst, MA, USA" ]


_max_min = "min"
for _destination in destinations:
    request_json = {'data': {'source': _source , 'destination': _destination, 'percentage_length': _percentage_length, 'max_min': _max_min}}
    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/fetch_route', json= request_json)
    post_time_end = time.time()
    server_json = server_response.json()
    if not "message" in server_json:
        min_response_times.append({server_json["distance"]: post_time_end - post_time_start})

_max_min = "max"
for _destination in destinations:
    request_json = {'data': {'source': _source , 'destination': _destination, 'percentage_length': _percentage_length, 'max_min': _max_min}}
    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/fetch_route', json= request_json)
    post_time_end = time.time()
    server_json = server_response.json()

    if not "message" in server_json:
        max_response_times.append({server_json["distance"], post_time_end - post_time_start})

print(f"min_reesponse_time:{min_response_times}")
print(f"max_response_time:{max_response_times}")