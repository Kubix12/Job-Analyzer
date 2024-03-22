from bs4 import BeautifulSoup
import requests


def get_offer(url_page, scrapper_offers):
    page = requests.get(url_page)
    soup = BeautifulSoup(page.content, 'html.parser')

    job_list = soup.find_all('div', class_='css-2crog7')[:scrapper_offers]

    job_offers = []  # List to store multiple job offers

    for job in job_list:
        job_link = job.find("a", class_="offer_list_offer_link css-4lqp8g")
        href = job_link.get('href')
        if href:
            full_url = url_page + href
            single_job_page = requests.get(full_url)
            single_job_soup = BeautifulSoup(single_job_page.content, 'html.parser')

            offer_data = {}  # Dictionary to store data for a single job offer

            # Extracting title from job page
            title = single_job_soup.find("div", class_="css-vb54bv")
            if title:
                h1_tag = title.find('h1')
                offer_data['title'] = h1_tag.get_text(strip=True)

            # Extracting company from job page
            company = single_job_soup.find('div', class_='css-mbkv7r')
            offer_data['company'] = company.get_text(strip=True) if company else "No company found"

            # Extracting type of work, experience, employment type, operating mode
            description_work = {}
            type_work = single_job_soup.find_all("div", class_="css-6q28fo")
            for data in type_work:
                description = data.find('div', class_="css-qyml61").text
                rest = data.find('div', class_="css-15wyzmd").text
                description_work[description] = rest
            offer_data['description'] = description_work

            # Extracting stack
            stack_list = {}
            stack_description = single_job_soup.find_all("div", class_="css-cjymd2")
            for stack in stack_description:
                technology = stack.find("h6", class_="MuiTypography-root MuiTypography-subtitle2 css-x1xnx3").text
                technology_level = stack.find('span',
                                              class_="MuiTypography-root MuiTypography-subtitle4 css-1wcj8lw").text

                stack_list[technology] = technology_level
            offer_data['stack'] = stack_list

        # Extracting earnings from job page
        job_earnings = job.find('div', class_='css-17pspck')
        if job_earnings:
            span_text = job_earnings.find_all('span')
            if len(span_text) >= 2:
                first_text = span_text[0].get_text(strip=True)
                second_text = span_text[1].get_text(strip=True)
                offer_data['earnings'] = [first_text, second_text]
            else:
                offer_data['earnings'] = 'Undisclosed salary'
        else:
            offer_data['earnings'] = 'Undisclosed salary'

        job_offers.append(offer_data)

    return job_offers
