from time import sleep
import requests
from bs4 import BeautifulSoup
import csv
import logging
from typing import List, Optional
from itertools import zip_longest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
names = []
price = []
Kilométrage = []
Mise_en_circulation = []
Énergie = []
Boite_vitesse = []
Puissance_fiscale = []
Transmission = []
Carrosserie = []
Date_de_annonce = []
Gouvernorat = []
Marque = []
Modèle = []
Génération = []
Couleur_extérieure = []
Couleur_intérieure = []
Sellerie = []
Nombre_de_places = []
Nombre_de_portes = []
Moteur = []
Puissance = []
Énergie = []
Boite_vitesse = []
Puissance_fiscale = []
Transmission = []
Cylindrée = []


class AutoMobileOccasionScraper:
    def __init__(
        self, base_url: str = "https://www.automobile.tn/fr/occasion/"
    ) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        # Add headers to mimic browser behavior
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

    def get_page_content(self, url: str, retries: int = 3) -> Optional[str | bytes]:
        """Fetch URL content with retry mechanism and error handling."""
        for attempt in range(retries):
            try:
                response = self.session.get(url)
                response.raise_for_status()
                # Add small delay to be respectful to the server
                sleep(1)
                return response.content

            except requests.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed for URL {url}: {str(e)}")
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
                else:
                    sleep(2**attempt)  # Exponential backoff

    def get_car_links(self, i=0):
        """
        Extract constructor URLs.
        These names are within links href
        """

        content = self.get_page_content(self.base_url + str(i))
        if not content:
            return []

        soup = BeautifulSoup(content, "lxml")
        cars_href_list = []
        car_a_elements = soup.select("div.articles a.occasion-link-overlay")
        for a in car_a_elements:
            cars_href_list.append(a.get("href"))
        return [
            self.base_url + "/".join(car_href.split("/")[3:])
            for car_href in cars_href_list
        ]

    def get_technical_file_links(self, constructor_url: str) -> List[str]:
        """Get technical file links for a specific constructor."""
        page_content = self.get_page_content(constructor_url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, "lxml")
        technical_file_links = []
        versions = soup.select("div.versions-item a")
        for version in versions:
            href = version.get("href", "")
            if not href:
                continue
            href_parts = href.split("/")
            if len(href_parts) > 5:
                # hedha ya3ni raw tech file url hne ki nenzel 3al karhba
                # this means that the tech file is right here
                technical_file_links.append(self.base_url + "/".join(href_parts[3:]))
                print(self.base_url + "/".join(href_parts[3:]))
            else:
                versions_link = self.base_url + "/".join(href_parts[3:])
                print("going a little deeper!\n")
                print(f"this is a versions link {versions_link}\n")
                page_content = self.get_page_content(versions_link)
                if not page_content:
                    return []
                soup = BeautifulSoup(page_content, "lxml")
                versions = soup.select("td.version a")
                print(versions)
                for version in versions:
                    href = version.get("href", "")
                    if not href:
                        continue
                    href_parts = href.split("/")
                    technical_file_links.append(
                        self.base_url + "/".join(href_parts[3:])
                    )
                    print(self.base_url + "/".join(href_parts[3:]))

        return technical_file_links

    def extract_car_details(self, car_link: str) -> any:
        """Extract detailed information about a specific car."""
        page_content = self.get_page_content(car_link)
        if not page_content:
            return {}

        soup = BeautifulSoup(page_content, "lxml")
        prix = (
            soup.select_one("div.price").text.strip()
            if soup.select_one("div.price")
            else ""
        )
        name = (
            soup.select_one("h1.occasion-title").text.strip()
            if soup.select_one("h1.occasion-title")
            else "unkonwn"
        )
        print("name ", name)
        print("prix  ", prix)
        spec_names = soup.select("div.box li span.spec-name")
        spec_values = soup.select("div.box li span.spec-value")
        specs_dict = dict()
        for i in range(len(spec_names)):
            specs_dict[spec_names[i].text.strip()] = spec_values[i].text.strip()

        print("the dict *****: \n\n")
        for spec_name in spec_names:
            print(spec_name.text.strip())
        for spec_value in spec_values:
            print(spec_value.text.strip())

        price.append(prix)
        names.append(name)
        Kilométrage.append(spec_values[0].text.strip())
        print("kilometrage ", spec_values[0].text.strip())
        print("Mise_en_circulation", spec_values[1].text.strip())
        print("Énergie", spec_values[2].text.strip())
        print("Boite_vitesse", spec_values[3].text.strip())
        print("Puissance_fiscale", spec_values[4].text.strip())
        Mise_en_circulation.append(spec_values[1].text.strip())
        Énergie.append(spec_values[2].text.strip())
        Boite_vitesse.append(spec_values[3].text.strip())
        Puissance_fiscale.append(spec_values[4].text.strip())
        Transmission.append(spec_values[5].text.strip())
        Carrosserie.append(spec_values[6].text.strip())
        Date_de_annonce.append(spec_values[7].text.strip())
        Gouvernorat.append(spec_values[8].text.strip())
        Marque.append(spec_values[9].text.strip())
        Modèle.append(spec_values[10].text.strip())
        Génération.append(spec_values[11].text.strip())
        Couleur_extérieure.append(spec_values[12].text.strip())
        Couleur_intérieure.append(spec_values[13].text.strip())
        Sellerie.append(spec_values[14].text.strip())
        Nombre_de_places.append(spec_values[15].text.strip())
        Nombre_de_portes.append(spec_values[16].text.strip())
        Moteur.append(spec_values[17].text.strip())
        Puissance.append(spec_values[18].text.strip())
        Cylindrée.append(spec_values[23].text.strip())


