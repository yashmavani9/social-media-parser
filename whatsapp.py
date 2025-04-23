# # from datetime import datetime
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.action_chains import ActionChains
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # import time
# # from fpdf import FPDF

# # # Replace unsupported Unicode characters with ASCII equivalents
# # def sanitize_message(message_info):
# #     replacements = {
# #         '\u2026': '...',  # Ellipsis
# #         '‘': "'", '’': "'",  # Single quotes
# #         '“': '"', '”': '"',  # Double quotes
# #         '–': '-',  # En-dash
# #         '—': '-',  # Em-dash
# #     }
# #     for key, value in replacements.items():
# #         message_info = message_info.replace(key, value)
# #     return message_info

# # # Function to generate a WhatsApp-style PDF report using FPDF
# # class WhatsAppChatPDF(FPDF):
# #     def header(self):
# #         self.set_font('Arial', 'B', 16)
# #         self.cell(200, 10, f'Messages in Chat', ln=True, align='C')

# #     def add_message(self, timestamp, sender, message_type, message_info, is_user_message):
# #         # Format the timestamp
# #         if timestamp:
# #             timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
# #         else:
# #             timestamp_str = "No Timestamp"

# #         # Sanitize message for unsupported characters
# #         message_info = sanitize_message(message_info)

# #         # Add message based on whether it's from the user or contact
# #         self.set_font('Arial', '', 12)
        
# #         if is_user_message:
# #             # User's message on the right (light blue)
# #             self.set_fill_color(173, 216, 230)  # Light blue background
# #             self.set_text_color(0, 0, 0)  # Black text
# #             self.multi_cell(0, 10, f"{timestamp_str} - You", align='R', fill=True)
# #             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='R')
# #         else:
# #             # Contact's message on the left (light grey)
# #             self.set_fill_color(211, 211, 211)  # Light grey background
# #             self.set_text_color(0, 0, 0)  # Black text
# #             self.multi_cell(0, 10, f"{timestamp_str} - {sender}", align='L', fill=True)
# #             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='L')

# #         self.ln(5)  # Add space after each message

# # def generate_pdf_report(messages, contact_name):
# #     pdf = WhatsAppChatPDF()
# #     pdf.add_page()

# #     for timestamp, sender, message_type, message_info in messages:
# #         # Check if the message is from the user or the contact
# #         is_user_message = (sender == contact_name)
# #         pdf.add_message(timestamp, sender, message_type, message_info, is_user_message)

# #     # Save the PDF
# #     pdf_filename = f"messages_report_{contact_name}.pdf"
# #     pdf.output(pdf_filename)
# #     print(f"PDF report generated: {pdf_filename}")

# # # Function to parse timestamp
# # def parse_timestamp(timestamp):
# #     try:
# #         timestamp = timestamp.split(']')[0].strip()
# #         timestamp = timestamp.strip('[] ')
# #         return datetime.strptime(timestamp, '%H:%M, %m/%d/%Y')
# #     except ValueError as e:
# #         print(f"Error parsing timestamp: {e}")
# #         return None

# # def get_message_type(message):
# #     try:
# #         text_element = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
# #         if text_element:
# #             return "text", text_element[0].text

# #         image_element = message.find_elements(By.XPATH, './/img[contains(@src, "blob:")]')
# #         if image_element:
# #             image_id = f"image_{hash(image_element[0].get_attribute('src')) % 1000:03d}"
# #             caption = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
# #             return "image", caption[0].text if caption else image_id

# #         # Add other media types as needed...

# #         return "unknown", "Unknown message type"

# #     except Exception as e:
# #         print(f"Error detecting message type: {e}")
# #         return "unknown", "Unknown message type"

# # # Updated scroll_and_capture function
# # def scroll_and_capture(driver, start_date, end_date):
# #     wait = WebDriverWait(driver, 10)
# #     chat_container_xpath = '//*[@id="app"]/div/div[2]/div[4]'
# #     chat_container = wait.until(EC.presence_of_element_located((By.XPATH, chat_container_xpath)))

