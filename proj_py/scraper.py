import json
import random
import time
from itertools import product
from typing import List, Dict, Any

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

from config import USER_AGENTS, DESIRED_PARAM_IDS, DROPDOWN_ORDER, PROGRESS_FILE

class BMWScraper:
    def __init__(self):
        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def get_driver(self) -> webdriver.Chrome:
        """Initialize and return a configured Chrome driver."""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        ua = random.choice(USER_AGENTS)
        chrome_options.add_argument(f"user-agent={ua}")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.page_load_strategy = "normal"
        
        driver = webdriver.Chrome(service=self.service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(10)
        return driver

    def handle_cookie_consent(self) -> bool:
        """Handle cookie consent popup."""
        js_find_and_click_cookie = """
            function findAndClickAccept(node) {
                if (!node) return false;
                if ((node.tagName === 'BUTTON' || node.tagName === 'SPAN') && 
                    node.innerText.includes("Alle akzeptieren")) {
                    node.click();
                    return true;
                }
                if (node.shadowRoot) {
                    const found = findAndClickAccept(node.shadowRoot);
                    if (found) return true;
                }
                for (const child of node.children || []) {
                    const found = findAndClickAccept(child);
                    if (found) return true;
                }
                return false;
            }
            return findAndClickAccept(document.body);
        """
        return self.driver.execute_script(js_find_and_click_cookie)

    def get_car_links(self) -> List[str]:
        """Get all car configuration URLs from the main page."""
        js_script = """
            function deepQuerySelectorAll(selector) {
                const results = [];
                function traverse(node) {
                    if (node.shadowRoot) {
                        traverse(node.shadowRoot);
                    }
                    const elements = node.querySelectorAll(selector);
                    if (elements.length) {
                        elements.forEach(el => results.push(el));
                    }
                    node.children && [...node.children].forEach(traverse);
                }
                traverse(document);
                return results;
            }
            return deepQuerySelectorAll("a.cmp-allmodelscard__link").map(a => a.href);
        """
        return list(set(self.driver.execute_script(js_script)))

    def load_progress(self) -> Dict[str, int]:
        """Load saved progress from file."""
        try:
            with open(PROGRESS_FILE, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"last_processed_index": 0}

    def save_progress(self, progress_data: Dict[str, int]) -> None:
        """Save current progress to file."""
        with open(PROGRESS_FILE, "w") as file:
            json.dump(progress_data, file)

    def extract_model_data(self, url: str) -> List[Dict[str, Any]]:
        """Extract data for a specific model configuration."""
        self.driver = self.get_driver()
        self.driver.get(url)
        time.sleep(2)

        if self.handle_cookie_consent():
            print("✅ 'Alle akzeptieren' button clicked.")
        else:
            print("❌ Could not find 'Alle akzeptieren' button.")

        time.sleep(3)
        
        # Get model name
        body = self.driver.find_element(By.TAG_NAME, "body")
        all_text = body.text
        lines = [line.strip() for line in all_text.strip().splitlines() if line.strip()]
        model_name = next((line for line in lines if "BMW" in line), "Unknown")

        # Click "Finanzieren & Leasen" button
        js_find_and_click = """
            function findAndClickButton(node) {
                if (!node) return null;
                if (node.tagName === "BUTTON" && node.innerText.includes("Finanzieren & Leasen")) {
                    node.click();
                    return true;
                }
                if (node.shadowRoot) {
                    let found = findAndClickButton(node.shadowRoot);
                    if (found) return true;
                }
                for (const child of node.children || []) {
                    let found = findAndClickButton(child);
                    if (found) return true;
                }
                return false;
            }
            return findAndClickButton(document.body);
        """
        
        if self.driver.execute_script(js_find_and_click):
            print("✅ Button clicked successfully!")
        else:
            print("❌ Button not found!")
            
        time.sleep(2)

        # Get all configuration options
        results = self.driver.execute_async_script("""
            const done = arguments[0];
            function findElementByAriaLabel(root, label) {
                if (!root) return null;
                if (root.getAttribute && root.getAttribute("aria-label") === label) return root;
                if (root.shadowRoot) {
                    const result = findElementByAriaLabel(root.shadowRoot, label);
                    if (result) return result;
                }
                for (const child of root.children || []) {
                    const result = findElementByAriaLabel(child, label);
                    if (result) return result;
                }
                return null;
            }
            async function selectAllOptions() {
                const select = findElementByAriaLabel(document.body, "Weitere Finanzierungs- und Leasingbeispiele:");
                if (!select) {
                    done({error: "Select element not found"});
                    return;
                }
                const results = [];
                for (let i = 0; i < select.options.length; i++) {
                    select.selectedIndex = i;
                    select.dispatchEvent(new Event("input", { bubbles: true }));
                    select.dispatchEvent(new Event("change", { bubbles: true }));
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    results.push({
                        index: i,
                        optionText: select.options[i].textContent.trim(),
                        optionValue: select.options[i].value
                    });
                }
                done(results);
            }
            selectAllOptions();
        """)

        if isinstance(results, dict) and "error" in results:
            print("Error:", results["error"])
            return []

        # Process each configuration
        data_rows = []
        for config_group in results:
            # ... (rest of the data collection logic)
            # This part would be similar to your original code, but organized in methods
            pass

        self.driver.quit()
        return data_rows

    def run(self):
        """Main execution method."""
        self.driver = self.get_driver()
        self.driver.get("https://www.bmw.de/de/konfigurator.html")
        time.sleep(2)

        car_links = self.get_car_links()
        self.driver.quit()

        progress = self.load_progress()
        start_index = progress["last_processed_index"]

        for url in car_links[start_index:]:
            data_rows = self.extract_model_data(url)
            
            if data_rows:
                df = pd.DataFrame(data_rows)
                df['Country'] = 'Germany'
                df['Model_Name'] = df['Model'].str.split(' - Option').str[0]
                df['URL'] = url
                
                columns = ["Country", "Model_Name", "URL"] + [col for col in df.columns 
                            if col not in ("Country", "Model_Name", "URL")]
                df = df[columns]
                
                model_name = df['Model_Name'].iloc[0]
                df.to_csv(f'output/bmw/batch_2/{model_name}.csv', index=False)

                progress["last_processed_index"] = car_links.index(url) + 1
                self.save_progress(progress) 