# main.py
import os
from fastapi import FastAPI, Depends, HTTPException
from clients.base import IncidentClient, Incident
from clients.json_server import JSONServerClient
from metrics import compute_mttd, compute_mttr, compute_mtta, compute_mtbf

app = FastAPI()

def get_incident_client() -> IncidentClient:
    # for now, always use JSON mock
    url = os.getenv("JSON_SERVER_URL", "http://host.docker.internal:4000")
    return JSONServerClient(base_url=url)

@app.get("/incidents/", response_model=list[Incident])
def read_incidents(client: IncidentClient = Depends(get_incident_client)):
    return client.list_incidents()

@app.get("/metrics/")
def read_metrics(client: IncidentClient = Depends(get_incident_client)):
    incs = client.list_incidents()
    if not incs:
        raise HTTPException(status_code=404, detail="No incidents found")
    return {
        "mtta_seconds": compute_mtta(incs),
        "mttd_seconds": compute_mttd(incs),
        "mttr_seconds": compute_mttr(incs),
        "mtbf_seconds": compute_mtbf(incs),
    }
