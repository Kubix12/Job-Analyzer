from bs4 import BeautifulSoup
import requests

job_offer_quantity = 1
ulr_page = "https://justjoin.it/"


def get_offer(url, offer_quantity):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    job_list = soup.find_all('div', class_='css-2crog7')[:offer_quantity]

    for job in job_list:
        job_link = job.find("a", class_="offer_list_offer_link css-4lqp8g")
        href = job_link.get('href')
        if href:
            full_url = url + href
            single_job_page = requests.get(full_url)
            single_job_soup = BeautifulSoup(single_job_page.content, 'html.parser')

            # Extracting title from job page
            title = single_job_soup.find("div", class_="css-vb54bv")
            if title:
                h1_tag = title.find('h1')
                h1_tag_text = h1_tag.get_text(strip=True)
                return h1_tag_text

            # Extracting company from job page
            company = single_job_soup.find('div', class_='css-mbkv7r')
            span_text_company = company.get_text(strip=True) if company else "No company found"

            # Extracting type of work, experience, employment type, operating mode
            description_work = {}
            type_work = single_job_soup.find_all("div", class_="css-6q28fo")
            for type in type_work:
                description = type.find('div', class_="css-qyml61").text
                rest = type.find('div', class_="css-15wyzmd").text
                description_work[description] = rest

            # Extracting stack
            stack_list = {}
            stack_description = single_job_soup.find_all("div", class_="css-cjymd2")
            for stack in stack_description:
                technology = stack.find("h6", class_="MuiTypography-root MuiTypography-subtitle2 css-x1xnx3").text
                technology_level = stack.find('span',
                                              class_="MuiTypography-root MuiTypography-subtitle4 css-1wcj8lw").text

                stack_list[technology] = technology_level

        # Extracting earnings from job page
        money = job.find('div', class_='css-17pspck')
        if money:
            span_text = money.find_all('span')
            if len(span_text) >= 2:
                first_text = span_text[0].get_text(strip=True)
                second_text = span_text[1].get_text(strip=True)
                return first_text, second_text
            else:
                return False
        else:
            return False


get_offer(ulr_page, job_offer_quantity)
