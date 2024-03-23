from web_scraper.web_scraper_justjoin import get_offer
from web_scraper.data.db_offers import JobOffersDB
from web_scraper.data.transformation_data import transform_data

# Configuration variables
scrapper_offers = 1
url_page = "https://justjoin.it/"

# Database configuration
name = 'postgres'
user = 'postgres'
password = '123'
host = 'localhost'
port = '5432'
table = 'job_offers'


def main():
    job_list = get_offer(url_page, scrapper_offers)
    job_offers_db = JobOffersDB(name, user, password, host, port, table)
    for job in job_list:
        clean_data = transform_data(job)
        job_offers_db.insert_job_offer(clean_data)


if __name__ == "__main__":
    main()
