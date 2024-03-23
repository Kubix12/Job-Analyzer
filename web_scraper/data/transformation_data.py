import json


def transform_data(job: dict):
    """

    :type job: dict
    """
    title = job['title']
    company = job['company']
    type_of_work = job['description']['Type of work']
    experience = job['description']['Experience']
    employment_type = job['description']['Employment Type']
    operating_mode = job['description']['Operating mode']
    stack = json.dumps(job['stack'])
    earnings_from = job['earnings'][0]
    earnings_to = job['earnings'][1]

    return title, company, type_of_work, experience, employment_type, operating_mode, stack, earnings_from, earnings_to
