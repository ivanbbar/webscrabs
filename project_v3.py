import pandas as pd
from playwright.sync_api import sync_playwright
import time

def get_match_page_hrefs(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False)
        page = browser.new_page()

        try:
            page.goto(page_url)
            page.wait_for_load_state("networkidle")

            match_page_hrefs = page.query_selector_all("a.Opta-MatchLink")
            hrefs = []
            if match_page_hrefs:
                for match_page_href in match_page_hrefs:
                    hrefs.append(match_page_href.get_attribute("href"))
            else:
                print("No Match Page hrefs found.")
            return hrefs

        except Exception as e:
            print("Error:", e)

        finally:
            browser.close()

def scrape_stats(page):
    headers = page.query_selector_all('.Opta-Player-Stats th.Opta-Stat abbr')
    header_names = [header.inner_text() for header in headers]

    rows = page.query_selector_all('tbody tr')
    data_dict = {header_name: [] for header_name in header_names}
    data_dict['Player'] = []
    for row in rows:
        player_name_element = row.query_selector('th.Opta-Player')
        if player_name_element:
            player_name = player_name_element.inner_text()
            if player_name != 'Total':
                stats = [cell.inner_text() for cell in row.query_selector_all('.Opta-Stat')]
                data_dict['Player'].append(player_name)
                for header_name, stat in zip(header_names, stats):
                    data_dict[header_name].append(stat)
    return data_dict

def process_page(page_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False)
        page = browser.new_page()
        page.goto(page_url)
        time.sleep(5)
        data_dict = scrape_stats(page)
        browser.close()

    df = pd.DataFrame(data_dict)
    player_col = df.pop('Player')
    df.insert(0, 'Player', player_col)
    n_rows = len(df)
    df = df.head(n_rows // 2)
    return df

def main():
    page_url_1 = "https://optaplayerstats.statsperform.com/en_GB/soccer/premier-league-2023-2024/1jt5mxgn4q5r6mknmlqv5qjh0/results"
    hrefs = get_match_page_hrefs(page_url_1)

    for idx, href in enumerate(hrefs, start=1):
        print(f"Processing {href}...")
        df = process_page(href)
        if len(df) > 21:
            csv_filename = f"match_{idx}_stats.csv"
            df.to_csv(csv_filename)
            print("Ok")
        else:
            print("Skipped - Number of rows in DataFrame is not the minimum.")

if __name__ == "__main__":
    main()
