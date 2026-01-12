import csv
import time
import os
from playwright.sync_api import sync_playwright

def scrape_league():
    # This line ensures the CSV is saved in the same folder as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'league_roster.csv')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Replace with URL
        page.goto("https://vdc.gg/player")
        
        print("\n--- ACTION REQUIRED ---")
        print("1. Complete any Cloudflare/Human verification in the browser.")
        print("2. Once you see the player grid, return here and press ENTER.")
        input("Press Enter to start auto-loading players...")

        # --- AUTO-LOAD ALL PLAYERS ---
        print("Expanding the list... please stay on the browser tab.")
        while True:
            # Targets the 'Load more' button
            load_more_btn = page.locator("button.bg-vdcRed:has-text('Load more')")
            
            if load_more_btn.is_visible():
                load_more_btn.click()
                time.sleep(1.5) # Wait for content to load
            else:
                print("All players loaded or 'Load more' button is gone.")
                break

        # --- DATA EXTRACTION ---
        print("Extracting player data...")
        player_cards = page.query_selector_all("a.flex.relative.flex-row")
        
        scraped_data = []

        for card in player_cards:
            try:
                # Username
                username_el = card.query_selector("div.text-right.truncate h1:first-child")
                username = username_el.inner_text().strip() if username_el else ""

                # Tier
                tier_el = card.query_selector("div.flex-1 h1:nth-of-type(2)")
                tier = tier_el.inner_text().strip() if tier_el else ""

                # MMR
                mmr_el = card.query_selector("div.text-right.truncate h1:has-text('MMR:')")
                mmr_raw = mmr_el.inner_text() if mmr_el else ""
                
                # Cleaning MMR: Remove "MMR:", quotes, and newlines
                mmr_value = mmr_raw.replace("MMR:", "").replace('"', '').replace("\n", "").strip()

                # Filter: Only keep if they have a valid Username and MMR
                if tier and mmr_value and "#" in username:
                    scraped_data.append({
                        "Username": username,
                        "Tier": tier,
                        "MMR": mmr_value
                    })
            except Exception:
                continue

        # --- SAVE TO CSV ---
        if scraped_data:
            keys = ["Username", "Tier", "MMR"]
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(scraped_data)
            print(f"\nSuccess! File saved at: {csv_path}")
            print(f"Total players captured: {len(scraped_data)}")
        else:
            print("\nNo data found. Check your selectors or ensure the page loaded correctly.")

        browser.close()

if __name__ == "__main__":
    scrape_league()

# Last updated 2026-01-10
