from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx
import os
from dotenv import load_dotenv
from typing import Optional
import uvicorn

# Load environment variables
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('API_KEY')

# Verify API key is available
if not API_KEY:
    print("WARNING: API_KEY not found in environment variables. API calls will fail!")
else:
    print(f"API Key loaded: {API_KEY[:6]}...{API_KEY[-4:]}")

app = FastAPI(title="Hourglass API Proxy")

# Configure CORS - IMPORTANT: Make sure this is set up correctly
origins = [
    "http://localhost:5173",    # Your React app
    "http://localhost:3000",    # Common React port
    "http://127.0.0.1:5173",    # Alternative localhost
    "*"                         # Allow all origins (use with caution in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Be more specific for security
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Base URL for the Hourglass API - USING HTTPS!
BASE_URL = 'https://hourglass-qa.shieldfoundry.com'

# Headers for API requests
headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY  # Include the API key in the headers
}

# Create a reusable HTTP client
http_client = httpx.AsyncClient(
    base_url=BASE_URL,
    headers=headers,
    timeout=30.0,
    follow_redirects=True
)

@app.on_event("shutdown")
async def shutdown_event():
    await http_client.aclose()

# Custom exception handler to ensure CORS headers are included even when errors occur
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.get("/api/resources")
async def get_resources(
    activeOnly: Optional[bool] = Query(True, description="Filter for active resources only"),
    resourceType: Optional[str] = Query(None, description="Filter by resource type"),
    serviceOffering: Optional[str] = Query(None, description="Filter by service offering ID")
):
    """
    Proxy endpoint to fetch resources from Hourglass API
    """
    # Construct the query parameters
    params = {}
    if activeOnly is not None:
        params['activeOnly'] = str(activeOnly).lower()
    if resourceType:
        params['resourceType'] = resourceType
    if serviceOffering:
        params['serviceOffering'] = serviceOffering
    
    try:
        print(f"Making request to {BASE_URL}/api/resources with params: {params}")
        # Make request to the Hourglass API
        response = await http_client.get("/api/resources", params=params)
        response.raise_for_status()
        
        # Print response for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        # Return the data as JSON
        return response.json()
    
    except httpx.HTTPStatusError as e:
        # Handle HTTP errors (4xx, 5xx)
        status_code = e.response.status_code
        print(f"HTTP Error {status_code}: {e.response.text}")
        try:
            error_detail = e.response.json()
        except ValueError:
            error_detail = {"detail": e.response.text}
        
        raise HTTPException(status_code=status_code, detail=error_detail)
    
    except httpx.RequestError as e:
        # Handle request errors (connection, timeout, etc.)
        print(f"Request Error: {str(e)}")
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Route to verify API key is working
@app.get("/api/check-connection")
async def check_connection():
    """
    Test endpoint to verify API key and connection to Hourglass API
    """
    if not API_KEY:
        return {"status": "error", "message": "API key not configured"}
        
    try:
        # Make a simple request to test the connection
        response = await http_client.get("/api/resources")
        response.raise_for_status()
        return {
            "status": "success", 
            "message": "Connection to Hourglass API successful",
            "url": f"{BASE_URL}/api/resources"
        }
    except Exception as e:
        return {"status": "error", "message": f"Connection failed: {str(e)}"}

# Simple CORS test endpoint
@app.get("/test-cors")
async def test_cors():
    """
    Simple endpoint to test if CORS is working properly
    """
    return {"message": "CORS is working properly!"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)