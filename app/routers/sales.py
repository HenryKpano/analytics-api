from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db_connection
from app.auth import verify_api_key
from datetime import datetime
import redis
import json
from os import getenv

# Create a router for sales-related endpoints
router = APIRouter(prefix="/api/v1/analytics/sales", tags=["sales"])

# Initialize Redis client for caching
redis_client = redis.Redis(host=getenv("REDIS_HOST", "redis"), port=6379, db=0)

@router.get("/")
async def get_sales(start: str, end: str, region: str = None, api_key: str = Depends(verify_api_key)):
    """
    Retrieve sales analytics by date range and optional region.
    Args:
        start: Start date (e.g., '2025-01')
        end: End date (e.g., '2025-05')
        region: Optional region filter (e.g., 'US')
    Returns:
        JSON with sales data and metadata
    """
    # Check cache first
    cache_key = f"sales:{start}:{end}:{region}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"status": "success", "data": {"sales": json.loads(cached)}, "meta": {"timestamp": datetime.now().isoformat()}}

    try:
        # Connect to Redshift
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query with optional region filter
        query = "SELECT month, region, total, orders FROM monthly_sales WHERE month >= %s AND month <= %s"
        params = [start, end]
        if region:
            query += " AND region = %s"
            params.append(region)
        query += " ORDER BY month"

        # Execute query and fetch results
        cursor.execute(query, params)
        results = cursor.fetchall()
        sales = [{"month": r[0], "region": r[1], "total": float(r[2]), "orders": int(r[3])} for r in results]

        # Cache results for 1 hour
        redis_client.setex(cache_key, 3600, json.dumps(sales))

        # Close database connection
        cursor.close()
        conn.close()

        # Return response
        return {"status": "success", "data": {"sales": sales}, "meta": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))