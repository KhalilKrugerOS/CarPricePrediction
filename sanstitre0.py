import json

def add_brand_to_technical_data(input_file, output_file):
    try:
        # Load the original car data from the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            all_car_data = json.load(f)
        
        # Modify the data by adding the brand name to each car's technical data
        for brand_name, models in all_car_data.items():
            for model_link, tech_data in models.items():
                # Add the brand name to the technical data
                tech_data['brand'] = brand_name
        
        # Save the modified data to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_car_data, f, ensure_ascii=False, indent=2)
        
        print(f"Brand names added and saved to {output_file}")
    
    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    # Define the input and output file paths
    input_file = 'TPML_updated.json'  # Adjust path if needed
    output_file = 'car_scraper_results/brand1.json'  # Output file with brand names added1
    
    # Add brand to each car's technical data
    add_brand_to_technical_data(input_file, output_file)
