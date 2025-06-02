from fastapi import APIRouter, Depends, HTTPException
from app.db import get_db_connection
from app.auth import verify_api_key
from datetime import datetime
import redis
import json
from os import getenv

# Create a router for user-related endpoints
router = APIRouter(prefix="/api/v1/analytics/users", tags=["users"])

# Initialize Redis client for caching
redis_client = redis.Redis(host=getenv("REDIS_HOST", "redis"), port=6379, db=0)

@router.get("/active")
async def get_active_users(start: str, end: str, api_key: str = Depends(verify_api_key)):
    """
    Retrieve daily active users analytics by date range.
    Args:
        start: Start date (e.g., '2025-01-01')
        end: End date (e.g., '2025-05-31')
    Returns:
        JSON with active users data and metadata
    """
    # Check cache first
    cache_key = f"users:active:{start}:{end}"
    cached = redis_client.get(cache_key)
    if cached:
        return {"status": "success", "data": {"active_users": json.loads(cached)}, "meta": {"timestamp": datetime.now().isoformat()}}

    try:
        # Connect to Redshift
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query daily active users
        query = "SELECT date, active_users FROM daily_active_users WHERE date >= %s AND date <= %s ORDER BY date"
        cursor.execute(query, (start, end))
        results = cursor.fetchall()
        users = [{"date": str(r[0]), "active_users": int(r[1])} for r in results]

        # Cache results for 1 hour
        redis_client.setex(cache_key, 3600, json.dumps(users))

        # Close database connection
        cursor.close()
        conn.close()

        # Return response
        return {"status": "success", "data": {"active_users": users}, "meta": {"timestamp": datetime.now().isoformat()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))