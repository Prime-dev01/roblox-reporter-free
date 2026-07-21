import requests
import random
import string
import time
from datetime import datetime, timedelta
from colorama import Fore, Style

class AccountCreator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        self.created_accounts = []
    
    def generate_username(self):
        timestamp = datetime.now().strftime("%H%M%S")
        adjectives = ["Cool", "Epic", "Super", "Mega", "Ultra", "Pro", "Ninja", "Dragon", "Shadow", "Storm"]
        nouns = ["Player", "Gamer", "Wolf", "Fox", "Tiger", "Hawk", "Phoenix", "Knight", "Wizard", "Hero"]
        
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        return f"{adj}{noun}{timestamp}"
    
    def generate_password(self, length=16):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))
    
    def generate_birthday(self):
        year = random.randint(1990, 2005)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"
    
    def warmup_account(self, username, password):
        try:
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            session.post("https://auth.roblox.com/v2/logout")
            
            payload = {
                "ctype": "Username",
                "cvalue": username,
                "password": password
            }
            
            response = session.post(
                "https://auth.roblox.com/v2/login",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                print(f"{Fore.CYAN}[*] Warming up account: {username}{Style.RESET_ALL}")
                
                time.sleep(random.uniform(1, 3))
                session.get("https://www.roblox.com/home")
                time.sleep(random.uniform(0.5, 1.5))
                session.get("https://www.roblox.com/my/avatar")
                time.sleep(random.uniform(0.5, 1.5))
                session.get("https://www.roblox.com/catalog")
                time.sleep(random.uniform(0.5, 1.5))
                
                print(f"{Fore.GREEN}[+] Account warmed up: {username}{Style.RESET_ALL}")
                return True
                
        except Exception as e:
            print(f"{Fore.YELLOW}[*] Warmup skipped for {username}: {e}{Style.RESET_ALL}")
            return False
    
    def create_account(self):
        try:
            username = self.generate_username()
            password = self.generate_password()
            birthday = self.generate_birthday()
            
            self.session.get("https://www.roblox.com")
            
            payload = {
                "username": username,
                "password": password,
                "birthday": birthday,
                "gender": random.choice([1, 2, 3]),
                "agreeToTerms": True
            }
            
            headers = {
                "Content-Type": "application/json",
                "Referer": "https://www.roblox.com/account/signup"
            }
            
            response = self.session.post(
                "https://auth.roblox.com/v2/signup",
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] Account created: {username}:{password}{Style.RESET_ALL}")
                
                self.warmup_account(username, password)
                
                with open("accounts.txt", "a") as f:
                    f.write(f"{username}:{password}\n")
                
                account_info = {
                    "email": username,
                    "password": password,
                    "username": username
                }
                self.created_accounts.append(account_info)
                return account_info
            else:
                print(f"{Fore.RED}[!] Account creation failed: {response.status_code}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] Account creation error: {e}{Style.RESET_ALL}")
            return None
    
    def create_bulk(self, count=10):
        print(f"{Fore.CYAN}[*] Creating {count} accounts with warmup...{Style.RESET_ALL}")
        
        created = 0
        for i in range(count):
            print(f"{Fore.CYAN}[*] Creating account {i+1}/{count}...{Style.RESET_ALL}")
            
            account = self.create_account()
            if account:
                created += 1
            
            delay = random.uniform(3, 7)
            time.sleep(delay)
        
        print(f"{Fore.GREEN}[+] Created {created}/{count} accounts with warmup{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Saved to accounts.txt{Style.RESET_ALL}")
        return self.created_accounts
