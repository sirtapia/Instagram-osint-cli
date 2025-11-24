import warnings
warnings.filterwarnings('ignore')

from instagrapi import Client
from dotenv import load_dotenv
import os
import json

class InstagramClient:
    def __init__(self):
        load_dotenv()
        self.cl = Client()
        self.username = os.getenv('INSTAGRAM_USERNAME')
        self.password = os.getenv('INSTAGRAM_PASSWORD')
        self.sessionFile = 'session.json'
        
    def login(self):
        """Authenticate with Instagram using session or credentials"""
        try:
            #Try to load existing session
            if os.path.exists(self.sessionFile):
                self.cl.load_settings(self.sessionFile)
                self.cl.login(self.username, self.password)
                #verify session works
                self.cl.get_timeline_feed()
            else:
                #fresh login
                self.cl.login(self.username, self.password)
                #save session for future use
                self.cl.dump_settings(self.sessionFile)
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            #if session is corrupted, delete and retry
            if os.path.exists(self.sessionFile):
                os.remove(self.sessionFile)
            return False
        
