# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


#############
# APP SETUP #
#############

app = FastAPI()

# Serve static files from the 'static' directory
BASE_DIR = os.path.dirname(__file__)
static_dir = os.path.join(BASE_DIR, '..', 'static')
index_path = os.path.join(static_dir, "index.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")


#################
# API ENDPOINTS #
#################

@app.get("/", response_class=FileResponse)
async def root():
    return index_path

@app.get("/health")
async def health():
    return {"status": "ok", "message": "The Pickles API is available."}
