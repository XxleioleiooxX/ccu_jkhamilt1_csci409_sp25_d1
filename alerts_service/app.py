from fastapi import FastAPI, Depends
import httpx
import requests

app = FastAPI()

API_KEY = "42245ea4f72648928384ef8e0b482344"
ENDPOINT_URL = "https://api-v3.mbta.com/" # DO NOT CHANGE THIS

# Dependency to fetch all alerts
async def get_all_alerts(route: str = None, stop: str = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route
    if stop:
        params["filter[stop]"] = stop

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ENDPOINT_URL}/alerts",
            params=params
        )
        response.raise_for_status()
        return response.json()



# Dependency to fetch a specific alert by ID
async def get_alert_by_id(alert_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ENDPOINT_URL}/alerts/{alert_id}",
            params={"api_key": API_KEY}
        )
        response.raise_for_status()
        return response.json()

@app.get("/alerts")
async def read_alerts(
    route: str = None,
    stop: str = None,
    alerts=Depends(get_all_alerts)
):
    return alerts


@app.get("/alerts/{alert_id}")
async def read_alert(alert_id: str, alert=Depends(get_alert_by_id)):
    return alert