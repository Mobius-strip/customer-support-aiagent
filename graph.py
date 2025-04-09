# graph.py
"""State graph construction for the food delivery support agent."""
from typing import Callable, Any, Optional, Type, Dict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

def build_support_graph(
    *,
    state_schema: Optional[Type[Any]] = None,
    config_schema: Optional[Type[Any]] = None,
    input_schema: Optional[Type[Any]] = None,
    output_schema: Optional[Type[Any]] = None,
    node_functions: Dict[str, Callable],
    router_functions: Dict[str, Callable],
) -> StateGraph:
    """
    Build and return the state graph for the food delivery support agent.
    
    Args:
        state_schema: Type definition for the state
        config_schema: Configuration schema
        input_schema: Input schema
        output_schema: Output schema
        node_functions: Dictionary of node implementation functions
        router_functions: Dictionary of conditional routing functions
        
    Returns:
        StateGraph: The constructed graph
    """
    # Validate function implementations
    expected_node_functions = {
        "classifier",
        "problem_verify", 
        "agent",
        "eta_tool",
        "check_resolution",
        "human_in_the_loop",
        "service_complaint",
        "bill_amount_verification",
        "refund_tool",
    }
    
    expected_router_functions = {
        "refundable_or_not",
        "verified_or_not",
        "user_convo",
        "satisfied_or_not",
    }
    
    # Check for missing node functions
    missing_nodes = expected_node_functions - set(node_functions.keys())
    if missing_nodes:
        raise ValueError(f"Missing node implementations for: {missing_nodes}")
        
    # Check for missing router functions
    missing_routers = expected_router_functions - set(router_functions.keys())
    if missing_routers:
        raise ValueError(f"Missing router implementations for: {missing_routers}")
    
    # Create the state graph
    builder = StateGraph(
        state_schema=state_schema,
        config_schema=config_schema,
        input=input_schema,
        output=output_schema
    )
    
    # Add nodes to the graph
    builder.add_node("classifier", node_functions["classifier"])
    builder.add_node("problem verify", node_functions["problem_verify"])
    builder.add_node("Agent", node_functions["agent"])
    builder.add_node("ETA tool", node_functions["eta_tool"])
    builder.add_node("check", node_functions["check_resolution"])
    builder.add_node("Human in loop", node_functions["human_in_the_loop"])
    builder.add_node("Service complaint Tool", node_functions["service_complaint"])
    builder.add_node("Bill Amount verification", node_functions["bill_amount_verification"])
    builder.add_node("Refund Tool", node_functions["refund_tool"])
    
    # Add fixed edges
    builder.add_edge(START, "classifier")
    builder.add_edge("ETA tool", "Agent")
    builder.add_edge("Service complaint Tool", "Agent")
    builder.add_edge("Bill Amount verification", "Refund Tool")
    builder.add_edge("Refund Tool", "check")
    
    # Add conditional edges
    builder.add_conditional_edges(
        "classifier",
        router_functions["refundable_or_not"],
        [
            "problem verify",
            "Agent",
        ],
    )
    
    builder.add_conditional_edges(
        "Agent",
        router_functions["user_convo"],
        [
            "ETA tool",
            "check",
            "Service complaint Tool",
            "Agent",
        ],
    )
    
    builder.add_conditional_edges(
        "check",
        router_functions["satisfied_or_not"],
        [
            END,
            "Human in loop",
        ],
    )
    
    builder.add_conditional_edges(
        "problem verify",
        router_functions["verified_or_not"],
        [
            "Bill Amount verification",
            "Human in loop",
        ],
    )
    
    return builder