# #     last_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
# #     messages_within_range = []

# #     while True:
# #         messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
# #         print(f"Found {len(messages)} messages.")

# #         for message in messages:
# #             try:
# #                 sender_name_element = message.find_elements(By.XPATH, './/span[contains(@class, "copyable-text")]')
# #                 sender_name = sender_name_element[0].text if sender_name_element else "Unknown"

# #                 timestamp_element = message.find_elements(By.XPATH, './/div[@data-pre-plain-text]')
# #                 if timestamp_element:
# #                     timestamp = timestamp_element[0].get_attribute("data-pre-plain-text")
# #                     print(f"Raw Timestamp: {timestamp}")
# #                     parsed_timestamp = parse_timestamp(timestamp)

# #                     if parsed_timestamp:
# #                         print(f"Parsed Timestamp: {parsed_timestamp}")
# #                         if start_date <= parsed_timestamp.date() <= end_date:
# #                             message_type, message_info = get_message_type(message)
# #                             messages_within_range.append((parsed_timestamp, sender_name, message_type, message_info))
# #                             print(f"Message within range: {parsed_timestamp} - {sender_name} - {message_type} - {message_info}")
# #                             print("-" * 50)
# #                 else:
# #                     print("Non-text message detected")
# #                     message_type, message_info = get_message_type(message)
# #                     if message_type != "unknown":
# #                         messages_within_range.append((None, sender_name, message_type, message_info))
# #                         print(f"Media message detected - {message_type}: {message_info}")
# #                         print("-" * 50)

# #             except Exception as e:
# #                 print(f"Error processing message: {e}")

# #         driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight;", chat_container)
# #         time.sleep(2)

# #         new_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
# #         if new_height == last_height:
# #             break
# #         last_height = new_height

# #     print("Finished processing messages.")
# #     return messages_within_range  # Return captured messages for PDF generation

# # # Function to capture chat messages
# # def capture_chat(driver, contact_name, start_date, end_date):
# #     try:
# #         search_box_xpath = '//div[@role="textbox"]'
# #         search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

# #         search_box.click()
# #         search_box.send_keys(contact_name)
# #         time.sleep(2)  

# #         contact_xpath = f'//span[@title="{contact_name}"]'
# #         contact = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, contact_xpath)))
# #         actions = ActionChains(driver)
# #         actions.move_to_element(contact).click().perform()
# #         time.sleep(3)

# #         messages_within_range = scroll_and_capture(driver, start_date, end_date)
# #         return messages_within_range  # Return messages for PDF generation

# #     except Exception as e:
# #         print(f"Error: {e}")
# #         driver.get_screenshot_as_file("error_screenshot.png")
# #         return None  # Return None if there is an error

# # # Main function
# # def main():
# #     driver = webdriver.Chrome()
# #     driver.get("https://web.whatsapp.com")
# #     input("Please scan the QR code and press Enter...")

# #     contact_name = input("Enter the contact name: ")
# #     start_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), '%Y-%m-%d').date()
# #     end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), '%Y-%m-%d').date()

# #     messages = capture_chat(driver, contact_name, start_date, end_date)

# #     if messages:  # Check if messages are not None
# #         generate_pdf_report(messages, contact_name)  # Generate PDF after capturing messages
# #     else:
# #         print("No messages found or an error occurred.")

# #     driver.quit()

# # if __name__ == "__main__":
# #     main()


# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from fpdf import FPDF

# # Replace unsupported Unicode characters with ASCII equivalents
# def sanitize_message(message_info):
#     replacements = {
#         '\u2026': '...',  # Ellipsis
#         '‘': "'", '’': "'",  # Single quotes
#         '“': '"', '”': '"',  # Double quotes
#         '–': '-',  # En-dash
#         '—': '-',  # Em-dash
#     }
#     for key, value in replacements.items():
#         message_info = message_info.replace(key, value)
#     return message_info

# # Function to generate a WhatsApp-style PDF report using FPDF
# # class WhatsAppChatPDF(FPDF):
# #     def header(self):
# #         self.set_font('DejaVu', 'B', 16)
# #         self.cell(200, 10, f'Messages in Chat', ln=True, align='C')

