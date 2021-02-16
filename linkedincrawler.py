import time, random, csv, traceback, pyautogui
from selenium.common.exceptions import TimeoutException
from itertools import product


class LinkedinCrawler:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.email = parameters['email']
        self.password = parameters['password']
        self.disable_lock = parameters['disableAntiLock']
        self.company_blacklist = parameters.get('companyBlacklist', []) or []
        self.title_blacklist = parameters.get('titleBlacklist', []) or []
        self.positions = parameters.get('positions', [])
        self.locations = parameters.get('locations', [])
        self.base_search_url = self.get_base_search_url(parameters)
        self.seen_jobs = []
        self.file_name = "output"
        self.output_file_directory = parameters['outputFileDirectory']

    def login(self):
        try:
            self.browser.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(5, 10))
            self.browser.find_element_by_id("username").send_keys(self.email)
            self.browser.find_element_by_id("password").send_keys(self.password)
            self.browser.find_element_by_css_selector(".btn__primary--large").click()
            time.sleep(random.uniform(5, 10))
        except TimeoutException:
            raise Exception("Could not login!")

    def security_check(self):
        current_url = self.browser.current_url
        page_source = self.browser.page_source

        if '/checkpoint/challenge/' in current_url or 'security check' in page_source:
            input("Please complete the security check and press enter in this console when it is done.")
            time.sleep(random.uniform(5.5, 10.5))

    def start_scrape(self):
        searches = list(product(self.positions, self.locations))
        random.shuffle(searches)

        page_sleep = 0
        minimum_page_time = time.time() + 240

        for (position, location) in searches:
            location_url = "&location=" + location
            job_page_number = -1

            print("Starting the search for " + position + " in " + location + ".")

            try:
                while True:
                    page_sleep += 1
                    job_page_number += 1
                    print("Going to job page " + str(job_page_number))
                    self.next_job_page(position, location_url, job_page_number)
                    time.sleep(random.uniform(1.5, 3.5))
                    print("Starting the scraping for this page...")
                    self.scrape_jobs(location)
                    print("Scraping for this page has been completed.")

                    time_left = minimum_page_time - time.time()
                    if time_left > 0:
                        print("Sleeping for " + str(time_left) + " seconds.")
                        time.sleep(time_left)
                        minimum_page_time = time.time() + 240
                    if page_sleep % 5 == 0:
                        sleep_time = random.randint(500, 900)
                        print("Sleeping for " + str(sleep_time/60) + " minutes.")
                        time.sleep(sleep_time)
                        page_sleep += 1
            except:
                traceback.print_exc()
                pass

            time_left = minimum_page_time - time.time()
            if time_left > 0:
                print("Sleeping for " + str(time_left) + " seconds.")
                time.sleep(time_left)
                minimum_page_time = time.time() + 240
            if page_sleep % 5 == 0:
                sleep_time = random.randint(500, 900)
                print("Sleeping for " + str(sleep_time/60) + " minutes.")
                time.sleep(sleep_time)
                page_sleep += 1


    def scrape_jobs(self, location):
        no_jobs_text = ""
        try:
            no_jobs_element = self.browser.find_element_by_class_name('jobs-search-two-pane__no-results-banner--expand')
            no_jobs_text = no_jobs_element.text
        except:
            pass
        if 'No matching jobs found' in no_jobs_text:
            raise Exception("No more jobs on this page")

        try:
            job_results = self.browser.find_element_by_class_name("jobs-search-results")
            self.scroll_slow(job_results)
            self.scroll_slow(job_results, step=300, reverse=True)

            job_list = self.browser.find_elements_by_class_name('jobs-search-results__list')[0].find_elements_by_class_name('jobs-search-results__list-item')
        except:
            raise Exception("No more jobs on this page")

        if len(job_list) == 0:
            raise Exception("No more jobs on this page")

        for job_tile in job_list:
            job_title, company, job_location, apply_method, link = "", "", "", "", ""

            try:
                job_title = job_tile.find_element_by_class_name('job-card-list__title').text
                link = job_tile.find_element_by_class_name('job-card-list__title').get_attribute('href').split('?')[0]
            except:
                pass
            try:
                company = job_tile.find_element_by_class_name('job-card-container__company-name').text
            except:
                pass
            try:
                job_location = job_tile.find_element_by_class_name('job-card-container__metadata-item').text
            except:
                pass
            try:
                apply_method = job_tile.find_element_by_class_name('job-card-container__apply-method').text
            except:
                pass

            # skip easy applys
            if 'easily' in apply_method.lower() or 'easy' in apply_method.lower():
                continue

            contains_blacklisted_keywords = False
            job_title_parsed = job_title.lower().split(' ')

            for word in self.title_blacklist:
                if word.lower() in job_title_parsed:
                    contains_blacklisted_keywords = True
                    break

            if company.lower() not in [word.lower() for word in self.company_blacklist] and \
               contains_blacklisted_keywords is False and link not in self.seen_jobs:
                job_el = job_tile.find_element_by_class_name('job-card-list__title')
                job_el.click()

                time.sleep(random.uniform(3, 5))

                # scroll through
                try:
                    job_description_area = self.browser.find_element_by_class_name("jobs-search__job-details--container")
                    self.scroll_slow(job_description_area, end=1600)
                    self.scroll_slow(job_description_area, end=1600, step=400, reverse=True)
                except:
                    pass

                t_end = time.time() + 5
                original_window = self.browser.window_handles[0]
                while time.time() < t_end:
                    try:
                        self.browser.find_element_by_class_name('jobs-apply-button').click()
                        time.sleep(1)

                        try:
                            try:
                                new_window = self.browser.window_handles[1]
                            except:
                                # it opened up another one
                                self.browser.find_element_by_class_name('jobs-apply-button').click()
                                time.sleep(1)
                                new_window = self.browser.window_handles[1]

                            self.browser.switch_to.window(window_name=new_window)
                            link = self.browser.current_url

                            self.browser.close()

                            # close any other windows if another one opened
                            windows = len(self.browser.window_handles)
                            if windows > 1:
                                while windows != 1:
                                    to_close = self.browser.window_handles[windows - 1]
                                    self.browser.switch_to.window(window_name=to_close)
                                    self.browser.close()

                                    self.browser.switch_to.window(window_name=original_window)

                                    windows -= 1
                        except:
                            pass
                        break


                    except:
                        pass
                try:
                    self.browser.switch_to.window(window_name=original_window)
                except:
                    pass

                try:

                    self.write_to_file(company, job_title, link, job_location, location)
                except Exception:
                    print("Could not write the job to the file! No special characters in the job title/company is allowed!")
                    traceback.print_exc()
            else:
                print("Job contains blacklisted keyword or company name!")
            self.seen_jobs += link

    def write_to_file(self, company, job_title, link, location, search_location):
        to_write = [company, job_title, link, location]
        file_path = self.output_file_directory + self.file_name + search_location + ".csv"

        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(to_write)

    def scroll_slow(self, scrollable_element, start=0, end=3600, step=100, reverse=False):
        if reverse:
            start, end = end, start
            step = -step

        for i in range(start, end, step):
            self.browser.execute_script("arguments[0].scrollTo(0, {})".format(i), scrollable_element)
            time.sleep(random.uniform(0.4, 1.6))

    def avoid_lock(self):
        if self.disable_lock:
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(1.0)
        pyautogui.press('esc')

    def get_base_search_url(self, parameters):
        remote_url = ""

        if parameters['remote']:
            remote_url = "f_CF=f_WRA"

        level = 1
        experience_level = parameters.get('experienceLevel', [])
        experience_url = "f_E="
        for key in experience_level.keys():
            if experience_level[key]:
                experience_url += "%2C" + str(level)
            level += 1

        distance_url = "?distance=" + str(parameters['distance'])

        job_types_url = "f_JT="
        job_types = parameters.get('experienceLevel', [])
        for key in job_types:
            if job_types[key]:
                job_types_url += "%2C" + key[0].upper()

        date_url = ""
        dates = {"all time": "", "month": "&f_TPR=r2592000", "week": "&f_TPR=r604800", "24 hours": "&f_TPR=r86400"}
        date_table = parameters.get('date', [])
        for key in date_table.keys():
            if date_table[key]:
                date_url = dates[key]
                break

        #easy_apply_url = "&f_LF=f_AL"

        extra_search_terms = [distance_url, remote_url, job_types_url, experience_url]
        extra_search_terms_str = '&'.join(term for term in extra_search_terms if len(term) > 0) + date_url

        return extra_search_terms_str

    def next_job_page(self, position, location, job_page):
        self.browser.get("https://www.linkedin.com/jobs/search/" + self.base_search_url +
                         "&keywords=" + position + location + "&start=" + str(job_page*25))

        self.avoid_lock()

