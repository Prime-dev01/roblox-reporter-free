import random
import time
from datetime import datetime
from colorama import Fore, Style
from config import Config

class RobloxReporter:
    def __init__(self, auth, captcha_solver):
        self.auth = auth
        self.captcha_solver = captcha_solver
        self.session = auth.session
        
        self.report_reasons = [
            "Harassment",
            "Scamming", 
            "Exploiting",
            "Inappropriate Content",
            "Bullying",
            "Discrimination",
            "Impersonation",
            "Spam",
            "Offensive Language",
            "Threats"
        ]
        
        self.evidence_templates = [
            "User is violating Roblox Community Standards through repeated harassment.",
            "This user is engaging in scamming activities and stealing from other players.",
            "User is using exploits and cheats to gain unfair advantage.",
            "User is posting inappropriate content in public spaces.",
            "This user is bullying other players in-game and in chat.",
            "User is making discriminatory comments against other players.",
            "This user is impersonating a Roblox staff member or another player.",
            "User is sending spam messages to multiple players."
        ]
    
    def report_user(self, user_id):
        try:
            auth_token = self.auth.get_authenticity_token()
            if not auth_token:
                print(f"{Fore.RED}[!] Failed to get authenticity token{Style.RESET_ALL}")
                return False
            
            captcha_token = self.captcha_solver.solve()
            if not captcha_token:
                print(f"{Fore.RED}[!] Failed to solve CAPTCHA{Style.RESET_ALL}")
                return False
            
            reason = random.choice(self.report_reasons)
            evidence = random.choice(self.evidence_templates)
            
            payload = {
                "__RequestVerificationToken": auth_token,
                "UserId": str(user_id),
                "ReportCategory": "User",
                "ReportReason": reason,
                "Evidence": evidence,
                "captchaResponse": captcha_token
            }
            
            response = self.session.post(
                Config.ROBLOX_REPORT_URL,
                data=payload,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Referer": "https://www.roblox.com/report/user"
                }
            )
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+] Report sent for user {user_id} - {reason}{Style.RESET_ALL}")
                self.log_report(user_id, reason, True)
                return True
            elif response.status_code == 429:
                print(f"{Fore.YELLOW}[*] Rate limited (429). Waiting 30 seconds...{Style.RESET_ALL}")
                time.sleep(30)
                return False
            else:
                print(f"{Fore.RED}[!] Report failed for user {user_id}: {response.status_code}{Style.RESET_ALL}")
                self.log_report(user_id, reason, False)
                return False
                
        except Exception as e:
            print(f"{Fore.RED}[!] Report error: {e}{Style.RESET_ALL}")
            return False
    
    def log_report(self, user_id, reason, success):
        try:
            with open("logs/reports.log", "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                status = "SUCCESS" if success else "FAILED"
                f.write(f"[{timestamp}] {status} - User: {user_id} - Reason: {reason}\n")
        except:
            pass
