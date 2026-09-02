import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.customer_router import customer_router
from backend.api.merchant_router import merchant_router
from database.database import db

app = FastAPI(
    title="PayPilot Agent API",
    description="Backend API for AI-Powered Agentic Commerce & Merchant Growth Platform (Razorpay AI Builder Track 1)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customer_router)
app.include_router(merchant_router)

@app.on_event("startup")
def startup_event():
    # Ensure tables are initialized
    db.init_db()

@app.get("/")
def healthcheck():
    return {
        "status": "healthy",
        "service": "PayPilot Agent API",
        "version": "1.0.0",
        "demo_mode": True,
        "payment_environment": "Demo / Test Simulated Payment"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)
