import logging
from pathlib import Path
import uuid


from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from app.config import Settings
from app import __version__
import os

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

Base.metadata.create_all(bind=engine)

# provide function for getting a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_app(config: Settings):
    app = FastAPI(
        title="Nirvana coalasce",
        description="",
        version=__version__,
        openapi_url=None
    )
    # remove sqllite db file on shutdown
    @app.on_event("shutdown")
    def release_lock():
        os.remove('./test.db')
    origins = ["*"]

    # on startup preload the DB with data
    from app.models.external import Api1, Api2, Api3
    @app.on_event("startup")
    def release_lock():
        # Populate the databases, should probably be in migration scripts
        api1_1 = Api1(memberid = 1, oop_max=10000, remaining_oop_max=9000, copay=1000)
        api1_2 = Api2(memberid = 1, oop_max=20000, remaining_oop_max=9000, copay=50000)
        api1_3 = Api3(memberid = 1, oop_max=10000, remaining_oop_max=8000, copay=1000)
        api2_1 = Api1(memberid = 2, oop_max=80000, remaining_oop_max=7000, copay=9000)
        api2_2 = Api2(memberid = 2, oop_max=80000, remaining_oop_max=6000, copay=5000)
        api2_3 = Api3(memberid = 2, oop_max=10000, remaining_oop_max=2000, copay=3000)
        api3_1 = Api1(memberid = 3, oop_max=10000, remaining_oop_max=9000, copay=1000)
        api3_2 = Api2(memberid = 3, oop_max=10000, remaining_oop_max=9000, copay=2000)
        api3_3 = Api3(memberid = 3, oop_max=10000, remaining_oop_max=9000, copay=3000)
        db = SessionLocal()
        db.add_all([api1_1, api1_2, api1_3, api2_1, api2_2, api2_3, api3_1, api3_2, api3_3])
        db.commit()

    origins = ["*"]
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    from app.config import APP_SETTINGS
    from app.api import external_apis
    from app.api import coalesce

    # add api endpoints to webserver
    app.include_router(external_apis.router)
    app.include_router(coalesce.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    # # All uncaught errors
    # @app.exception_handler(Exception)
    # async def error_response_handler(request: Request, exc: Exception):
    #     logger.error(exc)
    #     content = dict(code=500, message="Internal Server Error",
    #                    traceId=request.state.trace_id)
    #     logger.info(content)
    #     return JSONResponse(
    #         status_code=500,
    #         content=content
    #     )

    return app


    