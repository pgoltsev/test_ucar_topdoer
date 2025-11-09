import logging

from fastapi import FastAPI

from test_ucar.api import incident

logger: logging.Logger = logging.getLogger(__name__)

app: FastAPI = FastAPI()

app.include_router(incident.routes.router, prefix='/api/v1')
