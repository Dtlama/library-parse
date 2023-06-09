from bs4 import BeautifulSoup
import json
import requests
import lxml
import os


def check_for_redirect(response):
    for resp in response.history:
        if resp.status_code == 302:
            raise requests.exceptions.HTTPError


def download_book(url_download, filename, folder="books/"):
    response = requests.get(url_download)
    check_for_redirect(response)
    response.raise_for_status()
    filename = f'{filename}.txt'
    file_path = os.path.join('books', filename)

    with open(file_path, 'w', encoding='UTF8') as file:
        file.write(response.text)
    return file_path


def get_book_name_and_author(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_text = soup.find('body').find('table').find('h1')
    book_name = book_text.text.split("::", 1)[0].strip()
    book_author = book_text.text.split("::", 1)[1].strip()
    return book_name, book_author


def get_book_image(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    image_url = soup.find('body').find('table').find('div', class_='bookimage').find('img')['src']
    image_url = 'https://tululu.org' + image_url
    return image_url


def download_image(url, filename, folder="images/"):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    if url == "https://tululu.org/images/nopic.gif":
        filename = 'nopic.gif'
    else:
        filename = f'{filename}.jpg'
    file_path = os.path.join('images', filename)

    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

#https://tululu.org/b5/
if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    for number in range(1, 11):
        try:
            url = 'https://tululu.org/b{}/'.format(number)
            book_name, book_author = get_book_name_and_author(url)
            image_url = get_book_image(url)
            print(image_url)
            download_image(image_url, number)
            url_download = 'http://tululu.org/txt.php?id={}'.format(number)
            file_path = download_book(url_download, book_name)
            print(book_name, image_url)
        except requests.exceptions.HTTPError:
            print("Перенаправление")
