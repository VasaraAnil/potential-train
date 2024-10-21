from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service  # Import Service class
import time

class RClose:

    @staticmethod
    def main():
        # Set the path to the geckodriver
       # Set up the WebDriver with the path to geckodriver using Service class
        geckodriver_path = "C:\\Selenium\\Drivers\\geckodriver.exe"
        service = Service(executable_path=geckodriver_path)
        driver = webdriver.Firefox(service=service)
        driver.get("http://issuetracker.ntc-us.com/redmine/login?back_url=http%3A%2F%2Fissuetracker.ntc-us.com%2Fredmine%2Fprojects%2Ftd-support-tickets%2Fissues%2Fnew")

        # Find the username field
        username_field = driver.find_element(By.ID, "username")
        # Input your username
        username_field.send_keys("anilv")

        # Find the password field
        password_field = driver.find_element(By.ID, "password")
        # Input your password
        password_field.send_keys("abcd1234")

        # Find the login button
        login_button = driver.find_element(By.ID, "login-submit")
        # Click the login button
        login_button.click()

        element = driver.find_element(By.CSS_SELECTOR, ".issues.selected")
        element.click()

        filter_element = driver.find_element(By.ID, "add_filter_select")
        # Input your username
        filter_element.send_keys("au")

        time.sleep(1)  # Pause for 3 seconds

        author = driver.find_element(By.ID, "values_author_id_1")
        # Input your username
        author.send_keys("anil")

        apply = driver.find_element(By.CSS_SELECTOR, ".icon.icon-checked")
        apply.click()

        time.sleep(2)  # Pause for 5 seconds

        subject = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/form[2]/div/table/tbody/tr[1]/td[7]/a")
        subject.click()

        time.sleep(2)  # Pause for 5 seconds

        for i in range(1000):
            edit = driver.find_element(By.CSS_SELECTOR, ".icon.icon-edit")
            edit.click()

            status = driver.find_element(By.ID, "issue_status_id")
            # Input your username
            status.send_keys("close")

            time.sleep(1)  # Pause for 2 seconds

            submit = driver.find_element(By.CSS_SELECTOR, "#issue-form > input:nth-child(7)")
            submit.click()

            time.sleep(1)  # Pause for 2 seconds

            next_button = driver.find_element(By.CSS_SELECTOR, ".next-prev-links > a:nth-child(1)")
            next_button.click()

if __name__ == "__main__":
    RClose.main()

