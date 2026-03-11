import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AutomationService")

class NotificationService:
    def __init__(self):
        self.tickets_created = 0

    def create_support_ticket(self, incident_data):
        self.tickets_created += 1
        ticket_id = f"TKT-{int(time.time())}-{self.tickets_created}"
        logger.info(f"🚨 [AUTOMATION] Created Support Ticket: {ticket_id} for Priority Event: {incident_data.get('event_type')}")
        return ticket_id
        
    def send_email_alert(self, incident_data):
        logger.info(f"📧 [AUTOMATION] Sending Email Alert to Security Team - Subject: URGENT: {incident_data.get('risk_level')} Risk Detected - Location: {incident_data.get('location', 'Unknown')}")
        return True
