import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_dir="data/processed/reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_report(self, state):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{self.output_dir}/Incident_{state['event_name']}_{int(datetime.now().timestamp())}.md"
        
        report_content = f"""# Incident Report

**Time:** {timestamp}
**Location:** Main Entrance Camera
**Event:** {state['event_name']}
**Risk Level:** {state['risk_level']}

## Description
{state['vision_context']}

## Associated System Policy
{state['policy_context']}

## Agent Recommendations
{state['report']}
"""
        with open(filename, "w") as f:
            f.write(report_content)
            
        return filename
