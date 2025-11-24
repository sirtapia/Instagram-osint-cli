from ..client import InstagramClient

class NetworkCollector:
    def __init__(self, client):
        self.client = client

    def getFollowers(self, username, amount=50):
        """Get list of followers"""
        try:
            userID = self.client.cl.user_id_from_username(username)
            followers = self.client.cl.user_followers(userID, amount)
            
            followerList = []
            for userID, user in followers.items():
                followerList.append({
                    'username': user.username,
                    'fullName': user.full_name if hasattr(user, 'full_name') else 'N/A',
                    'isVerified': user.is_verified if hasattr(user, 'is_verified') else False,
                    'isPrivate': user.is_private if hasattr(user, 'is_private') else False,
                    'profilePicUrl': user.profile_pic_url if hasattr(user, 'profile_pic_url') else None
                })
            
            return followerList
        except Exception as e:
            return {'error': str(e)}
    
    def getFollowing(self, username, amount=50):
        """Get list of users the account follows"""
        try:
            userID = self.client.cl.user_id_from_username(username)
            following = self.client.cl.user_following(userID, amount)
            
            followingList = []
            for userID, user in following.items():
                followingList.append({
                    'username': user.username,
                    'fullName': user.full_name if hasattr(user, 'full_name') else 'N/A',
                    'isVerified': user.is_verified if hasattr(user, 'is_verified') else False,
                    'isPrivate': user.is_private if hasattr(user, 'is_private') else False,
                    'profilePicUrl': user.profile_pic_url if hasattr(user, 'profile_pic_url') else None
                })
            
            return followingList
        except Exception as e:
            return {'error': str(e)}
    
    def getMutualConnections(self, username1, username2):
        """Find mutual followers between two accounts"""
        try:
            userID1 = self.client.cl.user_id_from_username(username1)
            userID2 = self.client.cl.user_id_from_username(username2)
            
            followers1 = set(self.client.cl.user_followers(userID1, 100).keys())
            followers2 = set(self.client.cl.user_followers(userID2, 100).keys())
            
            mutualIDs = followers1.intersection(followers2)
            
            mutualList = []
            for uid in mutualIDs:
                try:
                    user = self.client.cl.user_info(uid)
                    mutualList.append({
                        'username': user.username,
                        'fullName': user.full_name if hasattr(user, 'full_name') else 'N/A'
                    })
                except:
                    continue
            
            return {
                'count': len(mutualList),
                'mutualFollowers': mutualList
            }
        except Exception as e:
            return {'error': str(e)}