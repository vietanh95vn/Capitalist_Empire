import sqlite3
import os
import html
from datetime import datetime
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# --- SECURITY PERIMETER ---
load_dotenv()

# ==========================================
# MODULE 1: THE EXTRACTOR (Playwright DOM Parsing)
# ==========================================
class CrawlData:
    def __init__(self):
        self.target_url = "https://weworkremotely.com/categories/remote-back-end-programming-jobs"
        self.base_url = "https://weworkremotely.com"

    def fetch_jobs(self):
        print(f"[{datetime.now().isoformat()}] 🤖 Initiating Playwright Extraction Sequence...")
        extracted_jobs = []

        with sync_playwright() as p:
            # Emulate real user constraints to avoid immediate WAF blocks
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            try:
                # 1. Direct Access & Dom Content Validation
                page.goto(self.target_url, timeout=30000, wait_until="domcontentloaded")
                
                # Wait for the main container to ensure the DOM is painted
                page.wait_for_selector('#job_list', timeout=15000)

                # 2. Node Traversal (Targeting specific list items)
                # We target all <li> inside the article, but will filter out empty/divider elements
                job_nodes = page.locator('article ul li').element_handles()

                for node in job_nodes:
                    # 2. Use the exact BEM classes you discovered
                    title_el = node.query_selector('.new-listing__header__title')
                    if not title_el:
                        continue 

                    try:
                        title = title_el.inner_text().strip()
                        
                        company_el = node.query_selector('.new-listing__company-name')
                        company = company_el.inner_text().strip() if company_el else "Unknown Company"
                        
                        region_el = node.query_selector('.new-listing__categories')
                        location = region_el.inner_text().strip() if region_el else "Anywhere"

                        # Extract URL & Sanitize Path
                        link_el = node.query_selector('.listing-link--unlocked') or node.query_selector('a')
                        raw_href = link_el.get_attribute('href') if link_el else ""
                        full_url = urljoin(self.base_url, raw_href)

                        # Generate Unique ID from URL slug
                        job_id = raw_href.split('/')[-1] if raw_href else str(len(extracted_jobs))

                        extracted_jobs.append((job_id, title, company, location, full_url, datetime.now().isoformat()))
                    
                    except Exception as parse_error:
                        print(f"⚠️ [NODE EXTRACTION FAILURE]: Skipped corrupted DOM node. Err: {parse_error}")
                        continue

            except PlaywrightTimeoutError:
                print("❌ [CRITICAL TIMEOUT]: WAF Blocked access or target server is unresponsive.")
            except Exception as e:
                print(f"❌ [PLAYWRIGHT ENGINE CRASH]: {e}")
            finally:
                browser.close()

        return extracted_jobs

