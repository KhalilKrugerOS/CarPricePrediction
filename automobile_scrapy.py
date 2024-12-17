from time import sleep
import requests
from bs4 import BeautifulSoup
import csv
import logging
from typing import List, Dict, Optional
from itertools import zip_longest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
names = []
disponobilite = []
Carrosserie = []
garanties = []
nombredePlaces = []
nombreDePortes = []
motorisation = []
nombredeCylindres = []
energie = []
puissancefiscale = []
puissance = []
couple = []
cylindre = []
boite = []
nombreDeRapports = []
transmission = []
longueur = []
largeur = []
hauteur = []
volumeDeCoffre = []
performance = []
vitesseMax = []
consommationUrbaine = []
consommationExtraUrbaine = []
consommationMixte = []
airbags = []
antiPatinage = []
aideAuStationnement = []
assistanceAuFreinage = []
feuxaLED = []
jantes = []
ecran = []
climatisation = []
fermetureCentralisee = []
retroviseurInterieur = []
vitresElectriques = []
retroviseurExterieur = []
autoradio = []
connectivite = []
ecran = []
vitres = []
volant = []
volantReglable = []
price = []


class AutoMobileScraper:
    def __init__(self, base_url: str = "https://www.automobile.tn/fr/neuf/") -> None:
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

    def get_constructors_links(self):
        """
        Extract constructor URLs.
        These names are within links href
        """
        src = self.get_page_content(self.base_url)
        if not src:
            return []
        content = self.get_page_content(self.base_url)
        soup = BeautifulSoup(content, "lxml")
        constructor_href_list = []
        constructor_a_elements = soup.select("div.brands-list a")
        for a in constructor_a_elements:
            constructor_href_list.append(a.get("href"))

        return [
            self.base_url + constructor_href.split("/")[3]
            for constructor_href in constructor_href_list
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

    def extract_car_details(self, technical_file_url: str) -> any:
        """Extract detailed information about a specific car."""
        page_content = self.get_page_content(technical_file_url)
        if not page_content:
            return {}

        soup = BeautifulSoup(page_content, "lxml")
        prix = (
            soup.select_one("div.buttons div span").text.strip()
            if soup.select_one("div.version-details div span")
            else ""
        )
        name = (
            soup.select_one("h3.page-title").text.strip()
            if soup.select_one("h3.page-title")
            else "unkonwn"
        )
        specs = soup.select("div#specs.technical-details th")
        print(specs)
        # inialise with None to avoid index out of range
        spec_values = [None] * 100
        spec_values_elmnts = soup.select("div#specs.technical-details td")
        specs_dict = dict()
        new_specs = soup.select("tr")
        print("attrs ", new_specs[1].td.text)
        for tr in new_specs:
            if tr.attrs["td"]:
                specs_dict[tr.attrs["td"].text.strip()] = tr.attrs["td"].text.strip()
        print(specs_dict)
        for i in range(len(spec_values_elmnts)):
            spec_values[i] = spec_values_elmnts[i]
        # try:
        names.append(name)
        price.append(prix)
        spec_values.insert(0, 0)
        disponobilite.append(spec_values[1].text.strip())
        Carrosserie.append(spec_values[2].text.strip())
        garanties.append(spec_values[3].text.strip())
        nombredePlaces.append(spec_values[4].text.strip())
        nombreDePortes.append(spec_values[5].text.strip())
        nombredeCylindres.append(spec_values[6].text.strip())
        energie.append(spec_values[7].text.strip())
        puissancefiscale.append(spec_values[8].text.strip())
        puissance.append(spec_values[9].text.strip())
        couple.append(spec_values[10].text.strip())
        cylindre.append(spec_values[11].text.strip())
        boite.append(spec_values[12].text.strip())
        nombreDeRapports.append(spec_values[13].text.strip())
        transmission.append(spec_values[14].text.strip())
        longueur.append(spec_values[16].text.strip())
        largeur.append(spec_values[17].text.strip())
        hauteur.append(spec_values[18].text.strip())
        volumeDeCoffre.append(spec_values[18].text.strip())
        performance.append(spec_values[19].text.strip())
        # vitesseMax.append(spec_values[20].text.strip())
        # consommationUrbaine.append(spec_values[21].text.strip())
        # consommationExtraUrbaine.append(spec_values[22].text.strip())
        # consommationMixte.append(spec_values[23].text.strip())
        # airbags.append(spec_values[25].text.strip())
        # antiPatinage.append(spec_values[29].text.strip())
        # aideAuStationnement.append(spec_values[30].text.strip())
        # assistanceAuFreinage.append(spec_values[31].text.strip())
        # feuxaLED.append(spec_values[38].text.strip())
        # jantes.append(spec_values[39].text.strip())
        # autoradio.append(spec_values[42].text.strip())
        # connectivite.append(spec_values[43].text.strip())
        # ecran.append(spec_values[44].text.strip())
        # vitres.append(spec_values[53].text.strip())
        # volant.append(spec_values[54].text.strip())
        # volantReglable.append(spec_values[55].text.strip())
        # climatisation.append(spec_values[57].text.strip())
        # fermetureCentralisee.append(spec_values[58].text.strip())
        # retroviseurExterieur.append(spec_values[61].text.strip())
        # retroviseurInterieur.append(spec_values[62].text.strip())
        # vitresElectriques.append(spec_values[63].text.strip())
        # except Exception as e:
        #     logger.error(
        #         f"Error extracting car details from {technical_file_url}: {str(e)}")
        #     return


def main():
    scraper = AutoMobileScraper()

    # Get all constructors
    constructors = scraper.get_constructors_links()
    logger.info(f"Found {len(constructors)} constructors")

    # testing awel model
    for constructor in constructors[:2]:
        logger.info(f"Processing constructor: {constructor}")
        # Get technical file links for this constructor
        technical_files = scraper.get_technical_file_links(constructor)
        logger.info(f"Found {len(technical_files)} technical files\n")
        # Process first technical file
        for technical_file in technical_files:
            scraper.extract_car_details(technical_file)

    file_list = [
        names,
        price,
        Carrosserie,
        garanties,
        nombredePlaces,
        nombreDePortes,
        nombredeCylindres,
        energie,
        puissancefiscale,
        puissance,
        couple,
        cylindre,
        boite,
        nombreDeRapports,
        transmission,
        longueur,
        largeur,
        hauteur,
        volumeDeCoffre,
        performance,
    ]
    # not the same features for all cars
    #    , couple, cylindre, boite, nombreDeRapports, transmission,
    #  longueur, largeur, hauteur, volumeDeCoffre, performance, vitesseMax, consommationUrbaine,
    #  consommationExtraUrbaine, consommationMixte, airbags, antiPatinage, aideAuStationnement,
    #  assistanceAuFreinage, feuxaLED, jantes, autoradio, connectivite, ecran, vitres, volant,
    #  volantReglable, climatisation, fermetureCentralisee, retroviseurExterieur, retroviseurInterieur,
    #  vitresElectriques]
    exported = zip_longest(*file_list, fillvalue="")
    with open("automobile_dataset.csv", "w", newline="", encoding="utf-8") as file:
        wr = csv.writer(file)
        wr.writerow(
            [
                "name",
                "prix",
                "carosserie",
                "garantie",
                "nombre de places",
                "nombre de portes",
                "nombredeCylindres",
                "energie",
                "puissance fiscale",
                "puissance",
                "couple",
                "cylindre",
                "boite",
                "nombre de rapports",
                "transmission",
                "longueur",
                "largeur",
                "hauteur" "volume de coffre",
                "performance",
            ]
        )
        #  , "couple", "cylindre",
        #  "boite", "nombre de rapports", "transmission", "longueur", "largeur", "hauteur"
        #  "volume de coffre", "performance", "vitesse max", "consommation urbaine", "consommation extra urbaine",
        #  "consommation mixte", "airbags", "anti-patinage", "aide au stationnement", "assistance au freinage",
        #  "feux a LED", "jantes", "autoradio", "connectivite", "ecran", "vitres", "volant", "volant reglable",
        #  "climatisation", "fermeture centralisee", "retroviseur exterieur", "retroviseur interieur",
        #  "vitres electriques"])

        wr.writerows(exported)
    print(len(names))
    print(len(price))
    print(len(disponobilite))
    print(len(Carrosserie))
    print(len(garanties))
    print(len(nombredePlaces))
    print(len(nombreDePortes))
    print(len(motorisation))
    print(len(nombredeCylindres))
    print(len(energie))
    print(len(puissancefiscale))
    print(len(puissance))
    print(len(couple))
    print(len(cylindre))
    print(len(boite))
    print(len(nombreDeRapports))
    print(len(transmission))
    print(len(longueur))
    print(len(largeur))
    print(len(hauteur))
    print(len(volumeDeCoffre))
    print(len(performance))
    print(len(vitesseMax))


if __name__ == "__main__":
    main()
