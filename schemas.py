# schemas.py
"""Type definitions and data schemas used throughout the application."""
from typing import TypedDict, Optional

class SomeState(TypedDict):
    """
    State object storing workflow data across nodes.
    
    Attributes:
        user_message: The user's current message
        user_first_message: The initial complaint or question
        verified: Whether the issue has been verified
        classification: "refundable" or "non_refundable"  
        resolved: Whether the issue has been resolved
        notes: Additional details or conversation logs
        refund_amount: Amount to be refunded
        refund_prdct: Product name for refund
        image_problem_path: Path to the problem image
        image_bill_path: Path to the bill image
    """
    user_message: str
    user_first_message: str
    verified: bool
    classification: str
    resolved: bool
    notes: str
    refund_amount: Optional[int]
    refund_prdct: Optional[str]
    image_problem_path: Optional[str]
    image_bill_path: Optional[str]

def create_initial_state(user_message: str) -> SomeState:
    """Create and return a new state object with default values."""
    return {
        "user_message": user_message,
        "user_first_message": user_message,
        "verified": False,
        "classification": "",
        "resolved": False,
        "notes": "",
        "refund_amount": 0,
        "refund_prdct": "",
        "image_problem_path": "",
        "image_bill_path": ""
    }