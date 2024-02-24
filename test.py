from playwright.sync_api import Playwright, sync_playwright, expect
import time
import pyautogui
import cv2
import numpy as np

def captcha_solved():
    # Read the images
    template = cv2.imread("solved.png")
    target = cv2.imread("target.png")

    # Perform template matching
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    

    # Define a threshold for matching
    threshold = 0.95

    # Find matches above the threshold
    locations = np.where(result >= threshold)

    # If there are any matches
    if len(locations[0]) > 0:
        return True 
        #for pt in zip(*locations[::-1]):
        #    cv2.rectangle(target, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
        #cv2.imshow('Target', target)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    else:
        return False 


    

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.connect_over_cdp("http://localhost:9222")
    context = browser.contexts[0]
    page = context.pages[0]
    
    start_time = time.time()

    page.goto("https://www.google.com/recaptcha/api2/demo")
    #print(page.inner_html("body"))
    page.frame_locator('[title="reCAPTCHA"]').get_by_role('checkbox', name="I'm not a robot").click()
    
    page.screenshot(type='png' , path='target.png')

    #page.frame_locator("iframe[name=\"a-upf9wdgpf97q\"]").get_by_text("I'm not a robot")
    while not captcha_solved():
        time.sleep(0.3)
        pyautogui.screenshot().save("target.png")



    # ---------------------
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"execution time : {execution_time} s")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    while True :
        run(playwright)
