import argparse
import urllib.request
import logging
import datetime


# Part 1: Download data by using --url parameter

def downloadData(url):  

    """
    Reads data from a URL and returns the data as a string

    :param url:
    :return: the content of the URL
    """
    # read the URL
    with urllib.request.urlopen(url) as response: 
        response = response.read().decode('utf-8') 

    # return the data
    return response

# Part 2: Write errors to a file named error.log
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Part 3: Process the data and handle any errors with invalid dates

def processData(file_content):
    """
    Takes the contents of the file as the first parameter, processes the file line by line, 
    and returns a dictionary that maps a person’s ID to a tuple of the form (name, birthday).
    """
    result_dict = {}
    header = True
    line_num = 0 
    for line in file_content.split("\n"):
        if header: 
            header = False 
            continue 

        line_num += 1
        try:
            id_str, name, birthday_str = line.split(",")
            id = int(id_str)
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y").date()
            result_dict[id] = (name, birthday)
        except ValueError as e:
            logging.error(f"Error processing line {line_num} for ID {id_str}: {e}")

    return result_dict 


# Part 4: Printing user info based on ID

def displayPerson(id, personData):
    """
    The purpose of this function is to print the name and birthday 
    of a given user identified by the input id. 
    """
    if id in personData:
        name, birthday = personData[id]
        print(f"User ID: {id}\nName: {name}\nBirthday: {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")

# Part 5: Main program logic
def main(url):
    print(f"Running main with URL = {url}...")

    try:
        file_data = downloadData(url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        return

    person_dict = processData(file_data)

    while True:
        try:
            user_input = int(input("Enter a User ID to lookup or <= 0 to exit: "))
            if user_input <= 0:
                print("Exiting the program...")
                break
            displayPerson(user_input, person_dict)
        except ValueError:
            print("Invalid input. Please enter a valid User ID.")


        # Main entry point
if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)