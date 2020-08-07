import requests
import time

for i in range(0, 1000):
    response = requests.get("http://www.jma.go.jp/jp/yoho/img/" + str(i).zfill(3) + ".png")
    if response.status_code == requests.codes.ok:
        image = response.content
        with open(str(i).zfill(3) + ".png", "wb") as img:
            img.write(image)
    time.sleep(0.5)
    