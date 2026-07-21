import time
import random
import tempfile
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore, Style
from config import Config

class FreeCaptchaSolver:
    def __init__(self):
        self.driver = None
        self.solved_count = 0
    
    def _init_driver(self):
        options = uc.ChromeOptions()
        
        if Config.HEADLESS_MODE:
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        
        width = random.randint(1200, 1400)
        height = random.randint(800, 900)
        options.add_argument(f'--window-size={width},{height}')
        
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-sync')
        options.add_argument('--incognito')
        
        temp_dir = tempfile.mkdtemp()
        options.add_argument(f'--user-data-dir={temp_dir}')
        
        self.driver = uc.Chrome(options=options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.driver.set_window_size(width, height)
        
        print(f"{Fore.CYAN}[*] Fresh browser instance created (window: {width}x{height}){Style.RESET_ALL}")
    
    def solve_captcha_automatically(self, page_url="https://www.roblox.com"):
        try:
            if not self.driver:
                self._init_driver()
            
            time.sleep(random.uniform(0.5, 1.5))
            self.driver.get(page_url)
            
            action = ActionChains(self.driver)
            action.move_by_offset(random.randint(100, 500), random.randint(100, 500))
            action.perform()
            
            time.sleep(random.uniform(2, 4))
            
            try:
                iframe_selectors = [
                    "iframe[src*='recaptcha']",
                    "iframe[title='reCAPTCHA']",
                    "iframe[src*='google.com/recaptcha']"
                ]
                
                iframe = None
                for selector in iframe_selectors:
                    try:
                        iframe = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if iframe:
                            break
                    except:
                        continue
                
                if not iframe:
                    print(f"{Fore.YELLOW}[*] No CAPTCHA iframe found{Style.RESET_ALL}")
                    return None
                
                self.driver.switch_to.frame(iframe)
                time.sleep(random.uniform(0.5, 1))
                
                checkbox = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "recaptcha-checkbox-border"))
                )
                
                action = ActionChains(self.driver)
                action.move_to_element(checkbox)
                action.pause(random.uniform(0.3, 0.8))
                action.click()
                action.perform()
                
                time.sleep(random.uniform(3, 6))
                
                self.driver.switch_to.default_content()
                
                token = self.driver.execute_script("""
                    return document.getElementById('g-recaptcha-response')?.value || 
                           document.querySelector('[name="g-recaptcha-response"]')?.value || 
                           '';
                """)
                
                if token:
                    self.solved_count += 1
                    print(f"{Fore.GREEN}[+] CAPTCHA solved automatically (#{self.solved_count}){Style.RESET_ALL}")
                    return token
                else:
                    print(f"{Fore.YELLOW}[*] CAPTCHA not solved automatically{Style.RESET_ALL}")
                    return None
                    
            except Exception as e:
                print(f"{Fore.YELLOW}[*] CAPTCHA interaction error: {e}{Style.RESET_ALL}")
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[!] Browser error: {e}{Style.RESET_ALL}")
            return None
    
    def solve(self):
        token = self.solve_captcha_automatically()
        
        if token:
            return token
        
        print(f"{Fore.YELLOW}[!] Opening browser for manual CAPTCHA solving...{Style.RESET_ALL}")
        
        if not self.driver:
            self._init_driver()
        
        self.driver.get("https://www.google.com/recaptcha/api2/demo")
        print(f"{Fore.CYAN}[*] Please solve the CAPTCHA in the browser window{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Waiting up to 60 seconds...{Style.RESET_ALL}")
        
        for _ in range(30):
            time.sleep(2)
            token = self.driver.execute_script("""
                return document.getElementById('g-recaptcha-response')?.value || '';
            """)
            if token:
                self.solved_count += 1
                print(f"{Fore.GREEN}[+] Manual CAPTCHA solved (#{self.solved_count}){Style.RESET_ALL}")
                return token
        
        print(f"{Fore.RED}[!] Manual CAPTCHA solving timeout{Style.RESET_ALL}")
        return None
    
    def close(self):
        if self.driver:
            try:
                self.driver.quit()
                print(f"{Fore.CYAN}[*] Browser closed{Style.RESET_ALL}")
            except:
                pass
            self.driver = None
