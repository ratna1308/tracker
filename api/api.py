"""

127.0.0.1:8000/docs - swagger
127.0.0.1:8000/redoc
"""


from fastapi import FastAPI
from api.handlers import demo


def create_app():
    app = FastAPI(docs_url="/", redoc_url="/docs")
    app.include_router(demo.router)
    return app
