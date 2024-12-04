import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from time import sleep

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CarScraper:
    def __init__(self, base_url: str = "https://www.automobile.tn/fr/neuf/"):
        self.base_url = base_url
        self.session = requests.Session()
        # Add headers to mimic browser behavior
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page_content(self, url: str, retries: int = 3) -> Optional[str]:
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
                sleep(2 ** attempt)  # Exponential backoff
        return None

    def get_constructors(self) -> List[str]:
        """Extract constructor names and their URLs."""
        src = self.get_page_content(self.base_url)
        if not src:
            return []
        
        soup = BeautifulSoup(src, 'lxml')
        constructor_links = soup.select("div.container a")
        
        # Extract constructor names from URLs
        constructors = []
        for link in constructor_links:
            href = link.get('href', '')
            parts = href.split('/')
            if len(parts) >= 4:
                constructors.append(parts[3])
        
        return constructors

    def get_technical_file_links(self, constructor_url: str) -> List[str]:
        """Get technical file links for a specific constructor."""
        page_content = self.get_page_content(constructor_url)
        if not page_content:
            return []

        soup = BeautifulSoup(page_content, "lxml")
        technical_files = []
        
        # Get initial version links
        version_links = soup.select("div.articles div.versions-item a")
        
        for version in version_links:
            href = version.get('href', '')
            if href:
                # Construct full URL for technical file
                technical_file_url = self.base_url + '/'.join(href.split('/')[3:])
                technical_files.append(technical_file_url)
                
                # Check if we need to go one level deeper
                tech_page_content = self.get_page_content(technical_file_url)
                if tech_page_content:
                    tech_soup = BeautifulSoup(tech_page_content, "lxml")
                    
                    # If technical details section doesn't exist, we need to go deeper
                    if not tech_soup.select("div#specs.technical-details"):
                        deeper_versions = tech_soup.select("td.specs a")
                        for deeper_version in deeper_versions:
                            deeper_href = deeper_version.get('href', '')
                            if deeper_href:
                                full_url = self.base_url + '/'.join(deeper_href.split('/')[3:])
                                technical_files.append(full_url)
        
        return technical_files

    def extract_car_details(self, technical_file_url: str) -> Dict:
        """Extract detailed information about a specific car."""
        page_content = self.get_page_content(technical_file_url)
        if not page_content:
            return {}

        soup = BeautifulSoup(page_content, "lxml")
        
        try:
            return {
                'model': soup.select_one("h3.page-title").text.strip() if soup.select_one("h3.page-title") else "",
                'version': soup.select_one("h3.page-title span").text.strip() if soup.select_one("h3.page-title span") else "",
                'price': soup.select_one("div.version-details div span").text.strip() if soup.select_one("div.version-details div span") else "",
                'specs': self._extract_specifications(soup)
            }
        except Exception as e:
            logger.error(f"Error extracting car details from {technical_file_url}: {str(e)}")
            return {}

    def _extract_specifications(self, soup: BeautifulSoup) -> Dict:
        """Extract technical specifications from the soup object."""
        specs = soup.select("div#specs.technical-details td")
        if len(specs) < 30:  # Ensure we have enough specifications
            return {}
            
        return {
            'garantie': specs[7].text.strip() if len(specs) > 7 else "",
            'performance': specs[9].text.strip() if len(specs) > 9 else "",
            'vitesse_max': specs[21].text.strip() if len(specs) > 21 else "",
            'consommation_urbaine': specs[23].text.strip() if len(specs) > 23 else "",
            'consommation_extra_urbaine': specs[24].text.strip() if len(specs) > 24 else "",
            'volume_coffre': specs[26].text.strip() if len(specs) > 26 else "",
            'nombre_cylindres': specs[29].text.strip() if len(specs) > 29 else "",
            'puissance_fiscale': specs[9].text.strip() if len(specs) > 9 else ""
        }

def main():
    scraper = CarScraper()
    
    # Get all constructors
    constructors = scraper.get_constructors()
    logger.info(f"Found {len(constructors)} constructors")
    
    # For testing, let's process just one constructor
    if constructors:
        constructor_url = scraper.base_url + constructors[5]
        logger.info(f"Processing constructor: {constructors[5]}")
        
        # Get technical file links for this constructor
        technical_files = scraper.get_technical_file_links(constructor_url)
        logger.info(f"Found {len(technical_files)} technical files")
        
        # Process first technical file
        if technical_files:
            car_details = scraper.extract_car_details(technical_files[0])
            logger.info("Car details:")
            logger.info(car_details)

if __name__ == "__main__":
    main()