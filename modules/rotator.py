import random
import time
import threading
from queue import Queue
from datetime import datetime
from colorama import Fore, Style

class AccountRotator:
    def __init__(self, account_file="accounts.txt"):
        self.accounts = self.load_accounts(account_file)
        self.account_queue = Queue()
        self.current_account = None
        self.lock = threading.Lock()
        self.daily_usage = {}
        
        for acc in self.accounts:
            self.account_queue.put(acc)
    
    def load_accounts(self, filename):
        accounts = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    if ':' in line:
                        email, password = line.strip().split(':', 1)
                        accounts.append({
                            'email': email,
                            'password': password,
                            'used_count': 0,
                            'banned': False,
                            'cooldown': 0,
                            'reports_sent': 0,
                            'daily_reports': 0,
                            'last_used_date': None,
                            'created_at': datetime.now()
                        })
            print(f"{Fore.CYAN}[*] Loaded {len(accounts)} accounts{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.YELLOW}[*] No accounts.txt found. Will create accounts automatically.{Style.RESET_ALL}")
        return accounts
    
    def get_next_account(self):
        with self.lock:
            today = datetime.now().strftime('%Y%m%d')
            
            for _ in range(len(self.accounts)):
                acc = self.account_queue.get()
                self.account_queue.put(acc)
                
                if acc['last_used_date'] != today:
                    acc['daily_reports'] = 0
                    acc['last_used_date'] = today
                
                if (not acc['banned'] and 
                    time.time() > acc['cooldown'] and 
                    acc['reports_sent'] < 5 and
                    acc['daily_reports'] < 10):
                    
                    acc['used_count'] += 1
                    acc['daily_reports'] += 1
                    self.current_account = acc
                    return acc
            
            print(f"{Fore.YELLOW}[!] All accounts in cooldown. Waiting 2 minutes...{Style.RESET_ALL}")
            time.sleep(120)
            return self.get_next_account()
    
    def mark_account_banned(self, account):
        with self.lock:
            account['banned'] = True
            print(f"{Fore.RED}[!] Account {account['email']} marked as BANNED{Style.RESET_ALL}")
    
    def set_cooldown(self, account, seconds=180):
        with self.lock:
            variance = random.randint(-30, 30)
            actual_cooldown = max(60, seconds + variance)
            account['cooldown'] = time.time() + actual_cooldown
            print(f"{Fore.YELLOW}[*] Account {account['email']} cooldown: {actual_cooldown}s{Style.RESET_ALL}")
    
    def increment_reports(self, account):
        with self.lock:
            account['reports_sent'] += 1
    
    def get_account_status(self):
        with self.lock:
            total = len(self.accounts)
            banned = sum(1 for a in self.accounts if a['banned'])
            available = sum(1 for a in self.accounts if not a['banned'] and time.time() > a['cooldown'])
            return total, banned, available
