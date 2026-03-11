from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    event_name: str
    event_data: Dict[str, Any]
    vision_context: str
    policy_context: str
    risk_level: str
    report: str
    alert_triggered: bool

# Agent Node Functions
def vision_node(state: AgentState):
    state["vision_context"] = f"Detected visual activity related to: {state['event_name']} with data {state['event_data']}"
    return state

from rag.knowledge_base import KnowledgeBase

# Initialize the RAG system centrally
kb = KnowledgeBase()

def context_node(state: AgentState):
    # Retrieve semantic policy
    policy = kb.query_policy(state["event_name"])
    state["policy_context"] = f"Policy retrieved: {policy}"
    return state

def decision_node(state: AgentState):
    # Determine risk
    if state["event_name"] == "restricted_area_entry":
        state["risk_level"] = "HIGH"
    elif state["event_name"] == "loitering" or state["event_name"] == "crowd_detected":
        state["risk_level"] = "MEDIUM"
    else:
        state["risk_level"] = "LOW"
    return state

from automation.report_generator import ReportGenerator
from backend.database import IncidentDatabase
import time

report_gen = ReportGenerator()
db = IncidentDatabase()

def report_node(state: AgentState):
    # Draft recommendations and dump to markdown
    state["report"] = f"Action Required: Investigate camera {state['event_data'].get('location', 'Main Entrance')} immediately."
    report_filename = report_gen.generate_report(state)
    print(f"[*] Report saved at: {report_filename}")
    return state

def alert_node(state: AgentState):
    if state["risk_level"] in ["MEDIUM", "HIGH", "CRITICAL"]:
        state["alert_triggered"] = True
        print(f"!!! DISPATCHING ALERT !!! -> {state['event_name']} ({state['risk_level']} RISK)")
        
        # Log to Database
        db.insert_incident({
            "timestamp": time.time(),
            "event_type": state["event_name"],
            "location": state["event_data"].get("location", "Main Entrance"),
            "risk_level": state["risk_level"],
            "description": state["vision_context"]
        })
        print("[*] Alert logged to Incident Database.")
    else:
        state["alert_triggered"] = False
    return state

def build_surveillance_graph():
    builder = StateGraph(AgentState)
    
    # 1. Add agent nodes
    builder.add_node("vision_agent", vision_node)
    builder.add_node("context_agent", context_node)
    builder.add_node("decision_agent", decision_node)
    builder.add_node("report_agent", report_node)
    builder.add_node("alert_agent", alert_node)

    # 2. Add edges shaping the agent flow
    builder.add_edge(START, "vision_agent")
    builder.add_edge("vision_agent", "context_agent")
    builder.add_edge("context_agent", "decision_agent")
    builder.add_edge("decision_agent", "report_agent")
    builder.add_edge("report_agent", "alert_agent")
    builder.add_edge("alert_agent", END)
    
    return builder.compile()