def main():
    # scraper = AutoMobileOccasionScraper()
    # #     print(cars)
    # for i in range(174):
    #     cars = scraper.get_car_links(i)
    #     print(cars)
    #     logger.info(f"Found {len(cars)} cars")

    #     # testing awel model
    #     for car in cars:
    #         logger.info(f"Processing car sales: {car}")
    #         # Process the car file
    #         scraper.extract_car_details(car)

    #     file_list = [
    #         names,
    #         price,
    #         Kilométrage,
    #         Mise_en_circulation,
    #         Énergie,
    #         Boite_vitesse,
    #         Puissance_fiscale,
    #         Transmission,
    #         Carrosserie,
    #         Date_de_annonce,
    #         Gouvernorat,
    #         Marque,
    #         Modèle,
    #         Génération,
    #         Couleur_extérieure,
    #         Couleur_intérieure,
    #         Sellerie,
    #         Nombre_de_places,
    #         Nombre_de_portes,
    #         Moteur,
    #         Puissance,
    #         Cylindrée,
    #     ]

    #     exported = zip_longest(*file_list, fillvalue="")
    #     with open(
    #         "full_cars_occasion_dataset.csv", "a", newline="", encoding="utf-8"
    #     ) as file:
    #         wr = csv.writer(file)
    #         wr.writerow(
    #             [
    #                 "name",
    #                 "prix",
    #                 "kilometrage",
    #                 "mise_en_circulation",
    #                 "energie",
    #                 "boite_vitesse",
    #                 "puissance_fiscale",
    #                 "transmission",
    #                 "carrosserie",
    #                 "date_de_annonce",
    #                 "gouvernorat",
    #                 "marque",
    #                 "modele",
    #                 "generation",
    #                 "couleur_exterieure",
    #                 "couleur_interieure",
    #                 "sellerie",
    #                 "nombre_de_places",
    #                 "nombre_de_portes",
    #                 "moteur",
    #                 "puissance",
    #                 "cylindre",
    #             ]
    #         )

    #     wr.writerows(exported)

    scraper = AutoMobileOccasionScraper()

    # List to store all data
    file_list = [
        names,
        price,
        Kilométrage,
        Mise_en_circulation,
        Énergie,
        Boite_vitesse,
        Puissance_fiscale,
        Transmission,
        Carrosserie,
        Date_de_annonce,
        Gouvernorat,
        Marque,
        Modèle,
        Génération,
        Couleur_extérieure,
        Couleur_intérieure,
        Sellerie,
        Nombre_de_places,
        Nombre_de_portes,
        Moteur,
        Puissance,
        Cylindrée,
    ]

    # Open the file outside the loop
    with open(
        "automobile_tn_occasion_dataset3.csv", "a", newline="", encoding="utf-8"
    ) as file:
        wr = csv.writer(file)

        # Write headers first
        wr.writerow(
            [
                "name",
                "prix",
                "kilometrage",
                "mise_en_circulation",
                "energie",
                "boite_vitesse",
                "puissance_fiscale",
                "transmission",
                "carrosserie",
                "date_de_annonce",
                "gouvernorat",
                "marque",
                "modele",
                "generation",
                "couleur_exterieure",
                "couleur_interieure",
                "sellerie",
                "nombre_de_places",
                "nombre_de_portes",
                "moteur",
                "puissance",
                "cylindre",
            ]
        )

        scraper = AutoMobileOccasionScraper()

        # Process cars
        for i in range(174):
            cars = scraper.get_car_links(i)
            logger.info(f"Found {len(cars)} cars")

            for car in cars:
                logger.info(f"Processing car sales: {car}")
                # Process the car file
                scraper.extract_car_details(car)

        # Use zip_longest to handle potentially unequal list lengths
        exported = zip_longest(*file_list, fillvalue="")

        # Write rows to the CSV
        wr.writerows(exported)

    # Print lengths after processing
    print("Lengths of different lists:")
    print(f"names: {len(names)}")
    print(f"price: {len(price)}")
    print(f"Kilométrage: {len(Kilométrage)}")
    print(f"Mise_en_circulation: {len(Mise_en_circulation)}")
    print(f"Carrosserie: {len(Carrosserie)}")
    print(f"Date_de_annonce: {len(Date_de_annonce)}")
    print(f"Gouvernorat: {len(Gouvernorat)}")
    print(f"Marque: {len(Marque)}")
    print(f"Modèle: {len(Modèle)}")
    print(f"Génération: {len(Génération)}")
    print(f"Couleur_extérieure: {len(Couleur_extérieure)}")
    print(f"Couleur_intérieure: {len(Couleur_intérieure)}")
    print(f"Sellerie: {len(Sellerie)}")
    print(f"Nombre_de_places: {len(Nombre_de_places)}")
    print(f"Nombre_de_portes: {len(Nombre_de_portes)}")
    print(f"Moteur: {len(Moteur)}")
    print(f"Puissance: {len(Puissance)}")
    print(f"Cylindrée: {len(Cylindrée)}")


if __name__ == "__main__":
    main()
