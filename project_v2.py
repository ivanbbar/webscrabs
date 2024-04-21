import pandas as pd
from playwright.sync_api import sync_playwright

page_url = "https://optaplayerstats.statsperform.com/en_GB/soccer/premier-league-2023-2024/1jt5mxgn4q5r6mknmlqv5qjh0/match/view/c3h42njfgxs5smffn86jc6kno/match-summary"

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

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path="/usr/bin/google-chrome", headless=False)
        page = browser.new_page()
        page.goto(page_url)
        data_dict = scrape_stats(page)
        browser.close()

    df = pd.DataFrame(data_dict)
    
    # Extract Player column
    player_col = df.pop('Player')
    
    # Insert Player column at the beginning
    df.insert(0, 'Player', player_col)
    
    print(df)

if __name__ == "__main__":
    main()
