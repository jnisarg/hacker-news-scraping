import time
import requests
from pprint import pprint
from bs4 import BeautifulSoup

crawl_delay = 30
custom_votes = 99
hn = []


def sort_links_by_points(hn_list):
    return sorted(hn_list, key=lambda k: k["points"], reverse=True)


def create_custom_hn(scraped_links, scraped_subtexts):
    for idx, item in enumerate(scraped_links):
        title = item.getText()
        href = item.get("href")
        vote = scraped_subtexts[idx].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > custom_votes:
                hn.append({
                    "title": title,
                    "link": href,
                    "points": points
                })
    return None


if __name__ == "__main__":
    while True:
        try:
            num_pages = int(input("How many pages do you want to scrape?: "))
        except (ValueError, TypeError) as err:
            print(err)
            continue
        else:
            print("Scraping... Please wait...")
            for page in range(1, num_pages+1):
                res = requests.get(f"https://news.ycombinator.com/news?p={page}")
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    links = soup.select(".storylink")
                    subtexts = soup.select(".subtext")
                    create_custom_hn(links, subtexts)
                print(f"\t {page} page/s scraped...")
                if page != num_pages:
                    print(f"\t\tApplying Crawl-Delay... of {crawl_delay}s")
                    time.sleep(crawl_delay)  # This delay is requested by hacker news
            break

    hn = sort_links_by_points(hn)
    pprint(hn)

    save = input("\nDo you want to save this data? [y|n]: ")
    if save.lower() == "y":
        with open("scraped_data.txt", "w", encoding="utf-8") as file:
            for data in hn:
                file.write(f"Title: {data['title']}\nLink: {data['link']}\nPoints: {data['points']} points\n\n")
        print("File saved...")
