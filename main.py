import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook


def save_to_exel(item):

    file_name = 'D:\OneDrive\Рабочий стол\est.xlsx'
    df = pd.DataFrame(item)
    df.to_excel(file_name, index=False)


def parse_offers(car_type="", numOfOffers=5):
    url = "https://kolesa.kz/cars"

    # i  -  страница на сайте
    i = 1
    item = {}
    # k  -  количество оферов
    k = 0
    while k != numOfOffers:
        if k == 0:
            try:
                response = requests.get(url=url+f"/{car_type}/").text

            except Exception as ex:
                save_to_exel(item)
                print(ex)
                break
        else:
            try:
                response = requests.get(url=url + f"/{car_type}" + f"/?page={i}/").text
            except Exception as ex:
                save_to_exel(item)
                print(ex)
                break

        soup = BeautifulSoup(response, 'html.parser')
        div = soup.find('div', class_='a-list')
        offerInfoLink = div.find_all('a', class_='a-card__link')
        offerInfoLink = div.find_all("a", class_="a-card_-link")

        for t in offerInfoLink:
            #желаемое количество оферов
            if (k == numOfOffers):
                break

            # открываю ссылку на офер с которого буду брать инфу
            link = "https://kolesa.kz" + t.get("href")
            offerLink = requests.get(url=link).text
            soup = BeautifulSoup(offerLink, "html.parser")
            offer = soup.find("div", class_="offer")
            k += 1
            print(k)
            # car brand
            carBrand = ""
            try:
                carBrand = offer.find("span", itemprop="brand").text
            except Exception as ex:
                print(ex)
            # car name
            carName = ""
            try:
                carName = offer.find("span", itemprop="name").text
            except Exception as ex:
                print(ex)

            # car year
            carYear = None
            try:
                carYear_text = int(offer.find("span", class_="year").text)
                # делаю год машины интеджером
                carYear = int("".join([char for char in str(carYear_text) if char.isdigit()]))
            except Exception as ex:
                print(ex)


            item[k]=({'id': k,
                         "carBrand": carBrand,
                         "carName": carName,
                         "carYear": carYear,
                         "OfferLink": link})
            print(item[k])
        i += 1
    print(item)
    save_to_exel(item)


def main():
    # введите название компании желаемой машины
    parse_offers(car_type="toyota", numOfOffers=3)


def test(data_filtered=None):
   print("test")

if __name__ == "__main__":
    main()
