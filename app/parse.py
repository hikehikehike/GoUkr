import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

from app.models import Pages


def generate_google_map_link(name):
    base_url = "https://www.google.com/maps/search/?api=1&query="
    query = name.replace(" ", "+")
    return base_url + query


def generate_booking_link(name):
    checkin_date = date.today().strftime("%Y-%m-%d")
    checkout_date = (date.today() + timedelta(days=7)).strftime("%Y-%m-%d")
    base_url = "https://www.booking.com/searchresults.ru.html?ss="
    query = name.replace(" ", "+")
    time_ = f"checkin={checkin_date}&checkout={checkout_date}"
    return base_url + query + "&" + time_


def generate_restaurant_tripadvisor_link(name, city):
    base_url = "https://www.tripadvisor.com/Search?q="
    restaurant = name.replace(" ", "+")
    return base_url + restaurant + "&geo=" + city


def parse_hotels(city):

    proxies = {
        "http": "http://91.241.217.58:9090",
    }

    checkin_date = date.today().strftime("%d.%m.%Y")
    checkout_date = (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    url = f"https://hotels24.ua/en/{city.name}/?lang_code=en&target=search&event=city&typeLink=hotels24&dateArrival={checkin_date}&dateDeparture={checkout_date}"
    page = requests.get(url, proxies=proxies).content

    soup = BeautifulSoup(page, "html.parser")
    hotels = soup.select(".hotel-container")[:3]
    hotel_list = []
    for hotel in hotels:

        name = hotel.select_one(".hotel-name").text
        rating_element = hotel.select_one(".hotel-item-info-rating strong")
        rating = rating_element.text.strip() if rating_element else ""
        description = (
            hotel.select_one(".hotel-description-trim").text.strip().split(".")[0]
        )
        price = hotel.select_one(".price_recommendation").text
        image_element = hotel.select_one("img")
        image = image_element["src"][2:] if image_element else ""
        location = generate_google_map_link(name)
        view_deal = generate_booking_link(name)

        hotel_list.append(
            {
                "name": name,
                "rating": rating,
                "description": description,
                "price": price,
                "image": image,
                "location": location,
                "view_deal": view_deal,
            }
        )
    return hotel_list


def parse_restaurant(city):
    proxies = {
        "http": "http://195.137.167.109:80",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "TE": "Trailers",
    }

    params = {
        "utm_source": "google",
        "utm_medium": "organic",
        "utm_campaign": "organic",
        "utm_content": "",
        "sort": "rating",
    }

    url = f"https://restaurantguru.com/{city.name}"
    page = requests.get(url, headers=headers, proxies=proxies, params=params).content

    page_text = str(page)  # конвертируем переменную page в строку, если она не является строкой
    page_obj = Pages(text=page_text)  # создаем экземпляр модели Pages
    page_obj.save()  # сохраняем экземпляр модели в базе данных

    soup = BeautifulSoup(page, "html.parser")
    restaurants = soup.select(".restaurant_row")[:15]
    restaurant_list = []
    for restaurant in restaurants:
        name = restaurant.select_one(".title_url").text
        image_element = restaurant.select_one("img")
        image = image_element["data-src"] if image_element else ""
        price = len(restaurant.select_one(".cost").find_all("i"))
        location = generate_restaurant_tripadvisor_link(name, city.name)
        cuisines = restaurant.select_one(".cuisine").text
        if restaurant.select_one(".now_closed_r") is not None:
            status = restaurant.select_one(".now_closed_r").text
        else:
            status = restaurant.select_one(".green").text

        restaurant_list.append(
            {
                "name": name,
                "image": image,
                "price": price,
                "location": location,
                "cuisines": cuisines,
                "status": status,
            }
        )

    return restaurant_list
