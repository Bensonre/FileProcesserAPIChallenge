from typing import Union, List, Optional
from fastapi import FastAPI
from pydantic import BaseModel
from urllib.parse import urlparse
import os
import requests
from common.Status import Status
from common.QueuingService import QueuingService
from common.DataService import DataService

app = FastAPI()
data = DataService()
queue = QueuingService()

class Files(BaseModel):
    uris: List[str]
    out_uri: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/trigger")
def put_files(files: Files):
    #Store job in Database and create Job id
    job_id = data.create_job()
    for file in files.uris:
        # Queue the file for Processing
        queue.queue(file, files.out_uri, job_id)
        # Store the file in database to keep track of status
        data.create_file(file, job_id, Status.get_status(1), files.out_uri)
    return {"job_id": job_id}

@app.get("/Status/{job_id}")
def get_Job_Status(job_id: int):
    return data.get_job(job_id, "status")

@app.get("/Status/{job_id}/{fileName}")
def get_Job_Status(job_id: int, fileName: str):
    return data.get_file(job_id,fileName,"status")

@app.get("/Retrieve/{job_id}")
def get_file_uris(job_id: int):
    return { 
            "job_id": job_id,
            "files": data.get_job_files(job_id,"file_name, out_uri, status")
           }

@app.get("/Retrieve/{job_id}/{fileName}")
def get_file(job_id: int, fileName: str):
    results = dict(data.get_file(job_id,fileName,"out_uri, status"))
    if (results["status"] != Status.get_status(4)):
        return results
    return requests.get(results["out_uri"])