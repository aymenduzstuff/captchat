from playwright.sync_api import Playwright, sync_playwright, expect , TimeoutError , Error
from playwright.sync_api import Locator
from imageRecognition import get_nums , get_target_text , initial_eval
import time , traceback
import notifier 



normalchildren  = []
shiftchildren = []




def solve_captcha(page , nums , target ) :
    coordinates = {
    0:(520 , 230,),
    1:(630 , 233,),
    2:(735 , 240,),

    3:(520 , 350,),
    4:(630 , 355,),
    5:(740 , 340,),

    6:(520 , 460 ,),
    7:(630 , 455,),
    8:(740 , 462,)
                    }
    for i , (n, _) in enumerate(nums) :

        if n==target :
            page.mouse.click(coordinates[i][0] ,coordinates[i][1] )
    

def click(page , btn:str):
    sptlchars =  ['~', ')', '*', '#', '^', '%' , '&', '(', '@', '!', '$', '_', '+']
    if btn.isupper() or btn in sptlchars :
        page.get_by_role("button", name="Shift").first.click()
        page.get_by_role("button", name=btn, exact=True).click()
        page.get_by_role("button", name="Shift").first.click()
    else : 
        page.get_by_role("button", name=btn, exact=True).click()

def update_keyboard_vars(page):
    global normalchildren
    normalchildren = page.query_selector('div[name="normal"]').query_selector_all('button')
    global shiftchildren
    shiftchildren = page.query_selector('div[name="shift"]').query_selector_all('button')
    print(f"lengths : {len(normalchildren) }\n\n{len(shiftchildren)}")

def handle_captcha(page ) : 
    print("frame found") 
    target = None
    lowest = 0
    nums = []
    while lowest < 0.7 : 
        #with page.expect_navigation():
        #    frame.wait_for_selector("button[title='Refresh/Reload numbers']")

        time.sleep(3)
        page.screenshot(path="hello.png")
        initial_scan = initial_eval('hello.png')

        initial_list = initial_scan[0]
        initial_value = initial_scan[1]

        if initial_value < 0.6 :

            #page.frame_locator("iframe[title=\"Verify Selection\"]").get_by_text("Reload Images")
            #page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Refresh/Reload numbers")
            page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#captchaForm div").nth(3).click()
            if not page.frame_locator("iframe[title=\"Verify Selection\"]").get_by_role("alert") :
                print("wasn't solved")
                page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Refresh/Reload numbers").click()
                time.sleep(2)
                handle_captcha(page)

            continue
        nums = get_nums("hello.png" , initial_list)
        target = get_target_text("hello.png")
        list_lowest = 1
        for i in range(9):
            if nums[i]:
                if nums[i][1] < list_lowest :
                    list_lowest = nums[i][1]
        lowest = list_lowest 
        if lowest < 0.7 :
            page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Refresh/Reload numbers").click()
            time.sleep(2)
    
    

        
    solve_captcha(page , nums , target )
    page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Submit Selection").click()
    time.sleep(2)
    if not page.query_selector('#btnVerified') :
        
        print("wasn't solved")
        handle_captcha(page)


def run(playwright: Playwright ) -> None:
    try :
        browser = playwright.chromium.launch(headless=False , slow_mo=300 )
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://algeria.blsspainglobal.com/DZA/account/login" , timeout= 40000)
        #page.goto("https://algeria.blsspainglobal.com/DZA/Account/LogIn?ReturnUrl=%2FDZA%2Fbls%2Fvtv")
        time.sleep(2)
        page.get_by_role("textbox", name="Email*").click()
        page.get_by_role("textbox", name="Email*").fill("aymene22k@gmail.com")
    
        page.get_by_role("textbox", name="Password*").click()
        #parent : 
        #page.locator(".fakepasswordicon").first.click()
        
        password = "12345abcdE#2"
        #print(len(shiftchildren))
        #
        for i in password : 
            click(page , i)
        
        page.get_by_role("button", name="Accept").click()
            

        
        page.get_by_role("button", name="Verify").click()
        
    

        page.wait_for_selector("iframe[title='Verify Registration']")

        
        if page.frame_locator("iframe[title=\"Verify Registration\"]") :
            handle_captcha(page)
            

        print("captcha solved")

    except Error as e :
        notifier.send_msg(e)
        
        page.screenshot(path="problem.png")
        notifier.send_image("problem.png")
        print(f"exception occured in first part : \n{e}")
        traceback.print_exc()

        #page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Verify Registration").screenshot(path="capa.png")
    
    try : 
        

        page.get_by_role("button", name="Login").click()

        page.get_by_role("button", name="Close").click()
        page.get_by_role("link", name="Book New Appointment").click()
        page.get_by_role("button", name="Verify Selection").click()

        if page.frame_locator("iframe[title=\"Verify Registration\"]") :
            handle_captcha(page)

        page.get_by_role("button", name="Submit").click()
        page.get_by_role("listbox", name="Visa Type*").get_by_label("select").locator("span").click()
        page.get_by_role("option", name="Schengen Visa").click()
        page.get_by_role("listbox", name="Visa Sub Type*").get_by_label("select").locator("span").click()
        page.locator("#VisaSubType2_listbox").get_by_role("option", name="Schengen Visa").click()
        page.get_by_role("listbox", name="Location*").get_by_role("option").click()
        page.get_by_role("option", name="Algiers").click()
        page.get_by_role("listbox", name="Appointment Category*").get_by_label("select").click()
        page.get_by_role("option", name="Normal").click()
        page.get_by_role("button", name="Submit").click()

        if not page.get_by_text("No Appointments Available") : 
            notifier.send_msg("rehom fet7o")
        

        page.pause()
    except Error as e :
        print("exception occured in second part  : ")
        traceback.print_exc()
        print(f"somethign went wrong : {e}")
        page.pause()


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
