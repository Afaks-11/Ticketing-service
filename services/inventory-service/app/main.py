import os
from fastapi import FastAPI

from .database import  engine
from . import models
from .routers import events, tickets, reservations

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory Service")

app.include_router(events.router)
app.include_router(tickets.router)
app.include_router(reservations.router)

@app.get("/health")
def health_check():
    return({ 'status': 200, 'message': 'Inventory service is active'})
    

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT"))
    uvicorn.run("app.main:app", host="localhost", port=port, reload=True)