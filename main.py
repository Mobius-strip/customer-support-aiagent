# main.py
"""Main application for the Food Delivery Support Agent."""
import logging
from typing import Dict, Any, Callable

from schemas import SomeState, create_initial_state
from models import setup_llm_models, setup_vision_models 
from nodes import NodeFunctions
from conditionals import ConditionalRouters
from graph import build_support_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_models() -> Dict[str, Any]:
    """Set up and return all required models."""
    logger.info("Setting up language models...")
    llm_models = setup_llm_models()
    
    logger.info("Setting up vision models...")
    vision_models = setup_vision_models()
    
    # Combine all models into one dictionary
    return {**llm_models, **vision_models}

def create_support_agent():
    """Create and return the compiled support agent."""
    # Set up models
    models = setup_models()
    
    # Create node function implementations
    logger.info("Creating node functions...")
    node_funcs = NodeFunctions(models)
    
    # Create router function implementations
    logger.info("Creating router functions...")
    router_funcs = ConditionalRouters(models)
    
    # Create node function dictionary
    node_functions = {
        "classifier": node_funcs.classifier,
        "problem_verify": node_funcs.problem_verify,
        "agent": node_funcs.agent,
        "eta_tool": node_funcs.eta_tool,
        "check_resolution": node_funcs.check_resolution,
        "human_in_the_loop": node_funcs.human_in_the_loop,
        "service_complaint": node_funcs.service_complaint,
        "bill_amount_verification": node_funcs.bill_amount_verification,
        "refund_tool": node_funcs.refund_tool,
    }
    
    # Create router function dictionary
    router_functions = {
        "refundable_or_not": router_funcs.refundable_or_not,
        "verified_or_not": router_funcs.verified_or_not,
        "user_convo": router_funcs.user_convo,
        "satisfied_or_not": router_funcs.satisfied_or_not,
    }
    
    # Build the graph
    logger.info("Building support agent graph...")
    agent_graph = build_support_graph(
        state_schema=SomeState,
        node_functions=node_functions,
        router_functions=router_functions,
    )
    
    # Compile the graph
    logger.info("Compiling support agent graph...")
    return agent_graph.compile()

def run_support_flow():
    """
    Run the food delivery support agent workflow.
    """
    logger.info("Starting Food Delivery Support Agent Demo")
    print("\nWelcome to the Food Delivery Support Agent Demo!")
    print("-------------------------------------------------")

    # Get initial user message
    user_message = input("\nPlease describe your issue or complaint: ")
    
    # Create initial state
    state = create_initial_state(user_message)
    
    try:
        # Create and compile the agent
        compiled_agent = create_support_agent()
        
        # Invoke the workflow
        logger.info("Invoking agent workflow")
        final_state = compiled_agent.invoke(state)

        # Display results
        print("\n---- Conversation/Notes ----")
        print(final_state["notes"])
        print("----------------------------")

        logger.info("Workflow completed")
        print("Workflow completed. Final state summary:")
        print(f"- Issue type: {final_state['classification']}")
        print(f"- Resolved: {final_state['resolved']}")
        if final_state.get('refund_amount'):
            print(f"- Refund processed: {final_state['refund_amount']} for {final_state['refund_prdct']}")
            
    except Exception as e:
        logger.error(f"Error during workflow execution: {e}", exc_info=True)
        print(f"An error occurred: {e}")
        
    print("Thank you for using our Food Delivery Support Agent!\n")

if __name__ == "__main__":
    run_support_flow()