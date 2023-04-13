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


# def parse_restaurant(city):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
#         'Referer': 'https://www.google.com/'
#     }
#     url = f"https://restaurantguru.com/{city}"
#     page = requests.get(url, headers=headers).content
#     soup = BeautifulSoup(page, "html.parser")
#     restaurants = soup.select(".restaurant_row")[:15]
#     restaurant_list = []
#     for restaurant in restaurants:
#         name = restaurant.select_one(".title_url").text
#         restaurant_list.append({
#             "name": name,
#             # "image": image,
#             # "price": price,
#             # "location": location,
#             # "cuisines": cuisines,
#             # "status": status,
#
#         })
#
#     print(restaurant_list)
#
#
#
# parse_restaurant("Lviv")
