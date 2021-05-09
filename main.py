from selenium import webdriver


class HhParser:
    def __init__(self, driver):
        self.driver = driver

    def get_pages_count(self):
        pagination_btn = self.driver.find_elements_by_css_selector("a.bloko-button[data-qa='pager-page']")
        if pagination_btn:
            return int(pagination_btn[-1].text)
        else:
            return 1

    def get_vacancies(self):
        vacancy_items = self.driver.find_elements_by_css_selector("div.vacancy-serp-item")
        for vacancy_item in vacancy_items:
            vacancy_url = vacancy_item.find_element_by_css_selector(
                'a[data-qa="vacancy-serp__vacancy-title"]').get_attribute("href")
            vacancy_data = self.parse_vacansy(self.get_vacancy_data, vacancy_url)
            print(vacancy_data)

    def get_vacancy_data(self, vacancy_url):
        title = self.get_title()
        description = self.get_description()
        salary = self.get_salary()
        skills = self.get_skills()
        company_name = self.get_company_name()
        address = self.get_address()

        return {
            'title': title,
            'description': description,
            'salary': salary,
            'skills': skills,
            'company_name': company_name,
            'address': address,
            'vacancy_url': vacancy_url,
        }

    def get_address(self):
        try:
            address = self.driver.find_element_by_css_selector('span[data-qa="vacancy-view-raw-address"]').text
        except:
            address = ''
        return address

    def get_company_name(self):
        return self.driver.find_element_by_css_selector('.vacancy-company__details a span span').text

    def get_salary(self):
        return self.driver.find_element_by_css_selector('.vacancy-salary span').text

    def get_skills(self):
        skills = []
        skills_btn = self.driver.find_elements_by_css_selector('div.bloko-tag.bloko-tag_inline')
        if (len(skills_btn)):
            for skill_btn in skills_btn:
                skills.append(skill_btn.text)
        return skills

    def get_description(self):
        return self.driver.find_element_by_css_selector('div[data-qa="vacancy-description"]').text

    def get_title(self):
        return self.driver.find_element_by_css_selector('div.vacancy-title h1').text

    def parse_vacansy(self, func, url):
        self.open_and_switch_new_tab(url)
        vacancy_data = func(url)
        self.close_and_switch_to_main_tab()
        return vacancy_data

    def open_and_switch_new_tab(self, url):
        self.driver.execute_script("window.open('')")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(url)

    def close_and_switch_to_main_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


def parser():
    driver = webdriver.Firefox()
    driver.get("https://spb.hh.ru/search/vacancy?text=python")
    hh_parser = HhParser(driver)
    pages_count = hh_parser.get_pages_count()
    hh_parser.get_vacancies()
    driver.close()


parser()
