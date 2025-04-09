# conditionals.py
"""Conditional routing functions for the workflow graph."""
from typing import Dict, Any
from langgraph.constants import END

from schemas import SomeState

class ConditionalRouters:
    """Collection of conditional routing functions for the workflow graph."""
    
    def __init__(self, models: Dict[str, Any]):
        """Initialize with required models."""
        self.agent_conversation_llm = models.get("agent_conversation_llm")
    
    def refundable_or_not(self, state: SomeState) -> str:
        """
        Route based on refundable classification.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node name
        """
        print("\n[Condition: refundable_or_not]")
        if state.get("classification") == "refundable":
            return "problem verify"
        else:
            return "Agent"

    def verified_or_not(self, state: SomeState) -> str:
        """
        Route based on verification status.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node name
        """
        print("\n[Condition: verified_or_not]")
        if state.get("verified", False):
            return "Bill Amount verification"
        else:
            return "Human in loop"

    def user_convo(self, state: SomeState) -> str:
        """
        Route based on user conversation intent analysis.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node name
        """
        print("\n[Condition: user_convo]")

        # Create a structured prompt for routing
        route_prompt = f"""
        The user last said: "{state['user_message']}".

        Analyze the message and choose the most appropriate route:

        1) Route to "ETA tool" if ANY of these apply:
           - User is asking when their order will arrive
           - User mentions delivery time, ETA, arrival, waiting, or timing
           - User wants to know how much longer they need to wait

        2) Route to "Service complaint" if ANY of these apply:
           - User complains about a rude or unprofessional delivery person
           - User mentions poor service quality
           - User has feedback about delivery staff behavior

        3) Route to "check" if ANY of these apply:
           - User indicates their question has been answered
           - User says "thank you" or expresses satisfaction
           - User has no further questions

        4) Route to "Agent" ONLY if none of the above apply.

        Return EXACTLY ONE of these four options (case sensitive):
        "ETA tool"
        "Service complaint"
        "check"
        "Agent"
        """

        route_decision = self.agent_conversation_llm.invoke(route_prompt).content.strip()
        print(f"user_convo decision text => {route_decision}")

        if "ETA tool" in route_decision:
            return "ETA tool"
        elif "Service complaint" in route_decision:
            return "Service complaint Tool"
        elif "check" in route_decision:
            return "check"
        else:
            return "Agent"

    def satisfied_or_not(self, state: SomeState) -> str:
        """
        Route based on resolution status.
        
        Args:
            state: Current workflow state
            
        Returns:
            Next node name or END
        """
        print("\n[Condition: satisfied_or_not]")
        return END if state.get("resolved", False) else "Human in loop"