from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db_connection
from app.auth import verify_api_key
from datetime import datetime
import redis
import json
from os import getenv

# Create a router for revenue-related endpoints
router = APIRouter(prefix="/api/v1/analytics/revenue", tags=["revenue"])

# Initialize Redis client for caching
redis_client = redis.Redis(host=getenv("REDIS_HOST", "redis"), port=6379, db=0)

@router.get("/")
async def get_revenue(start: str, end: str, product: str = None, api_key: str = Depends(verify_api_key)):
    """
    Retrieve revenue analytics by date range and optional product.
    Args:
        start: Start date (e.g., '2025-01')
        end: End date (e.g., '2025-05')
        product: Optional product filter (e.g., 'WidgetA')
    Returns:
        JSON with revenue data and metadata
    """
    # Check cache first
    cache_key = f"revenue:{start}:{end}:{product}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"status": "success", "data": {"revenue": json.loads(cached)}, "meta": {"timestamp": datetime.now().isoformat()}}

    try:
        # Connect to Redshift
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query with optional product filter
        query = '''
                select
 	                to_char(Date_trunc('day', dt_txt::date),'YYYY-MM-DD') as month,
 	                city_country as product,
 	                sum(humidity ) as total_revenue
                from dev_bronze.ext_canada_weather
                where to_char(Date_trunc('day', dt_txt::date),'YYYY-MM-DD') >= %s
 		                and to_char(Date_trunc('day', dt_txt::date),'YYYY-MM-DD') <= %s
 		                and city_country = %s
                group by month, product 
                order by month
                '''
        params = [start, end, product]

        # Execute query and fetch results
        cursor.execute(query, params)
        results = cursor.fetchall()
        revenue = [{"month": r[0], "product": r[1], "total_revenue": float(r[2])} for r in results]

        # Cache results for 1 hour
        redis_client.setex(cache_key, 3600, json.dumps(revenue))

        # Close database connection
        cursor.close()
        conn.close()

        # Return response
        return {"status": "success", "data": {"revenue": revenue}, "meta": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))