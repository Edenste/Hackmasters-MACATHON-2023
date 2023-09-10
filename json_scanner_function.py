import os
import json
from datetime import datetime

def read_json_files_in_range(start_date, end_date, category_list):
    # Specify the directory path to search for JSON files
    directory_path = r"./json_files"

    # Initialize a list to store the JSON data from each file
    json_data_list = []
    json_filename_list = []

    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        json_filename_list.append(filename)
        # Check if the file is a JSON file (ends with .json)
        if filename.endswith(".json"):
            date_str = filename.split(".")[
                0
            ]  # Extract the date portion from the file name
            file_date = datetime.strptime(
                date_str, "%Y-%m-%d"
            )  # Parse the date string into a datetime object

            # Check if the file's date is within the specified range
            file_path = os.path.join(directory_path, filename)
            try:
                # Open and read the JSON file
                with open(file_path, "r") as json_file:
                    data = json.load(json_file)
                    json_data_list.append(data)
            except Exception as e:
                print(f"Error reading {filename}: {str(e)}")

    # Changes the "YYYY-MM-DD.json" into "DD/MM/YYYY" format
    for index in range(len(json_filename_list)):
        date = json_filename_list[index]

        year = date[0:4]
        month = date[5:7]
        day = date[8:10]

        new_date = day + "/" + month + "/" + year

        json_filename_list[index] = new_date

    deals_dictionary = {}
    date_index = 0

    # Iterates through the json data in the json
    for deals_data in json_data_list:
        # Iterates through the categories in the deals data
        for key in deals_data:
            # Checks if the category is in the category list and verifies if the category is in the format of a list
            if key in category_list and isinstance(deals_data[key], list):
                temp_list = []

                # Converts the JSON file into a python dictionary
                # The title will only include the specified keywords and nouns from the value (text) of the title
                for product in range(len(deals_data[key])):
                    temp_dict = {}

                    if isinstance(deals_data[key][product], dict):
                        for attribute, value in deals_data[key][product].items():
                            temp_dict[attribute] = value

                    temp_dict["date"] = json_filename_list[date_index]

                temp_list.append(temp_dict)

            deals_dictionary[key] = temp_list
        date_index += 1

    print(deals_dictionary)
    return deals_dictionary

if __name__ == "__main__":
    start_date = datetime.strptime("2020-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2020-01-31", "%Y-%m-%d")
    default_category_list = [
        "Alcohol",
        "Automotive",
        "Books & Magazines",
        "Computing",
        "Dining & Takeaway",
        "Education",
        "Electrical & Electronics",
        "Entertainment",
        "Fashion & Apparel",
        "Financial",
        "Gaming",
        "Groceries",
        "Health & Beauty",
        "Home & Garden",
        "Internet",
        "Mobile",
        "Pets",
        "Sports & Outdoors",
        "Toys & Kids",
        "Travel",
        "Other",
    ]
    read_json_files_in_range(start_date, end_date, default_category_list)