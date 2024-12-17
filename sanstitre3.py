import json
import re

# Function to check if a string is a valid URL that starts with the base URL
def is_valid_url(string):
    base_url = "https://www.automobile.tn/fr/neuf"
    url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
    return string.startswith(base_url) and bool(url_pattern.match(string))

# Function to recursively replace keys with their values if conditions are met
def replace_keys_with_values(data):
    if not isinstance(data, dict):
        return data  # Return non-dict values as is

    updated_data = {}
    for key, value in data.items():
        # Check if the key is a valid URL
        if is_valid_url(key):
            # Replace the key with its corresponding value
            if isinstance(value, dict):
                # Check if the value contains at least one valid URL as a key
                if any(is_valid_url(inner_key) for inner_key in value):
                    updated_data.update(value)  # Replace the URL key with its value's keys
                else:
                    updated_data[key] = value  # Keep the key if no valid inner URL found
            else:
                updated_data[key] = value
        # If the value is a dictionary, process it recursively
        elif isinstance(value, dict):
            updated_data[key] = replace_keys_with_values(value)
        else:
            updated_data[key] = value

    return updated_data

# Main function to load, process, and save the JSON data
def main():
    input_file = 'car_scraper_results\TPML.json'
    output_file = 'TPML_updated.json'

    # Load the JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Process the JSON data to replace keys
    updated_data = replace_keys_with_values(data)

    # Save the updated JSON data to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=2)

    print(f"Updated JSON data saved to {output_file}")

if __name__ == "__main__":
    main()
