from fastapi import Header, HTTPException, Security

API_KEY = "42245ea4f72648928384ef8e0b482344"
API_KEY_NAME = "access_token"

def get_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key