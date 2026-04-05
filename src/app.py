# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


###############################################
# APP SETUP                                   #
###############################################

app = FastAPI()

# Serve static files from the 'static' directory
static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")


###############################################
# API ENDPOINTS                               #
###############################################

@app.get("/")
async def root():
    return {"status": "ok", "message": "Welcome to the Pickles API"}

@app.get("/ui")
async def ui():
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path, media_type="text/html")
