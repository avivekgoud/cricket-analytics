"""
Cricket Analytics Platform - Admin & Data Source Manager
"""
import time
from typing import Dict, List, Any

class AdminService:
    def __init__(self):
        self.sources = [
            {'name': 'Local Ball-by-Ball IPL Database', 'type': 'CSV Ingest', 'status': 'Active (1,169 Matches)', 'last_sync': '2026-08-30 14:00'},
            {'name': 'Cricbuzz / Live Data Feeder (API)', 'type': 'REST Webhook', 'status': 'Connected (Simulated)', 'last_sync': '2026-08-30 19:15'},
            {'name': 'International Player Registry', 'type': 'JSON Feed', 'status': 'Active', 'last_sync': '2026-08-29 10:00'}
        ]
        self.audit_log = [
            {'timestamp': '2026-08-30 14:00', 'action': 'Full Ball-by-Ball Ingest', 'records': '278,205 balls', 'user': 'System Daemon'},
            {'timestamp': '2026-08-30 14:05', 'action': 'Index Rebuild', 'records': '771 player profiles', 'user': 'Analytics Engine'}
        ]

    def get_status(self) -> Dict[str, Any]:
        return {
            'data_sources': self.sources,
            'audit_log': self.audit_log,
            'sync_health': 'Optimal (All local indices synchronized)'
        }

admin_service = AdminService()
