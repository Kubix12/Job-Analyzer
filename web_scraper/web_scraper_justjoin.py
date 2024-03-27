from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import NoSuchElementException

logging.basicConfig(level=logging.INFO)


def get_offer(page_url, scrapper_job_offers):
    job_offers = []  # List to store multiple job offers

    try:
        driver = webdriver.Edge()
        driver.set_window_size(1200, 800)
        driver.get(page_url)

        offers_fetched = 0

        while offers_fetched < scrapper_job_offers:
            WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-2crog7')))

            # Find all job offers on the page
            job_offers_list = driver.find_elements(By.CLASS_NAME, 'css-2crog7')[:scrapper_job_offers]

            for job in job_offers_list:
                if offers_fetched >= scrapper_job_offers:
                    break

                job_link = job.find_element(By.CLASS_NAME, "offer_list_offer_link.css-4lqp8g")
                href = job_link.get_attribute('href')
                if href:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(href)

                    offer_data = {}  # Dictionary to store data for a single job offer

                    # Extract title from job page
                    title = driver.find_element(By.CLASS_NAME, "css-vb54bv")
                    offer_data['title'] = title.find_element(By.TAG_NAME, 'h1').text.strip()

                    # Extract company from job page
                    company = driver.find_element(By.CLASS_NAME, 'css-mbkv7r')
                    offer_data['company'] = company.text.strip() if company else "Company not found"

                    time.sleep(2)

                    # Extract type of work, experience, employment type, operating mode
                    description_job_offer = {}
                    type_work_elements = driver.find_elements(By.CSS_SELECTOR, '.css-6q28fo')
                    for data in type_work_elements:
                        try:
                            description = data.find_element(By.CSS_SELECTOR, '.css-qyml61').text
                            rest = data.find_element(By.CSS_SELECTOR, '.css-15wyzmd').text
                            description_job_offer[description] = rest

                        except Exception as e:
                            logging.error(f"An error occurred while extracting type of work data: {e}")

                    offer_data['description'] = description_job_offer

                    # Extract stack from job page
                    stack_list = {}
                    stack_description = driver.find_elements(By.CLASS_NAME, 'css-cjymd2')
                    for stack in stack_description:
                        technology = stack.find_element(By.TAG_NAME, 'h6').text
                        technology_level = stack.find_element(By.TAG_NAME, 'span').text

                        stack_list[technology] = technology_level
                    offer_data['stack'] = stack_list

                    # Extract earnings from job page
                    try:
                        job_earnings = driver.find_element(By.CLASS_NAME, 'css-j7qwjs')

                        span_elements = job_earnings.find_elements(By.TAG_NAME, 'span')

                        if span_elements:
                            first_salary = span_elements[1].text.strip()
                            second_salary = span_elements[2].text.strip()
                            offer_data['earnings'] = [first_salary, second_salary]
                        else:
                            offer_data['earnings'] = ['Undisclosed salary', 'Undisclosed salary']

                    except NoSuchElementException:
                        offer_data['earnings'] = ['Undisclosed salary', 'Undisclosed salary']

                    job_offers.append(offer_data)
                    offers_fetched += 1
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            if offers_fetched < scrapper_job_offers:
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()

    return job_offers
