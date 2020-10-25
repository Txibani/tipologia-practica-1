from bs4 import BeautifulSoup
from datetime import date
import requests
import pandas as pd

url = "https://www.tripadvisor.es/Hotels-g187497-Barcelona_Catalonia-Hotels.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#Variables
today = date.today()
hotels = []
links = []
points = []
opinions = []
swimmingpools = []
bars = []
restaurants = []
airs = []
prices = []
stars = []
answers = []
restaurants_around = []
zones = []
longitude_latitude = []
attractions_around = []
opinions_rating = []
languages = []
ranking = []

base_url = "https://www.tripadvisor.es"

def paginationLoop():
    pagination = soup.find("div", attrs={"class": "pageNumbers"})
    total_pages = pagination.find("a", href=True, attrs={"class": "last"})["data-page-number"]
    total_length = int(total_pages)
    index = 0
    for index in list(range(index, total_length)):
        if index == 0:
            count = ""
        else:
            totals = 30 * index
            count = "oa" + str(totals) + "-"
        url_page = base_url +"/Hotels-g187497-" + count + "Barcelona_Catalonia-Hotels.html"
        page_requests = requests.get(url_page)
        soup_page = BeautifulSoup(page_requests.content, "html.parser")
        getListVariables(soup_page)

def getListVariables(soup_per_page):

    for data in soup_per_page.findAll("a", href=True, attrs={"class": "property_title"}):
        name = data.text
        link = data.get("href")
        print("Scraping page: ", link)
        hotels.append(name)
        links.append(link)

        hotel_view_url = base_url + link
        hotel_page = requests.get(hotel_view_url)
        soup_hotel_page = BeautifulSoup(hotel_page.content, "html.parser")

        prices.append(get_hotel_price(soup_hotel_page))
        #stars.append(getHotelStars(soup_hotel_page))
        answers.append(get_hotel_p_y_r(soup_hotel_page))
        restaurants_around.append(get_hotel_restaurants_around(soup_hotel_page))
        attractions_around.append(get_attractions_around(soup_hotel_page))
        #zones.append(get_zone(soup_hotel_page))

    for data in soup_per_page.findAll("div", attrs={"class": "info-col"}):
        point = data.find("a", attrs={"class": "ui_bubble_rating"})
        if point:
            points.append(point["alt"])
        else:
            points.append("0")

        opinion = data.find("a", attrs={"class": "review_count"})
        if point:
            opinions.append(opinion.text)
        else:
            opinions.append("0")

        swimmingpool = data.find("div", attrs={"data-clicksourcelabel": "Piscina"})
        if swimmingpool:
            swimmingpools.append("YES")
        else:
            swimmingpools.append("NO")

        bar = data.find("div", attrs={"data-clicksourcelabel": "Bar/Salón"})
        if bar:
            bars.append("YES")
        else:
            bars.append("NO")

        restaurant = data.find("div", attrs={"data-clicksourcelabel": "Restaurante"})
        if restaurant:
            restaurants.append("YES")
        else:
            restaurants.append("NO")

        air = data.find("div", attrs={"data-clicksourcelabel": "Aire acondicionado"})
        if air:
            airs.append("YES")
        else:
            airs.append("NO")


def get_hotel_price(soup):
    price = soup.find("div", attrs={"class": "CEf5oHnZ"})
    if price:
        return price.text
    else:
        return "unknown"

def get_hotel_p_y_r(soup):
    answer = soup.find("span", attrs={"class": "_1aRY8Wbl"})
    if answer:
        return answer.text
    else:
        return 0

def get_hotel_restaurants_around(soup):
    restaurant = soup.find("span", attrs={"class": "TrfXbt7b"})
    if restaurant:
        return restaurant.text
    else:
        return 0

def get_attractions_around(soup):
    attraction = soup.find("span", attrs={"class": "_1WE0iyL_"})
    if attraction:
        return attraction.text
    else:
        return 0


paginationLoop()


df = pd.DataFrame({
    "Hotel name": hotels,
    "Precio/noche": prices,
    "Puntuación Tripadvisor": points,
    "Número opiniones": opinions,
    "Piscina": swimmingpools,
    "Bar": bars,
    "Restaurante": restaurants,
    "Aire acondicionado": airs,
    "Preguntas y Respuestas": answers,
    "Número restaurantes cerca": restaurants_around,
    "Atracciones cerca": attractions_around,
    "Date": today
    })
df.to_csv("./dataset/hotels_dataset.csv", index=True, encoding="utf-8")