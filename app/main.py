"""Main FastAPI Application"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Python Application",
    description="Sample Python application with Jenkins CI/CD pipeline",
    version="1.0.0"
)


class Item(BaseModel):
    """Item model for request/response"""
    id: int
    name: str
    description: str = None
    price: float


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str


# In-memory storage for demo
items_db = {}


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Python Application",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ready": "/ready",
            "items": "/items",
            "docs": "/docs"
        }
    }


@app.get("/health", tags=["Health"], response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes liveness probe"""
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.get("/ready", tags=["Health"])
async def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe"""
    logger.info("Readiness check requested")
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/items", tags=["Items"])
async def list_items():
    """Get all items"""
    logger.info("Listing all items")
    return {
        "items": list(items_db.values()),
        "count": len(items_db)
    }


@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: int):
    """Get a specific item by ID"""
    logger.info(f"Getting item with ID: {item_id}")
    if item_id not in items_db:
        logger.warning(f"Item {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", tags=["Items"])
async def create_item(item: Item):
    """Create a new item"""
    logger.info(f"Creating item: {item.name}")
    if item.id in items_db:
        logger.warning(f"Item {item.id} already exists")
        raise HTTPException(status_code=400, detail="Item already exists")
    items_db[item.id] = item
    return {
        "message": "Item created successfully",
        "item": item
    }


@app.put("/items/{item_id}", tags=["Items"])
async def update_item(item_id: int, item: Item):
    """Update an existing item"""
    logger.info(f"Updating item with ID: {item_id}")
    if item_id not in items_db:
        logger.warning(f"Item {item_id} not found for update")
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {
        "message": "Item updated successfully",
        "item": item
    }


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item"""
    logger.info(f"Deleting item with ID: {item_id}")
    if item_id not in items_db:
        logger.warning(f"Item {item_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {
        "message": "Item deleted successfully",
        "item": deleted_item
    }


@app.get("/stats", tags=["Stats"])
async def get_stats():
    """Get application statistics"""
    logger.info("Getting application statistics")
    return {
        "total_items": len(items_db),
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
