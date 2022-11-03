import json
from flask import Flask, request
app = Flask(__name__)

'''
Sample Request body : 

"data":{
	"source":"138 Brittany Manor Drive, Amherst, MA",
	"destination": "Amherst Commons, Amherst, MA",
	"percentage_length":"30",
	"max_min":"min"
	
}

Sample response:

"response":{
    'Route' : route,
    'Distance':dist,
    'Elevation Gain':elevation
}
'''
@app.route("/fetch_route",methods=["POST"])
def fetch_route():
    try:
        data = request.json
    except Exception as e:
        print(f"Something went wrong in parsing data with error {e}")

    '''
    TODO: Call graph generator and get the generated graph
    TODO: Call Path Finder and get the optimal route satisfying all the conditions
    '''
    
    return data.get("data")
if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)