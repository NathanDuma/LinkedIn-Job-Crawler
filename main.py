import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from linkedincrawler import LinkedinCrawler
from validate_email import validate_email


def init_browser():
    browser_options = Options()
    options = ['--disable-blink-features', '--no-sandbox', '--start-maximized', '--disable-extensions',
               '--ignore-certificate-errors', '--disable-blink-features=AutomationControlled']

    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)

    driver.set_window_position(0, 0)
    driver.maximize_window()

    return driver


def validate_yaml():
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    mandatory_params = ['email', 'password', 'disableAntiLock', 'remote', 'experienceLevel', 'jobTypes', 'date',
                        'positions', 'locations', 'distance', 'outputFileDirectory']

    for mandatory_param in mandatory_params:
        if mandatory_param not in parameters:
            raise Exception(mandatory_param + ' is not inside the yml file!')

    assert validate_email(parameters['email'])
    assert len(parameters['password']) > 0

    assert isinstance(parameters['disableAntiLock'], bool)

    assert isinstance(parameters['remote'], bool)

    assert len(parameters['experienceLevel']) > 0
    experience_level = parameters.get('experienceLevel', [])
    at_least_one_experience = False
    for key in experience_level.keys():
        if experience_level[key]:
            at_least_one_experience = True
    assert at_least_one_experience

    assert len(parameters['jobTypes']) > 0
    job_types = parameters.get('jobTypes', [])
    at_least_one_job_type = False
    for key in job_types.keys():
        if job_types[key]:
            at_least_one_job_type = True
    assert at_least_one_job_type

    assert len(parameters['date']) > 0
    date = parameters.get('date', [])
    at_least_one_date = False
    for key in date.keys():
        if date[key]:
            at_least_one_date = True
    assert at_least_one_date

    approved_distances = {0, 5, 10, 25, 50, 100}
    assert parameters['distance'] in approved_distances

    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0

    return parameters


if __name__ == '__main__':
    parameters = validate_yaml()
    browser = init_browser()

    crawler = LinkedinCrawler(parameters, browser)
    crawler.login()
    crawler.security_check()
    crawler.start_scrape()




