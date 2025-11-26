# main.py
# from fastapi import FastAPI
# import redis.asyncio as redis

# app = FastAPI()
# redis_client = redis.Redis(host="localhost", port=6379, db=0)

# @app.on_event("startup")
# async def startup_event():
#     try:
#         pong = await redis_client.ping()
#         print("Redis connected:", pong)   # Output: True
#     except Exception as e:
#         print("Redis error:", e)
