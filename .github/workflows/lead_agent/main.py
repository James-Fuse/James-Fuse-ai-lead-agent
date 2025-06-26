from lead_agent.ted_scraper import search_ted
from lead_agent.bund_scraper import search_bund
from lead_agent.kleinanzeigen_checker import search_kleinanzeigen
from lead_agent.website_crawler import crawl_industry_websites
from lead_agent.email_reporter import send_email_report

def main():
    print("🔎 Running lead search agent...")

    ted_results = search_ted()
    bund_results = search_bund()
    kleinanzeigen_results = search_kleinanzeigen()
    website_results = crawl_industry_websites()

    all_results = ted_results + bund_results + kleinanzeigen_results + website_results

    print(f"📦 Total leads found: {len(all_results)}")
    send_email_report(all_results)

if __name__ == "__main__":
    main()
