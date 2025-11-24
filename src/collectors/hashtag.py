from ..client import InstagramClient

class HashtagCollector:
    def __init__(self, client):
        self.client = client

    def getTopPostsByHashtag(self, hashtag, amount=27):
        """Get top posts for a hashtag"""
        try:
            #Remove # if provided
            hashtag = hashtag.replace('#', '')
            
            medias = self.client.cl.hashtag_medias_top(hashtag, amount)
            
            postList = []
            for media in medias:
                postData = {
                    'username': media.user.username,
                    'caption': media.caption_text[:100] if media.caption_text else '',
                    'likes': media.like_count,
                    'comments': media.comment_count,
                    'timestamp': media.taken_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'url': f"https://www.instagram.com/p/{media.code}/"
                }
                postList.append(postData)
            
            return postList
        except Exception as e:
            return {'error': str(e)}
    
    def getHashtagInfo(self, hashtag):
        """Get hashtag information"""
        try:
            hashtag = hashtag.replace('#', '')
            info = self.client.cl.hashtag_info(hashtag)
            
            return {
                'name': info.name,
                'mediaCount': info.media_count,
                'profilePicUrl': info.profile_pic_url if hasattr(info, 'profile_pic_url') else None
            }
        except Exception as e:
            return {'error': str(e)}