# ==========================================
# MODULE 2: THE VAULT (Persistence & Business Logic)
# ==========================================
class SaveData:
    def __init__(self, db_name="wwr_jobs.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            url TEXT,
            timestamp TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_bulk_data(self, records):
        if not records:
            return 0
        # Idempotency constraint: INSERT OR IGNORE
        query = "INSERT OR IGNORE INTO jobs (id, title, company, location, url, timestamp) VALUES (?, ?, ?, ?, ?, ?)"
        try:
            cursor = self.conn.executemany(query, records)
            self.conn.commit()
            return cursor.rowcount  # Returns the number of NEW rows inserted
        except sqlite3.Error as e:
            print(f"❌ [SQL CRASH]: Database write failure: {e}")
            return 0

    def filter_target_jobs(self, records):
        """BUSINESS LOGIC: Orchestrator's condition -> Title contains 'python' or 'data'"""
        target_jobs = []
        for record in records:
            title = record[1].lower() # record[1] is the title in the tuple
            if "senior" in title or "engineer" in title:
                target_jobs.append(record)
        return target_jobs

# ==========================================
# MODULE 3: THE MESSENGER (Telemetry & Alerts)
# ==========================================
class TelegramNotice:
    def __init__(self):
        self.token = os.getenv("TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        
        if not self.token or not self.chat_id:
            print("❌ [SECURITY ALERT]: TOKEN or CHAT_ID missing from environment!")

    def send_report(self, message):
        if not self.token: return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
        try:
            # The Kill-Switch is engaged
            res = requests.post(url, json=payload, timeout=10)
            res.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print("❌ [TELEGRAM CRASH]: Network failure or API rejection.")
            if hasattr(e, 'response') and e.response is not None:
                print(f"🔍 [CORE ERROR]: {e.response.text}")
            return False

# ==========================================
# THE ORCHESTRATOR (MAIN ENGINE EXECUTION)
# ==========================================
import time
from datetime import datetime

# ... [GIỮ NGUYÊN CÁC CLASS CrawlData, SaveData, TelegramNotice CỦA CẬU Ở TRÊN] ...

# ==========================================
# THE ORCHESTRATOR (CONTINUOUS WORKER ENGINE)
# ==========================================
if __name__ == "__main__":
    crawler = CrawlData()
    vault = SaveData()
    notifier = TelegramNotice()

    print(f"🚀 [WORKER INIT] Continuous Ingestion Engine Started. Interval: 60 Minutes.")

    # The Infinite Enterprise Loop
    while True:
        try:
            print(f"\n[{datetime.now().isoformat()}] 🔄 Waking up to execute Ingestion Cycle...")
            
            # 1. Extraction Phase
            scraped_data = crawler.fetch_jobs()
            print(f"✅ Extracted {len(scraped_data)} jobs from the DOM.")

            # 2. Filtering Phase
            matched_jobs = vault.filter_target_jobs(scraped_data)
            print(f"🎯 Found {len(matched_jobs)} target jobs.")

            if not matched_jobs:
                print("💤 No target jobs found. Cycle complete.")
            else:
                # 3. Persistence Phase
                new_records_count = vault.save_bulk_data(matched_jobs)
                
                if new_records_count == 0:
                    print("💤 Jobs match criteria, but already exist in DB. System silenced.")
                else:
                    print(f"✅ Persisted {new_records_count} NEW target jobs.")
                    
                    # 4. Telemetry Phase
                    alert_items = []
                    for job in matched_jobs:
                        import html # Đảm bảo html được import
                        safe_title = html.escape(job[1])
                        safe_company = html.escape(job[2])
                        safe_loc = html.escape(job[3])
                        safe_url = html.escape(job[4])
                        
                        alert_items.append(
                            f"🏢 <b>{safe_company}</b>\n"
                            f"💼 {safe_title}\n"
                            f"🌍 {safe_loc}\n"
                            f"🔗 <a href=\"{safe_url}\">Apply Here</a>\n"
                        )

                    chunk_size = 5
                    for i in range(0, len(alert_items), chunk_size):
                        chunk = alert_items[i:i + chunk_size]
                        msg = f"🔥 <b>WWR JOB ALERT (PYTHON/DATA)</b> 🔥\n\n" + "\n".join(chunk)
                        
                        if notifier.send_report(msg):
                            print(f"✅ Telemetry Payload {i//chunk_size + 1} delivered.")
                        else:
                            print("❌ [TELEGRAM ERROR] Payload delivery failed.")
                            break
                            
        except Exception as critical_error:
            # FAIL-SAFE: Bẫy lỗi tối hậu. Không bao giờ để vòng lặp bị phá vỡ.
            print(f"❌ [CRITICAL ENGINE FAILURE]: Ingestion Cycle crashed. Error: {critical_error}")
            print("⚠️ System will attempt recovery in the next cycle.")
        
        # The Sleep Protocol (3600 seconds = 1 hour)
        print(f"⏳ Cycle finished. Engine going into Hibernation Mode for 60 minutes...")
        time.sleep(3600)