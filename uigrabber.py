from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
import time

print(">> Launching browser...")

# Setup Selenium driver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print(">> Loading login page...")
driver.get("https://pocketoption.com/en/login/")

print(">> Filling credentials...")
WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("erikrbohl@gmail.com")
driver.find_element(By.NAME, "password").send_keys("LemUroNimAko24")

# 👇 Optional: click "Sign In" manually if CAPTCHA involved
input(">> Press [Enter] after logging in manually and landing on the dashboard...")

print(">> Extracting session token from localStorage...")

# Inject JS to pull all localStorage items
session_data = driver.execute_script("""
    let data = {};
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        data[key] = localStorage.getItem(key);
    }
    return data;
""")

# Save to JSON
with open("session_data.json", "w") as f:
    json.dump(session_data, f, indent=4)
print("✅ session_data.json created.")

# Save to .env format
with open(".env", "w") as f:
    for k, v in session_data.items():
        f.write(f"{k.upper()}={v}\n")
print("✅ .env file created.")

driver.quit()
print("🧠 Session grab complete.")
