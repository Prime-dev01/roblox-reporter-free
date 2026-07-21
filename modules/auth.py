import requests
import cloudscraper
import time
import random
from colorama import Fore, Style
from config import Config

class RobloxAuth:
    def __init__(self, proxy=None):
        self.session = cloudscraper.create_scraper()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://www.roblox.com",
            "Referer": "https://www.roblox.com/"
        })
        
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}
        
        self.csrf_token = None
        self.authenticity_token = None
        self.is_authenticated = False
    
    def get_csrf_token(self):
        try:
            response = self.session.post(Config.ROBLOX_CSRF_URL)
            if 'x-csrf-token' in response.headers:
                self.csrf_token = response.headers['x-csrf-token']
                self.session.headers['x-csrf-token'] = self.csrf_token
                return True
            return False
        except Exception as e:
            print(f"{Fore.RED}[!] CSRF error: {e}{Style.RESET_ALL}")
            return False
    
    def login(self, username, password):
        try:
            self.get_csrf_token()
            
            payload = {
                "ctype": "Username",
                "cvalue": username,
                "password": password
            }
            
            response = self.session.post(
                Config.ROBLOX_AUTH_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                self.is_authenticated = True
                print(f"{Fore.GREEN}[+] Login success: {username}{Style.RESET_ALL}")
                return True
            else:
                print(f"{Fore.RED}[!] Login failed for {username}: {response.status_code}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Login error: {e}{Style.RESET_ALL}")
            return False
    
    def get_authenticity_token(self):
        try:
            response = self.session.get("https://www.roblox.com/report/user")
            if response.status_code == 200:
                import re
                match = re.search(r'__RequestVerificationToken.*?value="([^"]+)"', response.text)
                if match:
                    self.authenticity_token = match.group(1)
                    return self.authenticity_token
            return None
        except Exception as e:
            print(f"{Fore.RED}[!] Auth token error: {e}{Style.RESET_ALL}")
            return None