# #     def add_message(self, timestamp, sender, message_type, message_info, is_user_message):
# #         # Format the timestamp
# #         if timestamp:
# #             timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
# #         else:
# #             timestamp_str = "No Timestamp"

# #         # Sanitize message for unsupported characters
# #         message_info = sanitize_message(message_info)

# #         # Add message based on whether it's from the user or contact
# #         self.set_font('DejaVu', '', 12)
        
# #         if is_user_message:
# #             # User's message on the right (light blue)
# #             self.set_fill_color(173, 216, 230)  # Light blue background
# #             self.set_text_color(0, 0, 0)  # Black text
# #             self.multi_cell(0, 10, f"{timestamp_str} - You", align='R', fill=True)
# #             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='R')
# #         else:
# #             # Contact's message on the left (light grey)
# #             self.set_fill_color(211, 211, 211)  # Light grey background
# #             self.set_text_color(0, 0, 0)  # Black text
# #             self.multi_cell(0, 10, f"{timestamp_str} - {sender}", align='L', fill=True)
# #             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='L')

# #         self.ln(5)  # Add space after each message

# # def generate_pdf_report(messages, contact_name):
# #     pdf = WhatsAppChatPDF()
# #     pdf.add_page()

# #     # Add DejaVu font for UTF-8 support
# #     pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
# #     pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

# #     for timestamp, sender, message_type, message_info in messages:
# #         # Check if the message is from the user or the contact
# #         is_user_message = (sender == contact_name)
# #         pdf.add_message(timestamp, sender, message_type, message_info, is_user_message)

# #     # Save the PDF
# #     pdf_filename = f"messages_report_{contact_name}.pdf"
# #     pdf.output(pdf_filename)
# #     print(f"PDF report generated: {pdf_filename}")

# from fpdf import FPDF

# # Function to generate a WhatsApp-style PDF report using FPDF
# class WhatsAppChatPDF(FPDF):
#     def header(self):
#         self.set_font('DejaVu', 'B', 16)  # Use the bold version of DejaVu for the header
#         self.cell(200, 10, f'Messages in Chat', ln=True, align='C')

#     def add_message(self, timestamp, sender, message_type, message_info, is_user_message):
#         # Format the timestamp
#         if timestamp:
#             timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         else:
#             timestamp_str = "No Timestamp"

#         # Add message based on whether it's from the user or contact
#         self.set_font('DejaVu', '', 12)  # Use the regular DejaVu font
        
#         if is_user_message:
#             # User's message on the right (light blue)
#             self.set_fill_color(173, 216, 230)  # Light blue background
#             self.set_text_color(0, 0, 0)  # Black text
#             self.multi_cell(0, 10, f"{timestamp_str} - You", align='R', fill=True)
#             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='R')
#         else:
#             # Contact's message on the left (light grey)
#             self.set_fill_color(211, 211, 211)  # Light grey background
#             self.set_text_color(0, 0, 0)  # Black text
#             self.multi_cell(0, 10, f"{timestamp_str} - {sender}", align='L', fill=True)
#             self.multi_cell(0, 10, f"{message_type}: {message_info}", align='L')

#         self.ln(5)  # Add space after each message

# def generate_pdf_report(messages, contact_name):
#     pdf = WhatsAppChatPDF()

#     # Register the DejaVu fonts
#     pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
#     pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

#     pdf.add_page()

#     for timestamp, sender, message_type, message_info in messages:
#         # Check if the message is from the user or the contact
#         is_user_message = (sender == contact_name)
#         pdf.add_message(timestamp, sender, message_type, message_info, is_user_message)

#     # Save the PDF
#     pdf_filename = f"messages_report_{contact_name}.pdf"
#     pdf.output(pdf_filename)
#     print(f"PDF report generated: {pdf_filename}")


