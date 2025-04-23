import re
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
from fpdf import FPDF, XPos, YPos
import os

# Driver setup with Chrome options
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    return driver

# Facebook login
def login_to_facebook(driver, email, password):
    driver.get('https://www.facebook.com')
    time.sleep(2)
    
    driver.find_element(By.ID, 'email').send_keys(email)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.NAME, 'login').click()
    time.sleep(5)

# Extract profile ID from URL
def extract_profile_id(driver):
    driver.get('https://www.facebook.com/profile')
    time.sleep(5)
    current_url = driver.current_url
    match = re.search(r"id=(\d+)", current_url)
    if match:
        profile_id = match.group(1)
        print(f"Extracted profile ID: {profile_id}")
        return profile_id
    else:
        print("Profile ID not found, using default example.")
        return "100087722406099"  # Fallback example ID if the pattern is not found

# Wait for the page to load
def wait_for_page_load(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# # Improved scroll function with thorough checks
# def scroll_down(driver, pause_time=5, scrolls=10, screenshot_prefix=None):
#     driver.execute_script("window.scrollTo(0, 0)")  # Start at the top
#     time.sleep(3)  # Allow time for initial page load

#     last_height = driver.execute_script("return document.body.scrollHeight")
#     screenshots = []

#     for i in range(scrolls):
#         wait_for_page_load(driver)  # Ensure page has fully loaded
        
#         # Capture screenshot
#         if screenshot_prefix:
#             screenshot_name = f"{screenshot_prefix}_scroll_{i}.png"
#             driver.save_screenshot(screenshot_name)
#             screenshots.append(screenshot_name)
#             print(f"Captured screenshot: {screenshot_name}")

#         # Scroll down and check scroll position
#         driver.execute_script("window.scrollBy(0, window.innerHeight * 0.8);")
#         time.sleep(pause_time)

#         # Verify if the scroll position has actually changed
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         current_scroll_position = driver.execute_script("return window.pageYOffset;")
        
#         if new_height == last_height or current_scroll_position == 0:
#             print("Reached the bottom or unable to scroll further.")
#             break  # Stop scrolling if at the bottom

#         last_height = new_height

#     return screenshots

# def scroll_down(driver, pause_time=5, scrolls=10, screenshot_prefix=None):
#     driver.execute_script("window.scrollTo(0, 0)")  # Start at the top
#     time.sleep(3)  # Allow time for initial page load

#     last_height = driver.execute_script("return document.body.scrollHeight")
#     screenshots = []

#     for i in range(scrolls):
#         wait_for_page_load(driver)  # Ensure page has fully loaded

#         # Capture screenshot
#         if screenshot_prefix:
#             screenshot_name = f"{screenshot_prefix}_scroll_{i}.png"
#             driver.save_screenshot(screenshot_name)
#             screenshots.append(screenshot_name)
#             print(f"Captured screenshot: {screenshot_name}")

#         # Scroll down to the bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(pause_time)  # Increase pause time to load dynamic content

#         # Verify if the scroll position has actually changed
#         new_height = driver.execute_script("return document.body.scrollHeight")

#         if new_height == last_height:
#             print("Reached the bottom or unable to scroll further.")
#             break  # Stop scrolling if at the bottom

#         last_height = new_height

    # return screenshots

def scroll_down(driver, pause_time=5, scrolls=10, screenshot_prefix=None):
    driver.execute_script("window.scrollTo(0, 0)")  # Start at the top
    time.sleep(3)  # Allow time for initial page load

    last_height = driver.execute_script("return document.body.scrollHeight")
    screenshots = []
    
    # Capture initial screenshot before scrolling
    if screenshot_prefix:
        screenshot_name = f"{screenshot_prefix}_scroll_0.png"
        driver.save_screenshot(screenshot_name)
        screenshots.append(screenshot_name)
        print(f"Captured screenshot: {screenshot_name}")

    for i in range(1, scrolls + 1):
        wait_for_page_load(driver)  # Ensure the page has fully loaded

        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # Pause to allow content to load

        # Capture screenshot after each scroll
        if screenshot_prefix:
            screenshot_name = f"{screenshot_prefix}_scroll_{i}.png"
            driver.save_screenshot(screenshot_name)
            screenshots.append(screenshot_name)
            print(f"Captured screenshot: {screenshot_name}")

        # Verify if the scroll position has actually changed
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            print("Reached the bottom or unable to scroll further.")
            break  # Stop scrolling if at the bottom

        last_height = new_height

    return screenshots

# Combine images using OpenCV
def combine_images_opencv(image_list, output_image):
    images = [cv2.imread(img) for img in image_list]
    
    # Ensure all images have the same width
    widths = [img.shape[1] for img in images]
    common_width = min(widths)
    
    resized_images = [cv2.resize(img, (common_width, int(img.shape[0] * common_width / img.shape[1]))) for img in images]
    
    # Concatenate images vertically
    combined_image = np.vstack(resized_images)
    
    cv2.imwrite(output_image, combined_image)
    print(f"Combined image saved as {output_image}")

# Capture profile and related sections (posts, about, etc.)
def capture_profile_sections(driver, profile_id):
    sections = {
        "Posts": f"https://www.facebook.com/profile.php?id={profile_id}",
        "About": f"https://www.facebook.com/profile.php?id={profile_id}&sk=about",
        "Friends": f"https://www.facebook.com/profile.php?id={profile_id}&sk=friends",
        "Photos": f"https://www.facebook.com/profile.php?id={profile_id}&sk=photos",
        "Videos": f"https://www.facebook.com/profile.php?id={profile_id}&sk=videos",
        "Friend Requests": "https://www.facebook.com/friends",
        "Events": f"https://www.facebook.com/profile.php?id={profile_id}&sk=events",
        "Reviews": f"https://www.facebook.com/profile.php?id={profile_id}&sk=reviews_given",
        "Groups": f"https://www.facebook.com/profile.php?id={profile_id}&sk=groups"
    }

    screenshots = {}
    for section_name, url in sections.items():
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load
        section_screenshots = scroll_down(driver, scrolls=10, screenshot_prefix=section_name.lower())
        combined_image = f"{section_name.lower()}_combined.png"
        combine_images_opencv(section_screenshots, combined_image)
        screenshots[section_name] = combined_image
    
    return screenshots

# Generate PDF report with updated FPDF methods to avoid deprecation warnings
def generate_pdf_report(screenshots):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.add_page()
    pdf.set_font("helvetica", size=12)  # Use "helvetica" as Arial is deprecated
    pdf.cell(200, 10, text="Facebook Profile Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    for section_name, image_path in screenshots.items():
        pdf.add_page()
        pdf.cell(200, 10, text=section_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.image(image_path, x=10, y=30, w=190)
    
    pdf.output("facebook_profile_report.pdf")
    print("PDF report generated as 'facebook_profile_report.pdf'")

# Main script to execute everything
def main():
    driver = create_driver()
    email = '3yashmavani@gmail.com'
    password = 'yhm123'
    
    login_to_facebook(driver, email, password)
    
    profile_id = extract_profile_id(driver)  # Extract the profile ID from URL
    
    screenshots = capture_profile_sections(driver, profile_id)
    
    generate_pdf_report(screenshots)
    
    driver.quit()

if __name__ == "__main__":
    main()
