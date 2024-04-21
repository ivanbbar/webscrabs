from playwright.sync_api import sync_playwright

def run():
    page_url = "https://optaplayerstats.statsperform.com/en_GB/soccer/premier-league-2023-2024/1jt5mxgn4q5r6mknmlqv5qjh0/results"

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False)
        page = browser.new_page()

        try:
            page.goto(page_url)
            page.wait_for_load_state("networkidle")

            # Find all hrefs leading to "Match Page"
            match_page_hrefs = page.query_selector_all("a.Opta-MatchLink")
            
            if match_page_hrefs:
                print("Match Page hrefs:")
                for match_page_href in match_page_hrefs:
                    href = match_page_href.get_attribute("href")
                    print(href)
            else:
                print("No Match Page hrefs found.")

        except Exception as e:
            print("Error:", e)

        finally:
            browser.close()

if __name__ == "__main__":
    run()