# # Function to parse timestamp
# # def parse_timestamp(timestamp):
# #     try:
# #         timestamp = timestamp.split(']')[0].strip()
# #         timestamp = timestamp.strip('[] ')
# #         return datetime.strptime(timestamp, '%H:%M, %m/%d/%Y')
# #     except ValueError as e:
# #         print(f"Error parsing timestamp: {e}")
# #         return None

# # def parse_timestamp(timestamp):
# #     try:
# #         timestamp = timestamp.split(']')[0].strip()
# #         timestamp = timestamp.strip('[] ')
        
# #         # First try with the format "day/month/year"
# #         try:
# #             return datetime.strptime(timestamp, '%H:%M, %d/%m/%Y')
# #         except ValueError:
# #             # Fallback to "month/day/year" format if needed
# #             return datetime.strptime(timestamp, '%H:%M, %m/%d/%Y')
        
# #     except ValueError as e:
# #         print(f"Error parsing timestamp: {e}")
# #         return None


# def get_message_type(message):
#     try:
#         text_element = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
#         if text_element:
#             return "text", text_element[0].text

#         image_element = message.find_elements(By.XPATH, './/img[contains(@src, "blob:")]')
#         if image_element:
#             image_id = f"image_{hash(image_element[0].get_attribute('src')) % 1000:03d}"
#             caption = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
#             return "image", caption[0].text if caption else image_id

#         # Add other media types as needed...

#         return "unknown", "Unknown message type"

#     except Exception as e:
#         print(f"Error detecting message type: {e}")
#         return "unknown", "Unknown message type"

# # from datetime import datetime

# # def parse_timestamp(timestamp):
# #     try:
# #         timestamp = timestamp.split(']')[0].strip()
# #         timestamp = timestamp.strip('[] ')
        
# #         # Use the day/month/year format
# #         return datetime.strptime(timestamp, '%H:%M, %d/%m/%Y')
        
# #     except ValueError as e:
# #         print(f"Error parsing timestamp: {e}")
# #         return None

# def parse_timestamp(timestamp):
#     try:
#         timestamp = timestamp.split(']')[0].strip()
#         timestamp = timestamp.strip('[] ')

#         # First, try with day/month/year (common in some WhatsApp regions)
#         try:
#             return datetime.strptime(timestamp, '%H:%M, %d/%m/%Y')
#         except ValueError:
#             # If day/month/year fails, fallback to month/day/year
#             return datetime.strptime(timestamp, '%H:%M, %m/%d/%Y')

#     except ValueError as e:
#         print(f"Error parsing timestamp: {e}")
#         return None

# # def scroll_and_capture(driver, start_date, end_date):
# #     wait = WebDriverWait(driver, 10)
# #     chat_container_xpath = '//*[@id="app"]/div/div[2]/div[4]'
# #     chat_container = wait.until(EC.presence_of_element_located((By.XPATH, chat_container_xpath)))

# #     last_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
# #     messages_within_range = []

# #     while True:
# #         messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
# #         print(f"Found {len(messages)} messages.")

# #         for message in messages:
# #             try:
# #                 sender_name_element = message.find_elements(By.XPATH, './/span[contains(@class, "copyable-text")]')
# #                 sender_name = sender_name_element[0].text if sender_name_element else "Unknown"

# #                 timestamp_element = message.find_elements(By.XPATH, './/div[@data-pre-plain-text]')
# #                 if timestamp_element:
# #                     timestamp = timestamp_element[0].get_attribute("data-pre-plain-text")
# #                     print(f"Raw Timestamp: {timestamp}")
# #                     parsed_timestamp = parse_timestamp(timestamp)

# #                     if parsed_timestamp:
# #                         print(f"Parsed Timestamp: {parsed_timestamp}")
# #                         # Check if the parsed timestamp is within the given date range
# #                         if start_date <= parsed_timestamp.date() <= end_date:
# #                             message_type, message_info = get_message_type(message)
# #                             messages_within_range.append((parsed_timestamp, sender_name, message_type, message_info))
# #                             print(f"Message within range: {parsed_timestamp} - {sender_name} - {message_type} - {message_info}")
# #                             print("-" * 50)
# #                         else:
# #                             print(f"Message out of range: {parsed_timestamp}")
# #                 else:
# #                     print("Non-text message detected")
# #                     message_type, message_info = get_message_type(message)
# #                     if message_type != "unknown":
# #                         messages_within_range.append((None, sender_name, message_type, message_info))
# #                         print(f"Media message detected - {message_type}: {message_info}")
# #                         print("-" * 50)

