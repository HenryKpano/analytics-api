from fastapi import FastAPI
from app.routers import sales, users, revenue

# Initialize the FastAPI app
app = FastAPI(
    title="Analytics API",
    description="API for multiple analytics types (sales, users, revenue) from Redshift"
)

# Include routers for each analysis type
app.include_router(sales.router)
app.include_router(users.router)
app.include_router(revenue.router)