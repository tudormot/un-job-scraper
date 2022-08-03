from src.scrape.browser_automation.automation_interface import \
    AutomationInterface
from datetime import datetime, date
from datetime import timedelta
from src.models.job_model import JobModel
from bs4 import BeautifulSoup, NavigableString
import re
import logging as log

from src.scrape.postprocessing import postprocess_job_add_categories


class JobPageScraper:
    def __init__(self, browser_automator):
        # it is important to create a new instance of chrome. This way
        # parsing of the main page and the job pages can run "in parallel"
        self.browser_automator: AutomationInterface = browser_automator

    def scrape_job_from_job_page(self, url) -> JobModel:
        job = JobModel()
        self._populate_job_from_main_url(job, url)
        self._populate_job_from_button_click_result(job, url)
        postprocess_job_add_categories(job)
        return job

    @staticmethod
    def _has_h2_class_but_also_style(tag):
        return tag.has_attr('style') and tag.name == 'h2'

    def _populate_job_from_main_url(self, job, url):
        log.info("Scraping following url: " + str(url))

        html = self.browser_automator.get_html_from_url(url)

        soup = BeautifulSoup(html, 'html.parser')

        # get ID and title
        job_id = url.split('/')[-1]
        job.id = job_id
        potential_titles_list = soup.find_all(
            JobPageScraper._has_h2_class_but_also_style)
        if len(potential_titles_list) == 0:
            log.error("Could not find job title. Here is the html: ")
            log.error(soup.prettify())
            raise Exception("Could not parse job title")
        if len(potential_titles_list) != 1:
            log.warning("Found multiple potential titles. Choosing most "
                        "likely")
            assert 'Roboto Condensed' in potential_titles_list[0]['style'], \
                "Unable to decide which is the title!"

        job.title = str(potential_titles_list[0].string)

        self._get_info_from_contents_container(soup, job)

        # get closing date
        tag = soup.find("div", class_='job' + job.id)
        iterator = tag.children
        iterator.__next__()
        t = iterator.__next__()
        job.closing_date = self._parse_string_for_date(t.string)

        # get tags
        job.tags = [x.a.string for x in soup.find_all("div",
                                                      class_="md-chip "
                                                             "md-chip-raised "
                                                             "md-chip-hover")[
                                        1:]]

        self._get_text_content(soup, job)
        self._decide_job_category(job)

    @staticmethod
    def _get_info_from_contents_container(soup, job):
        contents = [x.contents for x in
                    soup.find_all("li",
                                  class_="list-group-item dropdown-toggle")]
        contents.pop()  # drop twitter button information

        pattern_org = 'Organization:\n'
        pattern_country = 'Country:\n'
        pattern_city_1 = 'City:\n'
        pattern_city_2 = 'Field location:\n'
        pattern_office = 'Office:\n'
        pattern_grade = 'Grade:\n'

        job.organisation = None
        job.country = None
        job.city = None
        job.grade = None
        job.office = None

        for content in contents:
            if content[0] == pattern_org:
                job.organisation = content[1].string.strip('\n')
            elif content[0] == pattern_country:
                job.country = content[1].string.strip('\n')
            elif content[0] == pattern_city_1 or content[0] == pattern_city_2:
                job.city = content[1].string.strip('\n')
            elif content[0] == pattern_grade:
                job.grade = content[1].string.strip('\n')
            elif content[0] == pattern_office:
                job.office = content[1].string.strip('\n')

        if job.office is None:
            log.error('cant parse office! Leaving Blank')
        if job.country is None:
            log.error('cant parse country! Leaving Blank')
        if job.city is None:
            log.error('cant parse city! Leaving Blank')
        if job.organisation is None:
            log.error('cant parse organisation! Leaving Blank')
        if job.grade is None:
            log.error('cant parse grade! Leaving Blank')

    @staticmethod
    def _get_text_content(soup, job):
        text_tag = soup.find("div", class_='t' + job.id)
        if text_tag is not None:
            # we are in the normal job format
            ads = text_tag.find_all('ins', class_='adsbygoogle')
            for ad in ads:
                ad.decompose()
            tag_buttons = text_tag.find_all("div", class_='md-chips')
            for container in tag_buttons:
                container.decompose()
            ads2 = text_tag.find_all('div', class_='google-auto-placed')
            for ad in ads2:
                ad.decompose()
            scripts = text_tag.find_all('script')
            for script in scripts:
                script.decompose()

            text_tag['class'] = 'job_description'
            JobPageScraper._remove_last_line_gibberish_and_urls(text_tag, soup)
            job.extra_information = str(text_tag)
        else:
            # we are probably in pdf job mode.
            log.warning(
                "Could not scrape main text content. Possibly pdf content.")
            job.extra_information = "Please follow original job link for " \
                                    "more information"

    @staticmethod
    def _decide_job_category(job):
        title = job.title
        text = job.extra_information
        pattern_internship = 'internship|intern[^a-z]'
        pattern_contractor = 'contractor|contract|consultancy|consultant'
        pattern_part_time = 'part time'

        # first try to decide based on title:
        c = len(re.findall(pattern_internship, title, re.IGNORECASE))
        if c > 0:
            job.job_type = 'Internship'
            return

        # exit here in case we could not extract main text body:
        if text is None:
            job.job_type = 'Full Time '
            return

        c = len(re.findall(pattern_contractor, text, re.IGNORECASE))
        if c > 2:
            job.job_type = 'Contractor'
        else:
            i = len(re.findall(pattern_internship, text, re.IGNORECASE))
            if i > 3:
                job.job_type = 'Internship'
            else:
                p = len(re.findall(pattern_part_time, text, re.IGNORECASE))
                if p > 2:
                    job.job_type = 'Part Time'
                else:
                    job.job_type = 'Full Time '

    @staticmethod
    def _parse_string_for_date(closing_date_pretty: str) -> date:
        my_hash = {
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
        }
        try:
            chunks = closing_date_pretty.split()
            if len(chunks[3]) == 1: chunks[3] = '0' + chunks[
                3]  # so date is dd.mm.YYYY
            return datetime.strptime(
                chunks[3] + '.' + my_hash[chunks[4]] + '.' +
                chunks[5], '%d.%m.%Y').date()
        except AttributeError as e:
            now = datetime.now()
            FAKE_DATE = (now + timedelta(weeks=8)).date()
            log.error(
                "Unable to find closing date for job. Setting artificial "
                "closing date in two months from now. FAKE_DATE = " +
                str(FAKE_DATE))
            return FAKE_DATE

    @staticmethod
    def _remove_last_line_gibberish_and_urls(tag, soup):
        re_pattern = r'[^ ]*(?:http://|www.|https://)[a-zA-Z0-9_/.]+'
        no_changes_made = True
        while no_changes_made:
            for i, string in enumerate(tag.strings):
                python_string = str(string)
                found_links = re.findall(re_pattern, python_string,
                                         re.IGNORECASE)
                if found_links:
                    no_changes_made = False
                    link = found_links[0]
                    chunks = python_string.split(link, 1)
                    new_tag = soup.new_tag("a", href=link)
                    new_tag.string = '(link)'
                    str1 = NavigableString(chunks[0])
                    string.replace_with(str1)
                    str1.insert_after(new_tag)
                    new_tag.insert_after(NavigableString(chunks[1]))
                    break
            if no_changes_made:
                break
            else:
                no_changes_made = True

        l = list(tag.strings)
        l[-1].extract()  # this is a gibberish code that should be removed

    def _populate_job_from_button_click_result(self, job, url):
        job.original_job_link = \
            self.browser_automator.get_url_after_button_press(url)