# #             except Exception as e:
# #                 print(f"Error processing message: {e}")

# #         driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight;", chat_container)
# #         time.sleep(2)

# #         new_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
# #         if new_height == last_height:
# #             break
# #         last_height = new_height

# #     print("Finished processing messages.")
# #     return messages_within_range  # Return captured messages for PDF generation


# def scroll_and_capture(driver, start_date, end_date):
#     wait = WebDriverWait(driver, 10)
#     chat_container_xpath = '//*[@id="app"]/div/div[2]/div[4]'
#     chat_container = wait.until(EC.presence_of_element_located((By.XPATH, chat_container_xpath)))

#     last_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
#     messages_within_range = []

#     while True:
#         messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
#         print(f"Found {len(messages)} messages.")

#         for message in messages:
#             try:
#                 sender_name_element = message.find_elements(By.XPATH, './/span[contains(@class, "copyable-text")]')
#                 sender_name = sender_name_element[0].text if sender_name_element else "Unknown"

#                 timestamp_element = message.find_elements(By.XPATH, './/div[@data-pre-plain-text]')
#                 if timestamp_element:
#                     timestamp = timestamp_element[0].get_attribute("data-pre-plain-text")
#                     print(f"Raw Timestamp: {timestamp}")
#                     parsed_timestamp = parse_timestamp(timestamp)

#                     if parsed_timestamp:
#                         print(f"Parsed Timestamp: {parsed_timestamp}")
#                         # Compare parsed timestamp with the date range entered by the user
#                         if start_date <= parsed_timestamp.date() <= end_date:
#                             message_type, message_info = get_message_type(message)
#                             messages_within_range.append((parsed_timestamp, sender_name, message_type, message_info))
#                             print(f"Message within range: {parsed_timestamp} - {sender_name} - {message_type} - {message_info}")
#                             print("-" * 50)
#                         else:
#                             print(f"Message out of range: {parsed_timestamp}")
#                 else:
#                     print("Non-text message detected")
#                     message_type, message_info = get_message_type(message)
#                     if message_type != "unknown":
#                         messages_within_range.append((None, sender_name, message_type, message_info))
#                         print(f"Media message detected - {message_type}: {message_info}")
#                         print("-" * 50)

#             except Exception as e:
#                 print(f"Error processing message: {e}")

#         driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight;", chat_container)
#         time.sleep(2)

#         new_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
#         if new_height == last_height:
#             break
#         last_height = new_height

#     print("Finished processing messages.")
#     return messages_within_range  # Return captured messages for PDF generation

# # Function to capture chat messages
# def capture_chat(driver, contact_name, start_date, end_date):
#     try:
#         search_box_xpath = '//div[@role="textbox"]'
#         search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

#         search_box.click()
#         search_box.send_keys(contact_name)
#         time.sleep(2)  

#         contact_xpath = f'//span[@title="{contact_name}"]'
#         contact = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, contact_xpath)))
#         actions = ActionChains(driver)
#         actions.move_to_element(contact).click().perform()
#         time.sleep(3)

#         messages_within_range = scroll_and_capture(driver, start_date, end_date)
#         return messages_within_range  # Return messages for PDF generation

#     except Exception as e:
#         print(f"Error: {e}")
#         driver.get_screenshot_as_file("error_screenshot.png")
#         return None  # Return None if there is an error

# # Main function
# # def main():
# #     driver = webdriver.Chrome()
# #     driver.get("https://web.whatsapp.com")
# #     input("Please scan the QR code and press Enter...")

# #     contact_name = input("Enter the contact name: ")
# #     start_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), '%Y-%m-%d').date()
# #     end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), '%Y-%m-%d').date()

