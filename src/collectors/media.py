from ..client import InstagramClient
from datetime import datetime

class MediaCollector:
    def __init__(self, client):
        self.client = client

    def getRecentMedia(self, username, amount=12):
        """Get recent posts from a user"""
        try:
            userID = self.client.cl.user_id_from_username(username)
            medias = self.client.cl.user_medias(userID, amount)
            
            mediaList = []
            for media in medias:
                mediaData = {
                    'id': media.id,
                    'type': media.media_type.name if hasattr(media.media_type, 'name') else str(media.media_type),
                    'caption': media.caption_text if media.caption_text else '',
                    'likes': media.like_count,
                    'comments': media.comment_count,
                    'timestamp': media.taken_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f"https://www.instagram.com/p/{media.code}/",
                    'location': media.location.name if media.location else None
                }
                mediaList.append(mediaData)
            
            return mediaList
        except Exception as e:
            return {'error': str(e)}
    
    def analyzePostingPatterns(self, username, amount=50):
        """Analyze when user posts most frequently"""
        try:
            userID = self.client.cl.user_id_from_username(username)
            medias = self.client.cl.user_medias(userID, amount)
            
            hourCounts = {}
            dayOfWeekCounts = {}
            
            for media in medias:
                hour = media.taken_at.hour
                dayOfWeek = media.taken_at.strftime('%A')
                
                hourCounts[hour] = hourCounts.get(hour, 0) + 1
                dayOfWeekCounts[dayOfWeek] = dayOfWeekCounts.get(dayOfWeek, 0) + 1
            
            mostActiveHour = max(hourCounts.items(), key=lambda x: x[1]) if hourCounts else (None, 0)
            mostActiveDay = max(dayOfWeekCounts.items(), key=lambda x: x[1]) if dayOfWeekCounts else (None, 0)
            
            return {
                'totalAnalyzed': len(medias),
                'hourlyDistribution': hourCounts,
                'dayOfWeekDistribution': dayOfWeekCounts,
                'mostActiveHour': mostActiveHour[0],
                'mostActiveDay': mostActiveDay[0],
                'avgLikes': sum(m.like_count for m in medias) / len(medias) if medias else 0,
                'avgComments': sum(m.comment_count for m in medias) / len(medias) if medias else 0
            }
        except Exception as e:
            return {'error': str(e)}