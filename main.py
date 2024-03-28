from web_scraper.web_scraper_justjoin import get_offer
from web_scraper.data.db_offers import JobOffersDB
from web_scraper.data.transformation_data import transform_data
from web_scraper.data.db_configuration import name, user, password, host, port, table

# Configuration variables
scrapper_offers = 1
url_page = "https://justjoin.it/"


def main():
    job_list = get_offer(url_page, scrapper_offers)
    job_offers_db = JobOffersDB(name, user, password, host, port, table)
    for job in job_list:
        clean_data = transform_data(job)
        job_offers_db.insert_job_offer(clean_data)


if __name__ == "__main__":
    main()
