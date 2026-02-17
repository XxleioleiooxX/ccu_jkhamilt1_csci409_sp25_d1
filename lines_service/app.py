from fastapi import FastAPI, Depends
import httpx
import requests

app = FastAPI()

API_KEY = "42245ea4f72648928384ef8e0b482344"
ENDPOINT_URL = "https://api-v3.mbta.com/" # DO NOT CHANGE THIS

# Get a list of all lines
@app.get("/lines")
def get_lines():
    lines_list = []

    response = requests.get(ENDPOINT_URL + f"/lines?api_key={API_KEY}")
    lines = response.json()["data"]

    for line in lines:
        lines_list.append({
            "id": line["id"],
            "text_color": line["attributes"]["text_color"],
            "short_name": line["attributes"]["short_name"],
            "long_name": line["attributes"]["long_name"],
            "color": line["attributes"]["color"]
        })

    return {"lines": lines_list}

# Get information on a specific line
@app.get("/lines/{line_id}")
def get_line(line_id: str):
    response = requests.get(ENDPOINT_URL + f"/lines/{line_id}?api_key={API_KEY}")
    json_response = response.json()

    # If MBTA returns an error
    if "data" not in json_response:
        return {
            "error": "Line not found",
            "line_id": line_id
        }

    line_data = json_response["data"]

    line = {
        "id": line_data["id"],
        "text_color": line_data["attributes"]["text_color"],
        "short_name": line_data["attributes"]["short_name"],
        "long_name": line_data["attributes"]["long_name"],
        "color": line_data["attributes"]["color"]
    }

    return {"line": line}