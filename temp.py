import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
import traceback

def get_all_brands(base_url, main_page_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(main_page_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the brands list
        brands_container = soup.find("div", class_="brands-list-widget")
        
        if not brands_container:
            print("No brands container found.")
            return []
        
        # Find all brand links
        brand_links = brands_container.find_all("a")
        
        # Extract brand information
        brands = []
        for link in brand_links:
            href = link.get("href", "")
            if href and href.startswith("/fr/neuf/"):
                # Extract brand name from the href
                brand_name = href.split("/")[-1]
                brands.append({
                    "name": brand_name,
                    "link": href
                })
        
        return brands
    
    except Exception as e:
        print(f"Error fetching brands: {e}")
        traceback.print_exc()
        return []

def scrape_technical_details(model_link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(model_link, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Check for primary technical details section
        tech_sections = [
            soup.find("div", class_="technical-details"),
            soup.find("section", class_="technical-details"),
            soup.find("div", id="technical-details"),
            soup.find("table", class_="technical-table"),
            soup.find("div", class_="car-specs")
        ]
        tech_section = next((section for section in tech_sections if section), None)
        
        # Verify we are on the technical details page
        if not tech_section:
            # Check for alternate structure with model links
            content_wrapper = soup.find("div", class_="content-wrapper")
            if content_wrapper:
                super_content = content_wrapper.find("div", id="super_content_container")
                if super_content:
                    content_container = super_content.find("div", id="content_container", class_="content-container container-lg")
                    if content_container:
                        detail_content = content_container.find("div", id="detail_content")
                        if detail_content:
                            versions_details = detail_content.find("div", class_="versions-details")
                            if versions_details:
                                versions_table = versions_details.find("table", class_="versions")
                                if versions_table:
                                    # Collect all model links
                                    model_links = []
                                    for row in versions_table.find_all("tr"):
                                        first_td = row.find("td")
                                        if first_td and first_td.a:
                                            model_links.append(first_td.a["href"])
                                    
                                    # Consolidate details from all model links
                                    all_tech_details = {}
                                    for link in model_links:
                                        full_link = requests.compat.urljoin(model_link, link)
                                        details = scrape_technical_details(full_link)
                                        all_tech_details[full_link] = details
                                    
                                    return all_tech_details
            
            # If neither structure is found, log and return empty
            print(f"No technical details found for {model_link}")
            return {}
        
        # Extract price if we're on the technical details page
        price_span = soup.select_one(
            '.content-wrapper #super_content_container .content-container #detail_content .version-details .buttons span'
        )
        price = price_span.text.strip() if price_span else "Price not available"
        
        # Extract technical data from the primary section
        tech_data = {}
        
        # Method 1: Technical rows
        technical_rows = tech_section.find_all(["div", "tr"], class_=["technical-row", "spec-row"])
        for row in technical_rows:
            label_element = row.find(["span", "th", "div"], class_=["label", "spec-label"])
            value_element = row.find(["span", "td", "div"], class_=["value", "spec-value"])
            
            if label_element and value_element:
                label = label_element.get_text(strip=True)
                value = value_element.get_text(strip=True)
                if label and value:
                    tech_data[label] = value
        
        # Method 2: Definition lists
        if not tech_data:
            def_lists = tech_section.find_all("dl")
            for dl in def_lists:
                terms = dl.find_all("dt")
                descriptions = dl.find_all("dd")
                for term, desc in zip(terms, descriptions):
                    label = term.get_text(strip=True)
                    value = desc.get_text(strip=True)
                    tech_data[label] = value
        
        # Method 3: Table rows
        if not tech_data:
            table_rows = tech_section.find_all("tr")
            for row in table_rows:
                cols = row.find_all(["th", "td"])
                if len(cols) >= 2:
                    label = cols[0].get_text(strip=True)
                    value = cols[1].get_text(strip=True)
                    tech_data[label] = value
        
        # Add price separately, without overriding other details
        tech_data["Price"] = price
        
        return tech_data
    
    except Exception as e:
        print(f"Error scraping technical details for {model_link}: {e}")
        traceback.print_exc()
        return {}

def scrape_brand_models(base_url, brand_link):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        full_url = base_url + brand_link
        
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the articles div containing all car models
        articles_div = soup.find("div", class_="articles")
        
        if not articles_div:
            print(f"No articles div found for {brand_link}")
            return []
        
        # Find all model spans
        model_spans = articles_div.find_all("span", attrs={"data-key": True})
        
        # Extract model links
        brand_models = []
        for span in model_spans:
            # Find the anchor tag
            a_tag = span.find("a")
            if not a_tag:
                continue
            
            # Extract model link
            model_link = a_tag.get("href", "")
            if model_link:
                # Add the full URL to the model link
                full_model_link = base_url + model_link
                brand_models.append(full_model_link)
        
        return brand_models
    
    except Exception as e:
        print(f"Error scraping models for {brand_link}: {e}")
        traceback.print_exc()
        return []

def main():
    # Base and main page URLs
    base_url = "https://www.automobile.tn"
    main_page_url = f"{base_url}/fr/neuf"
    
    # Create output directory
    output_dir = "car_scraper_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all brands
    all_brands = get_all_brands(base_url, main_page_url)
    print(f"Found {len(all_brands)} brands")
    
    # Dictionary to store all car data
    all_car_data = {}
    
    # Scrape models for each brand
    for brand in all_brands:
        # Random delay to be respectful to the website
        time.sleep(random.uniform(1, 3))
        
        print(f"Scraping models for brand: {brand['name']}")
        
        # Scrape models for this brand
        brand_models = scrape_brand_models(base_url, brand['link'])
        
        # Scrape technical details for each model
        model_technical_data = {}
        for model_link in brand_models:
            # Random delay to be respectful to the website
            time.sleep(random.uniform(1, 3))
            print(f"Scraping technical details for model: {model_link}")
            tech_data = scrape_technical_details(model_link)
            if tech_data:
                model_technical_data[model_link] = tech_data
        
        # Store models with their technical data
        if model_technical_data:
            all_car_data[brand['name']] = model_technical_data
            print(f"{brand['name']}: {len(model_technical_data)} models scraped with technical data")
        
        # Optional: Save intermediate results
        intermediate_file = os.path.join(output_dir, f"{brand['name']}_models_technical_data.json")
        with open(intermediate_file, 'w', encoding='utf-8') as f:
            json.dump(model_technical_data, f, ensure_ascii=False, indent=2)
    
    # Save complete results
    full_output_file = os.path.join(output_dir, "TPML.json")
    with open(full_output_file, 'w', encoding='utf-8') as f:
        json.dump(all_car_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal brands scraped: {len(all_car_data)}")
    print(f"Full results saved to {full_output_file}")
    
    
    # Print summary of scraped brands and their model counts
    print("\nScraping Summary:")
    for brand, models in all_car_data.items():
        print(f"{brand}: {len(models)} models")

if __name__ == "__main__":
    main()
