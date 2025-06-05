from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
import time
from app.core.config import settings
import redis
import json

# Use Redis for distributed rate limiting
try:
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=1,  # Use a separate DB for rate limiting
        decode_responses=True
    )
    redis_available = True
except Exception as e:
    print(f"Warning: Redis connection failed: {e}")
    redis_available = False
    # In-memory fallback
    rate_limit_data = {}

async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting for certain paths
    if request.url.path.startswith("/media") or request.url.path.startswith("/static"):
        return await call_next(request)
    
    # Get client IP
    client_ip = request.client.host
    
    # Create rate limit key
    endpoint = request.url.path
    rate_limit_key = f"rate_limit:{client_ip}:{endpoint}"
    
    current_time = int(time.time())
    window_start = current_time - settings.RATE_LIMIT_WINDOW
    
    if redis_available:
        try:
            # Use Redis sorted sets for rate limiting
            # Add current request timestamp
            redis_client.zadd(rate_limit_key, {str(current_time): current_time})
            
            # Remove timestamps outside current window
            redis_client.zremrangebyscore(rate_limit_key, 0, window_start)
            
            # Set expiry on the key
            redis_client.expire(rate_limit_key, settings.RATE_LIMIT_WINDOW * 2)
            
            # Count requests in current window
            request_count = redis_client.zcard(rate_limit_key)
            
        except Exception as e:
            print(f"Redis rate limiting error: {e}")
            # Fall back to allowing the request
            request_count = 0
    else:
        # In-memory fallback for rate limiting
        if rate_limit_key not in rate_limit_data:
            rate_limit_data[rate_limit_key] = []
        
        # Add current request timestamp
        rate_limit_data[rate_limit_key].append(current_time)
        
        # Filter timestamps to keep only those within the current window
        rate_limit_data[rate_limit_key] = [
            ts for ts in rate_limit_data[rate_limit_key] if ts > window_start
        ]
        
        request_count = len(rate_limit_data[rate_limit_key])
    
    # Check if rate limit exceeded
    if request_count > settings.RATE_LIMIT_REQUESTS:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": "Rate limit exceeded. Please try again later."
            }
        )
    
    # Process the request
    response = await call_next(request)
    
    # Add rate limit headers
    response.headers["X-Rate-Limit-Limit"] = str(settings.RATE_LIMIT_REQUESTS)
    response.headers["X-Rate-Limit-Remaining"] = str(settings.RATE_LIMIT_REQUESTS - request_count)
    response.headers["X-Rate-Limit-Reset"] = str(window_start + settings.RATE_LIMIT_WINDOW)
    
    return response
