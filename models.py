# models.py
"""Setup for language and vision models."""
import os
from typing import Callable, Any, Optional, Type
from typing_extensions import TypedDict

# ============== LangChain Imports ==============
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain_core.prompts import ChatPromptTemplate

# ============== LangGraph Imports ==============
from langgraph.constants import START, END
from langgraph.graph import StateGraph


from PIL import Image
import requests
from optimum.intel.openvino import OVModelForVisualCausalLM
from transformers import AutoProcessor, TextStreamer

from config import OPENAI_API_KEY, CLASSIFIER_MODEL, AGENT_MODEL, VISION_MODEL, AGENT_SYSTEM_PROMPT

def setup_llm_models():
    """Initialize and return the language models used in the application."""
    # Classifier model for determining if a complaint is refundable
    classifier_llm = ChatOpenAI(
        model_name=CLASSIFIER_MODEL,
        temperature=0.7,
    )
    
    # Agent conversation model
    agent_conversation_llm = ChatOpenAI(
        model_name=AGENT_MODEL,
        temperature=0.7,
    )
    
    system_message = SystemMessage(content=AGENT_SYSTEM_PROMPT)
    
    # Initialize the conversation chain with the system message
    agent_memory = ConversationBufferMemory()
    agent_conversation_chain = ConversationChain(
        llm=agent_conversation_llm,
        memory=agent_memory,
        verbose=False,
        prompt=ChatPromptTemplate.from_messages([
            ("system", system_message.content),
            ("human", "{input}"),
            ("ai", "{history}"),
        ]),
    )
    
    return {
        "classifier_llm": classifier_llm,
        "agent_conversation_llm": agent_conversation_llm,
        "agent_conversation_chain": agent_conversation_chain
    }

def setup_vision_models():
    """Initialize and return the vision models used in the application."""
    processor = AutoProcessor.from_pretrained(VISION_MODEL, trust_remote_code=True)
    ov_model = OVModelForVisualCausalLM.from_pretrained(VISION_MODEL, trust_remote_code=True)
    
    return {
        "processor": processor,
        "ov_model": ov_model
    }