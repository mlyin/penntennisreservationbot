from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

class TennisBookingBot:
    def __init__(self):
        self.driver = None
        self.username = os.getenv('TENNIS_USERNAME')
        self.password = os.getenv('TENNIS_PASSWORD')
        
    def initialize_driver(self):
        options = webdriver.ChromeOptions()
        # Keeping browser visible for testing
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def login(self):
        print("Attempting to load login page...")
        self.driver.get('https://penntennis.clubautomation.com/')
        
        try:
            print("Waiting for login form...")
            username_field = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            print("Found username field")
            
            password_field = self.driver.find_element(By.ID, "password")
            print("Found password field")
            
            print("Entering credentials...")
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            print("Looking for login button...")
            login_button = self.driver.find_element(By.ID, "loginButton")
            print("Found login button")
            
            login_button.click()
            print("Clicked login button")
            
            # Wait for login to complete (wait for member page to load)
            WebDriverWait(self.driver, 20).until(
                EC.url_contains("/member")
            )
            print("Login successful!")
            
        except Exception as e:
            print(f"Login error: {str(e)}")
            print("\nCurrent URL:", self.driver.current_url)
            print("\nPage source:", self.driver.page_source[:1000])
            raise
        
    def navigate_to_booking(self):
        print("Navigating to booking page...")
        self.driver.get('https://penntennis.clubautomation.com/event/reserve-court-new')
        
        # Wait for the page to load completely
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "guest_1"))
        )
        print("Booking page loaded successfully")

    def add_participant(self, participant_name):
        try:
            print(f"\nAttempting to add participant: {participant_name}")
            
            # Wait for the page to be fully loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "addParticipant"))
            )
            
            # Click Add Participant using JavaScript
            print("Clicking Add Participant using JavaScript...")
            self.driver.execute_script("jQuery('#addParticipant').trigger('click');")
            print("Triggered Add Participant click")
            
            # Wait for and find the guest input field
            print("Looking for guest input field...")
            guest_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "guest_1"))
            )
            
            # Clear and enter the name
            print("Found guest input, entering name...")
            guest_input.clear()
            guest_input.send_keys(participant_name)
            print(f"Entered name: {participant_name}")
            
            # Wait for autocomplete suggestions
            print("Waiting for autocomplete suggestions...")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-menu-item"))
            )
            
            # Small delay to ensure suggestions are fully loaded
            time.sleep(1)
            
            # Find and click the matching suggestion
            suggestions = self.driver.find_elements(By.CLASS_NAME, "ui-menu-item")
            for suggestion in suggestions:
                suggestion_text = suggestion.text.strip()
                print(f"Found suggestion: {suggestion_text}")
                if participant_name.lower() in suggestion_text.lower():
                    print(f"Clicking matching suggestion: {suggestion_text}")
                    suggestion.click()
                    print("Selected participant successfully")
                    return True
            
            print("No matching suggestion found")
            return False
            
        except Exception as e:
            print(f"Error adding participant: {str(e)}")
            return False

    def search_courts(self, date_str, court_type="indoor"):
        try:
            print(f"\nSearching for {court_type} courts on {date_str}")
            
            # # Wait for and set date
            date_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "date"))
            )
            date_input.clear()
            date_input.send_keys(date_str)
            
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "reserve-court-search"))
            )
            search_button.click()
            print("Clicked search button")
            
            # Wait a moment for results to load
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"Search error: {e}")
            return False
    
    def close(self):
        if self.driver:
            self.driver.quit()

def test_booking():
    load_dotenv()
    
    if not os.getenv('TENNIS_USERNAME') or not os.getenv('TENNIS_PASSWORD'):
        print("Error: Missing credentials in .env file")
        return
        
    bot = TennisBookingBot()
    try:
        bot.initialize_driver()
        bot.login()
        bot.navigate_to_booking()
        
        if bot.add_participant("Alan Du"):
            bot.search_courts(
                date_str="12/14/2024",
                court_type="indoor"
            )
        else:
            print("Failed to add participant")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        bot.close()

if __name__ == "__main__":
    test_booking()