from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, tempfile

EMAIL = "erikrbohl@gmail.com"
PASSWORD = "LemUroNimAko24"

# === Chrome Setup === #
options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1280,800")
options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

try:
    # === Step 1: Login === #
    driver.get("https://pocketoption.com/en/login/")
    print(">> Loading login page...")

    # Wait for form
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "balance__value")))

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)

    # Wait for the login button to be clickable
    login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[contains(text(), "Sign in") or contains(text(), "Sign In")]')
    ))
    login_btn.click()
    print(">> Logging in...")

    # Wait until redirected to demo dashboard
    wait.until(EC.url_contains("/cabinet"))
    driver.get("https://pocketoption.com/en/cabinet/demo-trade/")
    print(">> Navigated to demo dashboard...")

    time.sleep(5)

    # === Step 2: JS Injection to extract localStorage === #
    local_storage = driver.execute_script("""
        let out = {};
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            out[key] = localStorage.getItem(key);
        }
        return out;
    """)

    print(">> LocalStorage keys extracted.")

    # === Step 3: Parse UID === #
    if "user" in local_storage:
        user_data = json.loads(local_storage["user"])
        uid = user_data.get("id")
        print(f">> UID detected: {uid}")
    else:
        print("!! User info not found in localStorage")
        uid = None

    # === Step 4: Grab session cookie === #
    cookies = driver.get_cookies()
    session_cookie = next((c["value"] for c in cookies if "session" in c["name"]), None)
    print(f">> Session cookie: {session_cookie}")

    # === Save it all === #
    with open("session_info.json", "w") as f:
        json.dump({
            "uid": uid,
            "session": session_cookie,
            "localStorage": local_storage,
            "cookies": cookies
        }, f, indent=2)

    print("✅ session_info.json saved successfully.")

finally:
    driver.quit()
