from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://www.kinopoisk.ru/lists/movies/top_1000/')

input("CAPTCHA и нажмите Enter...")

# Получаем HTML-код страницы после прохождения CAPTCHA
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

movies = []

for movie_div in soup.find_all('div', class_='styles_root__ti07r'):
    # Название фильма
    title_tag = movie_div.find('span', class_='styles_mainTitle__IFQyZ')
    title = title_tag.text if title_tag else 'N/A'

    # Год выпуска
    secondary_text = movie_div.find('span', class_='desktop-list-main-info_secondaryText__M_aus')
    year = secondary_text.text.split(',')[1].strip().split(' ')[0] if secondary_text else 'N/A'

    # Страна и жанр
    additional_info = movie_div.find_all('span', class_='desktop-list-main-info_truncatedText__IMQRP')
    country_genre = additional_info[0].text.split('•')[0].strip() if additional_info else 'N/A'

    # Полное имя режиссера
    director = 'N/A'
    if additional_info:
        for text in additional_info:
            if "Режиссёр:" in text.text:
                director = text.text.split('Режиссёр:')[1].strip()
                break

    # Рейтинг
    rating_tag = movie_div.find('span', class_='styles_kinopoiskValue__nkZEC')
    rating = rating_tag.text if rating_tag else 'N/A'

    # Проверка на наличие кнопок «Трейлер» и «Смотреть»
    has_trailer = bool(movie_div.find('button', string="Трейлер"))
    has_watch = bool(movie_div.find('button', string="Смотреть"))

    # Добавляем данные о фильме в список
    movies.append({
        'Title': title,
        'Year': year,
        'Country/Genre': country_genre,
        'Director': director,
        'Rating': rating,
        'Has Trailer': has_trailer,
        'Has Watch Option': has_watch
    })

df = pd.DataFrame(movies)
df.to_csv('top_1000_movies.csv', index=False)

print("Data scraped and saved to 'top_1000_movies.csv'")
driver.quit()
