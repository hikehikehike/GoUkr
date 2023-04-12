import time

import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta


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


def parse_hotels(city):
    checkin_date = date.today().strftime("%d.%m.%Y")
    checkout_date = (date.today() + timedelta(days=7)).strftime("%d.%m.%Y")
    url = f"https://hotels24.ua/en/{city.name}/?lang_code=en&target=search&event=city&typeLink=hotels24&dateArrival={checkin_date}&dateDeparture={checkout_date}"
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    hotels = soup.select(".hotel-container")[:3]
    hotel_list = []
    for hotel in hotels:

        name = hotel.select_one(".hotel-name").text
        rating_element = hotel.select_one(".hotel-item-info-rating strong")
        rating = rating_element.text.strip() if rating_element else ""
        description = hotel.select_one(".hotel-description-trim").text.strip().split(".")[0]
        price = hotel.select_one(".price_recommendation").text
        image_element = hotel.select_one("img")
        image = image_element['src'][2:] if image_element else ""
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
