import requests
from bs4 import BeautifulSoup
import time


def write_page():
    try:
        page_number, img_number = p_r()
        if img_number == 15:
            img_number = 1
            page_number += 1
        else:
            img_number += 1
    except:
        page_number, img_number = 1, 1
    with open('image_number', 'w') as f:
        f.write(str(page_number) + '\n' + str(img_number))
    return page_number, img_number


def p_r():
    with open('image_number', 'r') as num:
        num = num.read().split('\n')
        return int(num[0].strip()), int(num[1].strip())


def save_data(pic_name, file_data):
    file = open(pic_name, 'bw')
    for chunk in file_data.iter_content(4096):
        file.write(chunk)


def main_download():
    page_number, img_number = write_page()
    if page_number == 1:
        page_str = ''
    else:
        page_str = '/page' + str(page_number)

    url_primal = f'https://wallpaperscraft.ru/catalog/space/3840x2400' + str(page_str)

    page = requests.get(url_primal)
    soup1 = str(BeautifulSoup(page.text, "html.parser"))

    point1, a = 0, 0
    while a != img_number:
        point1 = soup1.find('<a class="wallpapers__link" href="', point1) + 34
        a += 1
    point2 = soup1.find('">', point1)
    url_final = soup1[point1:point2]
    flag = False
    while flag == False:
        page = requests.get('https://wallpaperscraft.ru' + url_final)
        if str(page) != '<Response [429]>':
            a = 1
            soup2 = str(BeautifulSoup(page.text, "html.parser"))
            point3 = soup2.find('class="wallpaper__image" src="') + 30
            point4 = soup2.find('"/>', point3)
            url_image = soup2[point3:point4]
            page_number, img_number = p_r()
            save_data(f'Обои_{page_number}_{img_number}.png', requests.get(url_image))
            flag = True
        else:
            print(f'Слишком много запросов! Ждите {a} секунд...')
            time.sleep(a)
            a += 2


if __name__ == "__main__":
    main_download()
