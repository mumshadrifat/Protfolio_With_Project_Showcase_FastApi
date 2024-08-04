from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import logging

from helper.sqlConnector import fetch_sales_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize MongoDB client (add database and collection as needed)
con = MongoClient()
db = con['your_database']  # Replace 'your_database' with your actual database name
collection = db['your_collection']  # Replace 'your_collection' with your actual collection name

# Initialize Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define SalesData model
class SalesData(BaseModel):
    product: str
    product_name: str
    quantity_sold: str
    price: str
    vat_rate: str
    vat_amount: str
    line_amount: str

    @classmethod
    def from_dict(cls, obj: dict) -> 'SalesData':
        return cls(**obj)


# Route for the home page
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Route for the registration page
@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")


# Route for the report page
@app.get("/report", response_class=HTMLResponse)
async def read_report(request: Request):
    return templates.TemplateResponse(request=request, name="report.html")


@app.get("/dashboard", response_class=HTMLResponse)
async def read_report(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html")


@app.get("/api/sales-data", response_model=List[SalesData])
async def get_sales_data():
    try:
        sales_data_dicts = fetch_sales_data()
        sales_data = [SalesData.from_dict(data_dict) for data_dict in sales_data_dicts]
        return sales_data
    except Exception as e:
        logger.error("Error fetching sales data: %s", e)
        return []