# #     messages = capture_chat(driver, contact_name, start_date, end_date)

# #     if messages:  # Check if messages are not None
# #         generate_pdf_report(messages, contact_name)  # Generate PDF after capturing messages
# #     else:
# #         print("No messages found or an error occurred.")

# #     driver.quit()

# def main():
#     driver = webdriver.Chrome()
#     driver.get("https://web.whatsapp.com")
#     input("Please scan the QR code and press Enter...")

#     contact_name = input("Enter the contact name: ")
    
#     # User input in format YYYY-MM-DD
#     start_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), '%Y-%m-%d').date()
#     end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), '%Y-%m-%d').date()

#     messages = capture_chat(driver, contact_name, start_date, end_date)

#     if messages:  # Check if messages are not None
#         generate_pdf_report(messages, contact_name)  # Generate PDF after capturing messages
#     else:
#         print("No messages found or an error occurred.")

#     driver.quit()

# if __name__ == "__main__":
#     main()






from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fpdf import FPDF

# Replace unsupported Unicode characters with ASCII equivalents
def sanitize_message(message_info):
    replacements = {
        '\u2026': '...',  # Ellipsis
        '‘': "'", '’': "'",  # Single quotes
        '“': '"', '”': '"',  # Double quotes
        '–': '-',  # En-dash
        '—': '-',  # Em-dash
    }
    for key, value in replacements.items():
        message_info = message_info.replace(key, value)
    return message_info

# Function to generate a WhatsApp-style PDF report using FPDF
class WhatsAppChatPDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 16)
        self.cell(200, 10, f'Messages in Chat', ln=True, align='C')

    def add_message(self, timestamp, sender, message_type, message_info, is_user_message):
        # Format the timestamp
        if timestamp:
            timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        else:
            timestamp_str = "No Timestamp"

        # Sanitize message for unsupported characters
        message_info = sanitize_message(message_info)

        # Add message based on whether it's from the user or contact
        self.set_font('DejaVu', '', 12)
        
        if is_user_message:
            # User's message on the right (light blue)
            self.set_fill_color(173, 216, 230)  # Light blue background
            self.set_text_color(0, 0, 0)  # Black text
            self.multi_cell(0, 10, f"{timestamp_str} - You", align='R', fill=True)
            self.multi_cell(0, 10, f"{message_type}: {message_info}", align='R')
        else:
            # Contact's message on the left (light grey)
            self.set_fill_color(211, 211, 211)  # Light grey background
            self.set_text_color(0, 0, 0)  # Black text
            self.multi_cell(0, 10, f"{timestamp_str} - {sender}", align='L', fill=True)
            self.multi_cell(0, 10, f"{message_type}: {message_info}", align='L')

        self.ln(5)  # Add space after each message

def generate_pdf_report(messages, contact_name):
    pdf = WhatsAppChatPDF()

    # Register the DejaVu fonts
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

    pdf.add_page()

    for timestamp, sender, message_type, message_info in messages:
        # Check if the message is from the user or the contact
        is_user_message = (sender == contact_name)
        pdf.add_message(timestamp, sender, message_type, message_info, is_user_message)

    # Save the PDF
    pdf_filename = f"messages_report_{contact_name}.pdf"
    pdf.output(pdf_filename)
    print(f"PDF report generated: {pdf_filename}")

# Function to parse timestamp and handle both date formats
def parse_timestamp(timestamp):
    try:
        timestamp = timestamp.split(']')[0].strip()
        timestamp = timestamp.strip('[] ')
        
        # First, try with day/month/year (common in some WhatsApp regions)
        try:
            return datetime.strptime(timestamp, '%H:%M, %d/%m/%Y')
        except ValueError:
            # If day/month/year fails, fallback to month/day/year
            return datetime.strptime(timestamp, '%H:%M, %m/%d/%Y')

    except ValueError as e:
        print(f"Error parsing timestamp: {e}")
        return None

