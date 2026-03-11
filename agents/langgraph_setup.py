from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, START, END
from rag.knowledge_base import KnowledgeBase
from automation.report_generator import ReportGenerator
from backend.database import IncidentDatabase
from automation.notification_service import NotificationService
import time

class AgentState(TypedDict):
    event_name: str
    event_data: Dict[str, Any]
    vision_context: str
    policy_context: str
    historical_context: str
    risk_level: str
    reviewer_notes: str
    is_approved: bool
    report: str
    alert_triggered: bool

# Initialize System Tools
kb = KnowledgeBase()
report_gen = ReportGenerator()
db = IncidentDatabase()
notifier = NotificationService()

# 1. Vision Agent: Extracts primary visual context
def vision_node(state: AgentState):
    confidence = state["event_data"].get("confidence", 0.85)
    state["vision_context"] = f"Detected visual anomaly [{state['event_name']}] at {state['event_data'].get('location', 'Camera 1')} with {confidence*100:.1f}% confidence."
    return state

# 2. Context Agent: Queries RAG for corporate policy
def context_node(state: AgentState):
    policy = kb.query_policy(state["event_name"])
    state["policy_context"] = f"Corporate Protocol: {policy}"
    return state

# 3. Investigation Agent: Checks database for historical patterns to increase performance
def investigation_node(state: AgentState):
    # Simulate DB lookup for recent events of the same type
    recent_events = db.get_recent_incidents(limit=5)
    similar_count = sum(1 for e in recent_events if e['event_type'] == state["event_name"])
    state["historical_context"] = f"Found {similar_count} similar events in the last 24 hours. Pattern indicates possible recurring threat." if similar_count > 1 else "Isolated incident, no immediate historical pattern."
    return state

# 4. Decision Agent: Synthesizes Vision, Policy, and History to judge risk
def decision_node(state: AgentState):
    risk_score = 0
    # Base risk
    if state["event_name"] == "restricted_area_entry": risk_score += 8
    elif state["event_name"] == "crowd_detected": risk_score += 6
    elif state["event_name"] == "loitering": risk_score += 4
    
    # Modifier based on historical pattern (recurring threats escalate risk)
    if "recurring threat" in state["historical_context"]: risk_score += 2

    # Map score to level
    if risk_score >= 8: state["risk_level"] = "CRITICAL"
    elif risk_score >= 6: state["risk_level"] = "HIGH"
    elif risk_score >= 4: state["risk_level"] = "MEDIUM"
    else: state["risk_level"] = "LOW"
    return state

# 5. Reviewer Agent: Acts as a safeguard filter (Multi-Agent collaboration)
def reviewer_node(state: AgentState):
    # The reviewer cross-checks the decision to reduce False Positives
    confidence = state["event_data"].get("confidence", 0.0)
    
    if state["risk_level"] in ["HIGH", "CRITICAL"] and confidence < 0.50:
        state["is_approved"] = False
        state["reviewer_notes"] = "REJECTED: Risk level is high but vision confidence is too low. Downgrading to prevent false alarm."
        state["risk_level"] = "LOW"
    else:
        state["is_approved"] = True
        state["reviewer_notes"] = f"APPROVED: {state['risk_level']} risk assessment is justified based on evidence and policy."
    return state

# Router function for Conditional Edges
def reviewer_router(state: AgentState):
    if state["is_approved"] and state["risk_level"] in ["MEDIUM", "HIGH", "CRITICAL"]:
        return "report_agent"
    return "end" # Skip reporting for rejected or LOW risk events to save performance

# 6. Report Agent: Compiles final documentation
def report_node(state: AgentState):
    state["report"] = f"**Executive Summary:**\n{state['vision_context']}\n**Policy Applied:** {state['policy_context']}\n**History:** {state['historical_context']}\n**Reviewer Verdict:** {state['reviewer_notes']}"
    report_filename = report_gen.generate_report(state)
    print(f"[*] Comprehensive Agentic Report generated: {report_filename}")
    return state

# 7. Alert Agent: Executes final actions
def alert_node(state: AgentState):
    state["alert_triggered"] = True
    print(f"\n🚨 [SYSTEM ALERT OUTBOUND] -> {state['event_name']} ({state['risk_level']} RISK) 🚨")
    
    incident_data = {
        "timestamp": time.time(),
        "event_type": state["event_name"],
        "location": state["event_data"].get("location", "Main Entrance"),
        "risk_level": state["risk_level"],
        "description": f"{state['vision_context']} | {state['reviewer_notes']}"
    }
    
    db.insert_incident(incident_data)
    
    if state["risk_level"] in ["HIGH", "CRITICAL"]:
        notifier.send_email_alert(incident_data)
        notifier.create_support_ticket(incident_data)
        
    return state

def build_surveillance_graph():
    builder = StateGraph(AgentState)
    
    # 1. Register Agents
    builder.add_node("vision_agent", vision_node)
    builder.add_node("context_agent", context_node)
    builder.add_node("investigation_agent", investigation_node)
    builder.add_node("decision_agent", decision_node)
    builder.add_node("reviewer_agent", reviewer_node)
    builder.add_node("report_agent", report_node)
    builder.add_node("alert_agent", alert_node)

    # 2. Wire the Multi-Agent Collaboration Flow
    builder.add_edge(START, "vision_agent")
    builder.add_edge("vision_agent", "context_agent")
    builder.add_edge("context_agent", "investigation_agent")
    builder.add_edge("investigation_agent", "decision_agent")
    builder.add_edge("decision_agent", "reviewer_agent")
    
    # 3. Conditional Routing based on Reviewer's verdict (Performance Optimization)
    builder.add_conditional_edges(
        "reviewer_agent",
        reviewer_router,
        {
            "report_agent": "report_agent",
            "end": END
        }
    )
    
    builder.add_edge("report_agent", "alert_agent")
    builder.add_edge("alert_agent", END)
    
    return builder.compile()
