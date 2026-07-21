import random

class Config:
    ROBLOX_API_BASE = "https://api.roblox.com"
    ROBLOX_AUTH_URL = "https://auth.roblox.com/v2/login"
    ROBLOX_REPORT_URL = "https://www.roblox.com/report/request"
    ROBLOX_CSRF_URL = "https://auth.roblox.com/v2/logout"
    ROBLOX_SIGNUP_URL = "https://www.roblox.com/account/signup"
    
    MAX_WORKERS = 2
    MIN_DELAY = 10
    MAX_DELAY = 25
    ACCOUNT_SWITCH_INTERVAL = 3
    MAX_REPORTS_PER_TARGET_PER_DAY = 10
    
    AUTO_CREATE_ACCOUNTS = True
    ACCOUNTS_TO_CREATE = 10
    
    CAPTCHA_METHOD = "browser"
    HEADLESS_MODE = False
    
    @staticmethod
    def get_strategic_delay():
        hour = random.randint(0, 23)
        if 2 <= hour <= 5:
            return random.uniform(8, 15)
        elif 10 <= hour <= 14:
            return random.uniform(15, 30)
        else:
            return random.uniform(10, 25)
