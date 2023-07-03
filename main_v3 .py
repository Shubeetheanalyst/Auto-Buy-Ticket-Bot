import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ast

options = webdriver.ChromeOptions()

config                                = open(r'config.txt','r')
last_id_                              = config.read()
dx                                    = ast.literal_eval(last_id_)
extension_path                        = dx['extension_path']
config.close()

options.add_argument(fr'--load-extension={extension_path}')
driver = uc.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
print("Paste this API key into chrome Extensin,\n 6ea7d6d28a899bad115d65868e2e1e18")
time.sleep(0.3)
input("Configure API key in the chrome extension, \nThen Enter in the command prompt.....")



def available_ticket_list():
    month_count = 0
    while True:
        month_count = month_count+1
#         print(f"{month_count= }")
        time.sleep(2)
        if month_count>=2:
            break
        try:
            available_ticket = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".day-number.available.active")))
        except:
            available_ticket = []
        if len(available_ticket) == 0:
            time.sleep(1)
            next_month_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "glyphicon-chevron-right")))
            next_month_button.click()
            time.sleep(1.5)
        else:
            break
    try:
        available_ticket = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".day-number.available.active")))
    except:
        available_ticket = []
    return available_ticket

#In this function user put the month count.
# def available_ticket_list():
    # month_count = int(input("Enter the number of months to check: "))
    # while True:
    #     month_count += 1
    #     time.sleep(2)
    #     if month_count > 2:
    #         break
    #     try:
    #         available_ticket = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".day-number.available.active")))
    #     except:
    #         available_ticket = []
    #     if len(available_ticket) == 0:
    #         time.sleep(1)
    #         next_month_button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "glyphicon-chevron-right")))
    #         next_month_button.click()
    #         time.sleep(3)
    #     else:
    #         break
    # try:
    #     available_ticket = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".day-number.available.active")))
    # except:
    #     available_ticket = []
    # return available_ticket

while True:
    try:
        print("Start")
        # Demo link
        # driver.get('https://ecm.coopculture.it/index.php?option=com_snapp&view=event&id=CC6A9365-954F-41C5-9DE5-A71176DA7EB2&catalogid=6C165EEE-344F-DBCA-29C4-017A9F29BCD0&lang=it')
        # Live link
        driver.get('https://ecm.coopculture.it/index.php?option=com_snapp&view=event&id=3793660E-5E3F-9172-2F89-016CB3FAD609&catalogid=B79E95CA-090E-FDA8-2364-017448FF0FA0&lang=it')
        try:
            gdp_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.gdpr_c_r.gdpr_c_r_l > div > div > div.gdpr_col_sm_3.gdpr_r.gdpr_a_c.gdpr_f_e > a.gdpr_btn.gdpr_B_a_c.gdpr_sc')))
            gdp_button.click()
        except:
            pass
        available_ticket = available_ticket_list()
        total_tickets_ = len(available_ticket)
        print(f'Total available ticket is: {total_tickets_}')
        time.sleep(2)
        available_ticket_done = []
        while True:
            if len(available_ticket_done) == total_tickets_:
                break
            available_ticket = available_ticket_list()
            total_ticket     = len(available_ticket)
            time.sleep(2)
            for ind, ticket in enumerate(available_ticket):
                if ticket.text not in available_ticket_done:
                    time.sleep(6)
                    try:
                        ticket.click()
                    except:
                        time.sleep(5)
                        ticket.click()
                    time.sleep(2)
                    available_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".showPerformance")))
                    
                    available_ticket_no = available_button.text.split("(")[-1].split(")")[0]
                    available_button.click()
                    time.sleep(1)
                    try:
                        input_group = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#qB6B0B700-CEEA-3087-359F-016CB3FAF5CB')))
                        input_group.click()
                        # input_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'input')))
                        input_group.clear()
                        time.sleep(0.3)
                        input_group.send_keys(str(available_ticket_no))
                        modal_footer_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".modal-footer")))
                        # Iterate through the modal footers to find the add to cart button
                        for modal_footer in modal_footer_elements:
                            try:
                                add_to_cart_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary.addtocart")))
                                add_to_cart_button.click()
                                while True:
                                    if not driver.find_elements(By.CSS_SELECTOR, '.captchaviewer'):break
                                print('Captcha Solved!!!')
                                available_ticket_done.append(ticket.text)
                                # print(f"Click on Ticket : {ticket.text}")
                                print(f"This date ticket is in Cart!! : {ticket.text}")
                                time.sleep(5)
                                driver.refresh()
                                break  # Exit the loop after clicking the first add to cart button
                            except:
                                continue
                    except:
                        pass
                    break
        print("Sleep For 1 minute!!😴😴")
        time.sleep(60)
    except:
        driver.refresh()
    