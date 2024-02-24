import requests 
from typing import Final
import io
from PIL import Image



token:Final = "7155017125:AAH3DaxaFQgSre2URZtOtmiHC9zHoei-UVg"
chat_id = 6322389290
def send_msg(text): 
    requests.post(url=f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}")

def send_image(path):
    url = f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={chat_id}"
    img = Image.open(fp=path)
    
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)


    files = {"photo": img_bytes}
    requests.post(url, files=files)
