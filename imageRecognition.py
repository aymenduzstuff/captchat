import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re 
import math

def read_text(image , threshholded = False)->int :
    reader = easyocr.Reader(['en'] , gpu=False , verbose=False)

    if threshholded == False :
        contrast_stretched_image = cv2.convertScaleAbs(image, alpha=1.6 , beta= -100)
        gray_image = cv2.cvtColor(contrast_stretched_image, cv2.COLOR_BGR2GRAY)

        _, thresh_image = cv2.threshold(gray_image , 200, 255, cv2.THRESH_TOZERO)
    else :
        thresh_image = image
    
    


    text = reader.readtext(image=thresh_image  , allowlist ='0123456789')
    
    
    for (i, j , k) in text :
        if len(text) > 0  :
            return (j , k ,)
    return (0 , 0 ,)
    

def numbersonly(text):
    pattern = re.compile(r'(\d{3})')
    if text:
        match = re.search(pattern, number[0])
        if not match :
            number = " "
        return match.group(1)  # Return the first sequence of three numbers found
    else:
        return " "

def get_best(image):
    ths = [ cv2.THRESH_TOZERO , cv2.THRESH_BINARY , cv2.THRESH_TRUNC]
    contrast = 1.1
    best_param = (0 , 0 , cv2.THRESH_BINARY)
    best_res = 0

    for th in ths :
        for i in range(0, 10, 2):  # Outer loop increments by 0.1
            for j in range(-130 , 50, 30):  # Nested loop increments by 50
                contrast = 1 +(i * 0.1)

                contrast_stretched_image = cv2.convertScaleAbs(image, alpha= contrast, beta= j)
                gray_image = cv2.cvtColor(contrast_stretched_image, cv2.COLOR_BGR2GRAY)

                _, thresh_image = cv2.threshold(gray_image , 200, 255, th) 
                current = read_text(thresh_image , True)
                if current :
                    if current[1] > best_res : 
                        best_res = current[1]
                        best_param = ( contrast , j , th)
                        print(f"({i},{j})->{best_param} : text = {current[0]} , p= {current[1]}")
                        
                        if best_res >0.87 and re.search(re.compile(r'(\d{3})'), current[0]) :
                            print(best_param)
                            return current
                    
    print("defaul")      
    return (0 ,0 ,)
        
        

    
def initial_eval(imagePath) :
    image = cv2.imread(imagePath)
    y_nums = 190
    x_nums = 470
    numbers_image = image[y_nums:y_nums+320, x_nums:x_nums+320]

    parts = []
    for i in range(3):
        for j in range(3):
            part = numbers_image[i * 106: (i + 1) * 106,
                        j * 106: (j + 1) * 106]
            parts.append(part)
            
    numbers = []
    for part in parts :
        number = read_text(part )
        if number :
            numbers.append(number)
        else :
            numbers.append((0,0,))

    
    somme = sum(x[1] for x in numbers)
    eval = (somme/len(numbers)) ** 2

    for nbr in numbers  :
        if not str(nbr[0]).isdigit() and len(str(nbr[0])) == 3  :
            eval = 0
    
    print(f"numbers : {numbers} , eval : {eval}")
    return (numbers , eval , )

def get_nums(imagePath , initial_list) :
    image = cv2.imread(imagePath)
    y_nums = 190
    x_nums = 470
    numbers = image[y_nums:y_nums+320, x_nums:x_nums+320]

    parts = []
    for i in range(3):
        for j in range(3):
            part = numbers[i * 106: (i + 1) * 106,
                        j * 106: (j + 1) * 106]
            parts.append(part)
            
    textss = []
    for i ,  part in enumerate(parts) :

        if initial_list[i][1] > 0.9 and initial_list[i][0].isdigit() and len(initial_list[i][0]) == 3 :
            print(f"skipped { i }")
            textss.append(initial_list[i])
        else :
            number = read_text(part)
            if number :
                if number[1] < 0.88 :
                    number = get_best(part)
            
            textss.append(number)
    print(textss)
    return textss
    
def get_target_text(path) -> int:
    image = cv2.imread(path)
    x_text = 480 
    y_text = 145 
    text = image[y_text:y_text+30 , x_text:x_text+300]
    number:int = read_text(text)[0][-3:]
    print(f"target text is :{number}")
    return number

'''
image = cv2.imread('hello.png')
# Convert the image to grayscale
contrast_stretched_image = cv2.convertScaleAbs(image, alpha=1.3 , beta= -150)
gray_image = cv2.cvtColor(contrast_stretched_image, cv2.COLOR_BGR2GRAY)

ths = [ cv2.THRESH_TOZERO , cv2.THRESH_BINARY , cv2.THRESH_TRUNC]
imgs = []
for th in ths :
    _, thresh_image = cv2.threshold(gray_image , 200, 255, th)
    imgs.append(thresh_image)


#_, thresh_image = cv2.threshold(gray_image , 200, 255, cv2.THRESH_TOZERO_INV)


# Find contours in the thresholded image
contours, _ = cv2.findContours(trunc_thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate through the contours and filter based on area or other criteria

# Compute the area of each contour
area = cv2.contourArea(contours[0])

# You can add more criteria to filter out contours based on size, shape, etc.
if area > 150:
    # Draw the contour on the original image
    cv2.drawContours(image, [contours[0]], -1, (0, 255, 0), 2)
x, y, w, h = cv2.boundingRect(contours[0])
# Crop out the contour as another image

print( x , y , w , h )

'''
#image = cv2.imread('hello.png')
#print(get_best(image))
#contrast_stretched_image = cv2.convertScaleAbs(image, alpha=1.6 , beta= -100)
#gray_image = cv2.cvtColor(contrast_stretched_image, cv2.COLOR_BGR2GRAY)
#
#
#_, thresh_image = cv2.threshold(gray_image , 200, 255, cv2.THRESH_TOZERO)

#print(read_text(thresh_image))
#image = cv2.imread('hello.png')
initial_list = [('679', 0.7327555418014526), ('451', 0.9999878178937133), ('679', 0.988360809464087), ('382', 0.99991059619093), ('679', 0.7738277316093445), (0, 0), ('127', 0.9835945841517922), ('679', 0.8141140937805176), ('858', 0.9998223781585693)]
#get_nums("hello.png" , initial_list=initial_list)
#plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
#plt.axis('off')
#plt.show()
#












































'''CAPTCHA

 
    page.goto("https://algeria.blsspainglobal.com/DZA/account/login")
    page.get_by_role("textbox", name="Email*").click()
    page.get_by_role("button", name="Verify").click()
    page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#gmuue").get_by_role("img").click()
    page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#slhufop").get_by_role("img").click()
    page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#mvhllfzch").get_by_role("img").click()
    page.frame_locator("iframe[title=\"Verify Registration\"]").get_by_title("Refresh/Reload numbers").click()
    page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#captchaForm div").nth(4).click()
    page.get_by_text("Verify Verified Login").click()
    page.get_by_role("button", name="Login").click()

'''

'''NEXT STEP 
    page.frame_locator("iframe[title=\"Verify Registration\"]").locator("#captchaForm div").nth(4).click()
    page.get_by_text("Verify Verified Login").click()
    page.get_by_role("button", name="Login").click()
    page.get_by_role("button", name="Verify Selection").click()
    page.frame_locator("iframe[title=\"Verify Selection\"]").locator("#captcha-main-div").click()
    page.get_by_text("Verify Selection Verified").click()
    page.get_by_role("button", name="Submit").click()

'''