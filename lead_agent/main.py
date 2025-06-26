from lead_agent.ted_scraper import search_ted
from lead_agent.bund_scraper import search_bund
from lead_agent.kleinanzeigen_checker import search_kleinanzeigen
from lead_agent.website_crawler import search_industrystock
from lead_agent.email_reporter import send_email

def main():
    ted_results = search_ted()
    bund_results = search_bund()
    ebay_results = search_kleinanzeigen()
    web_results = search_industrystock()

    all_leads = ted_results + bund_results + ebay_results + web_results

    if all_leads:
        send_email(all_leads)
    else:
        print("Keine Leads gefunden.")

if __name__ == "__main__":
    main()
