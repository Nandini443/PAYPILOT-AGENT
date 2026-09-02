from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class CustomerIntent(BaseModel):
    raw_query: str
    category: Optional[str] = None
    budget: Optional[float] = None
    min_rating: Optional[float] = None
    preferences: List[str] = Field(default_factory=list)
    confidence: float = 1.0

class AgentExecutionStep(BaseModel):
    step_id: str
    title: str
    tool_name: str
    status: str = "COMPLETED" # RUNNING, COMPLETED, FAILED
    details: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

class ProductCandidate(BaseModel):
    product_id: str
    product_name: str
    category: str
    price: float
    rating: float
    review_count: int
    stock: int
    brand: str
    features: List[str] = Field(default_factory=list)
    image_url: Optional[str] = None
    ai_match_score: int = 50
    match_reasons: List[str] = Field(default_factory=list)

class CartItemSchema(BaseModel):
    product_id: str
    product_name: str
    price: float
    quantity: int = 1
    subtotal: float
    image_url: Optional[str] = None

class CustomerSessionState(BaseModel):
    session_id: str
    customer_id: str = "CUST-DEMO-001"
    intent: Optional[CustomerIntent] = None
    cart: List[Dict[str, Any]] = Field(default_factory=list)
    recommended_products: List[Dict[str, Any]] = Field(default_factory=list)
    best_recommendation: Optional[Dict[str, Any]] = None
    active_order: Optional[Dict[str, Any]] = None
    active_transaction: Optional[Dict[str, Any]] = None
    activity_log: List[AgentExecutionStep] = Field(default_factory=list)

class MerchantSessionState(BaseModel):
    session_id: str
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)
    selected_timeframe: str = "Last 90 Days"
    active_insights: List[Dict[str, Any]] = Field(default_factory=list)
