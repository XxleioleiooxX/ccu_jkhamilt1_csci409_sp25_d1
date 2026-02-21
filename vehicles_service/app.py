from fastapi import FastAPI, Depends
from security import get_api_key
import httpx
import requests

app = FastAPI()

API_KEY = "42245ea4f72648928384ef8e0b482344"
ENDPOINT_URL = "https://api-v3.mbta.com/" # DO NOT CHANGE THIS

# Dependency to fetch all vehicles
async def get_all_vehicles(route: str = None, revenue: str = None):
    params = {"api_key": API_KEY}

    if route:
        params["filter[route]"] = route
    if revenue:
        params["filter[revenue]"] = revenue

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ENDPOINT_URL}/vehicles",
            params=params
        )
        response.raise_for_status()
        return response.json()

# Dependency to fetch a specific vehicle by ID
async def get_vehicle_by_id(vehicle_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ENDPOINT_URL}/vehicles/{vehicle_id}",
            params={"api_key": API_KEY}
        )
        response.raise_for_status()
        return response.json()

app = FastAPI() # Initialize the end point

@app.get("/vehicles")
async def read_vehicles(
    route: str = None,
    revenue: str = None,
    vehicles=Depends(get_all_vehicles)
):
    return vehicles

@app.get("/vehicles/{vehicle_id}")
async def read_vehicle(
    vehicle_id: str,
    vehicle=Depends(get_vehicle_by_id)
):
    return vehicle

@app.get("/vehicles")
def get_vehicles(api_key: str = Depends(get_api_key)):
    return {"vehicles": ["Bus 101", "Bus 102", "Bus 103"]}

@app.get("/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: int, api_key: str = Depends(get_api_key)):
    return {"vehicle_id": vehicle_id, "name": f"Vehicle {vehicle_id}"}