def scroll_and_capture(driver, start_date, end_date):
    wait = WebDriverWait(driver, 10)
    chat_container_xpath = '//*[@id="app"]/div/div[2]/div[4]'
    chat_container = wait.until(EC.presence_of_element_located((By.XPATH, chat_container_xpath)))

    last_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
    messages_within_range = []

    while True:
        messages = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')
        print(f"Found {len(messages)} messages.")

        for message in messages:
            try:
                sender_name_element = message.find_elements(By.XPATH, './/span[contains(@class, "copyable-text")]')
                sender_name = sender_name_element[0].text if sender_name_element else "Unknown"

                timestamp_element = message.find_elements(By.XPATH, './/div[@data-pre-plain-text]')
                if timestamp_element:
                    timestamp = timestamp_element[0].get_attribute("data-pre-plain-text")
                    print(f"Raw Timestamp: {timestamp}")
                    parsed_timestamp = parse_timestamp(timestamp)

                    if parsed_timestamp:
                        print(f"Parsed Timestamp: {parsed_timestamp}")
                        # Compare parsed timestamp with the date range entered by the user
                        if start_date <= parsed_timestamp.date() <= end_date:
                            message_type, message_info = get_message_type(message)
                            messages_within_range.append((parsed_timestamp, sender_name, message_type, message_info))
                            print(f"Message within range: {parsed_timestamp} - {sender_name} - {message_type} - {message_info}")
                            print("-" * 50)
                        else:
                            print(f"Message out of range: {parsed_timestamp}")
                else:
                    print("Non-text message detected")
                    message_type, message_info = get_message_type(message)
                    if message_type != "unknown":
                        messages_within_range.append((None, sender_name, message_type, message_info))
                        print(f"Media message detected - {message_type}: {message_info}")
                        print("-" * 50)

            except Exception as e:
                print(f"Error processing message: {e}")

        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop - arguments[0].clientHeight;", chat_container)
        time.sleep(2)

        new_height = driver.execute_script("return arguments[0].scrollHeight", chat_container)
        if new_height == last_height:
            break
        last_height = new_height

    print("Finished processing messages.")
    return messages_within_range  # Return captured messages for PDF generation

def get_message_type(message):
    try:
        text_element = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
        if text_element:
            return "text", text_element[0].text

        image_element = message.find_elements(By.XPATH, './/img[contains(@src, "blob:")]')
        if image_element:
            image_id = f"image_{hash(image_element[0].get_attribute('src')) % 1000:03d}"
            caption = message.find_elements(By.XPATH, './/span[contains(@class, "selectable-text")]')
            return "image", caption[0].text if caption else image_id

        return "unknown", "Unknown message type"

    except Exception as e:
        print(f"Error detecting message type: {e}")
        return "unknown", "Unknown message type"

# Function to capture chat messages
def capture_chat(driver, contact_name, start_date, end_date):
    try:
        search_box_xpath = '//div[@role="textbox"]'
        search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, search_box_xpath)))

        search_box.click()
        search_box.send_keys(contact_name)
        time.sleep(2)

        contact_xpath = f'//span[@title="{contact_name}"]'
        contact = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, contact_xpath)))
        actions = ActionChains(driver)
        actions.move_to_element(contact).click().perform()
        time.sleep(3)

        messages_within_range = scroll_and_capture(driver, start_date, end_date)
        return messages_within_range  # Return messages for PDF generation

    except Exception as e:
        print(f"Error: {e}")
        driver.get_screenshot_as_file("error_screenshot.png")
        return None  # Return None if there is an error

# Main function
def main():
    driver = webdriver.Chrome()
    driver.get("https://web.whatsapp.com")
    input("Please scan the QR code and press Enter...")

    contact_name = input("Enter the contact name: ")
    
    # User input in format YYYY-MM-DD
    start_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), '%Y-%m-%d').date()
    end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), '%Y-%m-%d').date()

    messages = capture_chat(driver, contact_name, start_date, end_date)

    if messages:  # Check if messages are not None
        generate_pdf_report(messages, contact_name)  # Generate PDF after capturing messages
    else:
        print("No messages found or an error occurred.")

    driver.quit()

if __name__ == "__main__":
    main()
