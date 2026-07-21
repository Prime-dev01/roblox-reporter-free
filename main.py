import os
import sys
import time
import threading
import random
from datetime import datetime
from colorama import Fore, Style, init
from modules.auth import RobloxAuth
from modules.reporter import RobloxReporter
from modules.rotator import AccountRotator
from modules.captcha_solver_free import FreeCaptchaSolver
from modules.account_creator import AccountCreator
from config import Config

init(autoreset=True)

class FreeBulkReporter:
    def __init__(self):
        self.rotator = AccountRotator()
        self.targets = self.load_targets()
        self.stats_lock = threading.Lock()
        self.stats = {
            "total_reports": 0,
            "successful": 0,
            "failed": 0,
            "accounts_used": 0,
            "accounts_banned": 0,
            "start_time": time.time(),
            "daily_target_count": {}
        }
        self.account_creator = AccountCreator()
        self.running = True
    
    def load_targets(self, filename="targets.txt"):
        targets = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    target = line.strip()
                    if target and not target.startswith('#'):
                        targets.append(target)
            print(f"{Fore.CYAN}[*] Loaded {len(targets)} targets{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}[!] targets.txt not found{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[*] Creating example targets.txt{Style.RESET_ALL}")
            with open("targets.txt", "w") as f:
                f.write("# Add Roblox User IDs here, one per line\n")
                f.write("123456789\n")
            targets = ["123456789"]
        return targets
    
    def ensure_accounts(self):
        if len(self.rotator.accounts) == 0:
            print(f"{Fore.YELLOW}[!] No accounts found. Creating accounts automatically...{Style.RESET_ALL}")
            count = Config.ACCOUNTS_TO_CREATE
            print(f"{Fore.CYAN}[*] Creating {count} accounts (this takes a few minutes)...{Style.RESET_ALL}")
            self.account_creator.create_bulk(count)
            self.rotator = AccountRotator()
            print(f"{Fore.GREEN}[+] Accounts created and saved to accounts.txt{Style.RESET_ALL}")
    
    def worker(self, worker_id):
        print(f"{Fore.CYAN}[*] Worker {worker_id} started{Style.RESET_ALL}")
        
        while self.running:
            try:
                account = self.rotator.get_next_account()
                if not account:
                    time.sleep(5)
                    continue
                
                captcha_solver = FreeCaptchaSolver()
                
                auth = RobloxAuth()
                if not auth.login(account['email'], account['password']):
                    self.rotator.set_cooldown(account, 300)
                    continue
                
                reporter = RobloxReporter(auth, captcha_solver)
                
                reports_per_account = 0
                max_reports = Config.ACCOUNT_SWITCH_INTERVAL
                
                for target_id in self.targets:
                    if reports_per_account >= max_reports:
                        break
                    
                    daily_key = f"{target_id}_{datetime.now().strftime('%Y%m%d')}"
                    with self.stats_lock:
                        if self.stats["daily_target_count"].get(daily_key, 0) >= 10:
                            print(f"{Fore.YELLOW}[*] Daily limit reached for target {target_id}{Style.RESET_ALL}")
                            continue
                    
                    delay = random.uniform(Config.MIN_DELAY, Config.MAX_DELAY)
                    print(f"{Fore.CYAN}[*] Waiting {delay:.1f} seconds before next report...{Style.RESET_ALL}")
                    time.sleep(delay)
                    
                    success = reporter.report_user(target_id)
                    
                    with self.stats_lock:
                        self.stats["total_reports"] += 1
                        if success:
                            self.stats["successful"] += 1
                            reports_per_account += 1
                            self.stats["daily_target_count"][daily_key] = self.stats["daily_target_count"].get(daily_key, 0) + 1
                            self.rotator.increment_reports(account)
                        else:
                            self.stats["failed"] += 1
                
                with self.stats_lock:
                    self.stats["accounts_used"] += 1
                
                cooldown = random.randint(180, 300)
                self.rotator.set_cooldown(account, cooldown)
                
                captcha_solver.close()
                
                if random.random() < 0.3:
                    extra_pause = random.randint(30, 120)
                    print(f"{Fore.YELLOW}[*] Taking strategic pause: {extra_pause}s{Style.RESET_ALL}")
                    time.sleep(extra_pause)
                
            except Exception as e:
                print(f"{Fore.RED}[!] Worker {worker_id} error: {e}{Style.RESET_ALL}")
                time.sleep(10)
    
    def stats_printer(self):
        while self.running:
            time.sleep(30)
            elapsed = time.time() - self.stats["start_time"]
            rate = self.stats["total_reports"] / (elapsed / 60) if elapsed > 0 else 0
            
            print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[STATS] {datetime.now().strftime('%H:%M:%S')}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[STATS] Runtime: {elapsed/60:.1f} minutes{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[STATS] Total reports: {self.stats['total_reports']}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[STATS] Successful: {self.stats['successful']}{Style.RESET_ALL}")
            print(f"{Fore.RED}[STATS] Failed: {self.stats['failed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[STATS] Accounts used: {self.stats['accounts_used']}{Style.RESET_ALL}")
            print(f"{Fore.RED}[STATS] Accounts banned: {self.stats['accounts_banned']}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}[STATS] Rate: {rate:.1f} reports/min{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    def run(self):
        self.ensure_accounts()
        
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] OPTIMIZED FREE Roblox Bulk Reporter{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Targets: {len(self.targets)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Workers: {Config.MAX_WORKERS}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Accounts: {len(self.rotator.accounts)}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Cost: $0.00 (completely free){Style.RESET_ALL}")
        print(f"{Fore.GREEN}[+] Browser: Fresh Chrome instance per account{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        startup_delay = random.randint(0, 10)
        print(f"{Fore.CYAN}[*] Starting in {startup_delay} seconds...{Style.RESET_ALL}")
        time.sleep(startup_delay)
        
        threads = []
        
        for i in range(Config.MAX_WORKERS):
            t = threading.Thread(target=self.worker, args=(i+1,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        stats_thread = threading.Thread(target=self.stats_printer)
        stats_thread.daemon = True
        stats_thread.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Shutting down gracefully...{Style.RESET_ALL}")
            self.running = False
            sys.exit(0)

if __name__ == "__main__":
    reporter = FreeBulkReporter()
    reporter.run()
