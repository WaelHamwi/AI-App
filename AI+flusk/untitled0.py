# -*- coding: utf-8 -*-
"""
Created on Mon May 22 03:13:56 2023

@author: WAEL
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}