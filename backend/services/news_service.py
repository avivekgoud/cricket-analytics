"""
Cricket Analytics Platform - News & Player Availability Tracker
"""
from typing import Dict, List, Any

class NewsService:
    def __init__(self):
        self.news_items = [
            {
                'id': 'news_1',
                'title': 'IPL 2026 Season Schedule Confirmed with 74 Fixtures Across 10 Venues',
                'category': 'Tournament',
                'date': '2026-08-28',
                'source': 'Official League Board',
                'summary': 'The 2026 edition of the Indian Premier League is set to commence with CSK hosting MI at the Wankhede Stadium.'
            },
            {
                'id': 'news_2',
                'title': 'Jasprit Bumrah Cleared by Medical Staff for Full 4-Over Bowling Load',
                'category': 'Player Availability',
                'date': '2026-08-26',
                'source': 'BCCI Medical Center',
                'summary': 'Lead pacer Jasprit Bumrah has resumed full intensity net bowling following routine workload management.'
            },
            {
                'id': 'news_3',
                'title': 'Heinrich Klaasen Crowned Most Lethal Death Overs Striker with 204.5 SR',
                'category': 'Analytics Insight',
                'date': '2026-08-24',
                'source': 'Cricket Analytics Lab',
                'summary': 'Statistical modeling confirms Klaasen holds the highest expected boundary conversion against both pace and spin in overs 16-20.'
            }
        ]
        self.availability_records = [
            {'player': 'Virat Kohli', 'team': 'Royal Challengers Bengaluru', 'status': 'Available', 'notes': 'Full match fitness', 'verified': True},
            {'player': 'Jasprit Bumrah', 'team': 'Mumbai Indians', 'status': 'Available', 'notes': 'Cleared for starting XI', 'verified': True},
            {'player': 'Ruturaj Gaikwad', 'team': 'Chennai Super Kings', 'status': 'Available', 'notes': 'Active captain', 'verified': True},
            {'player': 'Mohammed Shami', 'team': 'Gujarat Titans', 'status': 'Injured (Recovering)', 'notes': 'Rehab progressing well', 'verified': True},
            {'player': 'Rishabh Pant', 'team': 'Delhi Capitals', 'status': 'Available', 'notes': 'Wicketkeeping and captaining', 'verified': True},
            {'player': 'Travis Head', 'team': 'Sunrisers Hyderabad', 'status': 'Available', 'notes': 'In squad', 'verified': True}
        ]

    def get_news(self) -> List[Dict[str, Any]]:
        return self.news_items

    def get_availability(self) -> List[Dict[str, Any]]:
        return self.availability_records

news_service = NewsService()
