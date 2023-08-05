from bs4 import BeautifulSoup
import argparse
import requests
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


def get_book_comments(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_comments = soup.find('body').find('table').find_all(class_='texts')
    book_comments_text = []
    for book_comment in book_comments:
        comment = book_comment.get_text('span').split('span')[2]
        book_comments_text.append(comment)
    return book_comments_text


def get_book_genre(url):
    response = requests.get(url)
    check_for_redirect(response)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    book_genres = soup.find('body').find('table').find('span', class_='d_book').find('a').text
    return book_genres


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


if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
    os.makedirs('images', exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int)
    parser.add_argument('--end_id', type=int)
    arguments = parser.parse_args()
    for number in range(arguments.start_id, arguments.end_id):
        try:
            url = 'https://tululu.org/b{}/'.format(number)
            book_name, book_author = get_book_name_and_author(url)
            image_url = get_book_image(url)
            download_image(image_url, number)
            book_comments = get_book_comments(url)
            book_genres = get_book_genre(url)
            url_download = 'http://tululu.org/txt.php?id={}'.format(number)
            file_path = download_book(url_download, book_name)
            print("Заголовок:" + book_name, book_genres)
        except requests.exceptions.HTTPError:
            print("Перенаправление")
