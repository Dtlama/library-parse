import requests
import os


for number in range(1, 11):
    url = f'https://tululu.org/txt.php?id={number}'
    response = requests.get(url)
    response.raise_for_status()
    filename = f'id{number}.txt'
    file_path = os.path.join('books', filename)

    with open(file_path, 'w', encoding='UTF8') as file:
        file.write(response.text)

if __name__ == '__main__':
    os.makedirs('books', exist_ok=True)
