from bs4 import BeautifulSoup
import requests



url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1')
title_text = title_tag.text
print(title_text)
post_photo = soup.find('img', class_='attachment-post-image')['src']
print(post_photo)
post_tag = soup.find('main').find(class_='entry-content')
post_text = post_tag.text
print(post_text)
