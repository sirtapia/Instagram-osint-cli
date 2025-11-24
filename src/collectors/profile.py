from ..client import InstagramClient

class ProfileCollector:
    def __init__(self, client):
        self.client = client

    def getProfileInfo(self, username):
        """Gather public profile information"""
        try: 
            userID = self.client.cl.user_id_from_username(username)
            userInfo = self.client.cl.user_info(userID)
            
            email = None
            phone = None
            
            
            #Email attributes
            if hasattr(userInfo, 'public_email') and userInfo.public_email:
                email = userInfo.public_email
            elif hasattr(userInfo, 'email') and userInfo.email:
                email = userInfo.email
            elif hasattr(userInfo, 'contact_email') and userInfo.contact_email:
                email = userInfo.contact_email
                
            #Phone attributes
            if hasattr(userInfo, 'contact_phone_number') and userInfo.contact_phone_number:
                phone = userInfo.contact_phone_number
            elif hasattr(userInfo, 'public_phone_number') and userInfo.public_phone_number:
                phone = userInfo.public_phone_number
            elif hasattr(userInfo, 'phone_number') and userInfo.phone_number:
                phone = userInfo.phone_number
            
            #Try alternative method using user_info_v1
            try:
                userInfoV1 = self.client.cl.user_info_v1(userID)
                if not email and hasattr(userInfoV1, 'public_email'):
                    email = userInfoV1.public_email
                if not phone and hasattr(userInfoV1, 'contact_phone_number'):
                    phone = userInfoV1.contact_phone_number
            except:
                pass

            return {
                'username': userInfo.username,
                'fullName': userInfo.full_name,
                'biography': userInfo.biography,
                'followers': userInfo.follower_count,
                'following': userInfo.following_count,
                'posts': userInfo.media_count,
                'isVerified': userInfo.is_verified,
                'isPrivate': userInfo.is_private,
                'profilePicUrl': userInfo.profile_pic_url,
                'externalUrl': userInfo.external_url if hasattr(userInfo, 'external_url') else None,
                'isBusinessAccount': userInfo.is_business if hasattr(userInfo, 'is_business') else False,
                'isCreator': userInfo.is_professional if hasattr(userInfo, 'is_professional') else False,
                'email': email if email else 'None',
                'phone': phone if phone else 'None',
                'category': userInfo.category if hasattr(userInfo, 'category') else None,
                'addressStreet': userInfo.address_street if hasattr(userInfo, 'address_street') else None,
                'city': userInfo.city_name if hasattr(userInfo, 'city_name') else None,
                'zipCode': userInfo.zip if hasattr(userInfo, 'zip') else None
            }
        except Exception as e:
            return {'error': str(e)}
