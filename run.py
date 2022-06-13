# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import pyinputplus as pyip

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('birthday_book')
BIRTHDAY_WORKSHEET = SHEET.worksheet('birthdays')

def user_response(message, min_value, max_value):
    """
    Function validates users input from a list of choices.
    used throughout the programme
    """
    input = pyip.inputInt(prompt=message, min=min_value, max=max_value)
    return input

def main_menu_():
    """
    User selects which action to do, function uses their input and runs
    elif loop to trigger the next process.
    If user inputs invalid choice, programme will continue to ask for a valid input.
    """
    print(
        "\n 1. Search Birthdays\n 2. Add a new Birthday\n\
 3. Edit Exisiting Birthday\n 4. Retrieve all Birthdays\n")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 4
            )
        if user_input == 1:
            print("search birthday")
            break
        elif user_input == 2:
            add_new_birthday()
            break
        elif user_input == 3:
            print("edit_birthday_from_menu")
            break
        else:
            retrieve_all_birthdays()
            break
        return False

def another_task():
    """
    Function returns user to the main menu if they'd 
    like to perform another action
    """
    print("\nWould you like to perform another action?\n")
    print("1. Yes, back to main menu\n\
2. No, I'm done")
    while True:
        user_input = user_response(
            "\nPlease enter a number from the above options: ", 1, 2
            )
        if user_input == 1:
            print("\nReturning to the main menu...\n")
            main_menu_()
            break
        else:
            print(
                "Exiting programme...\n")
            raise SystemExit

def retrieve_records():
    """
    Function to retrieve all records found
    in the birthday book spreadhseet.
    """
    return BIRTHDAY_WORKSHEET.get_all_records()


def retrieve_all_birthdays():
    """
    Function to retrieve full list of Birthdays
    """
    all_birthdays = retrieve_records()
    print("\nNow retrieving all Birthdays...\n")
    for birthday in all_birthdays:
        print_records_in_loop(birthday)
    
    another_task()
    
def print_records(records, function=None):
    """
    Function to print a single contact.
    To be used in the contact search functions.
    """
    print("\nNow printing your contact(s)...\n")
    for record in records:
        print_records_in_loop(record)

def print_records_in_loop(record):
    """
    Function to loop through all records passed
    as a parameter and print the details in a
    list of key: values.
    """
    print("Printing record...")
    for key, value in record.items():
            print(f"{key}: {value}")
    print("\n")

def update_worksheet(row, col, value):
    """
    Function used when editing a contact
    to make changes to the worksheet.
    """
    worksheet_to_update = BIRTHDAY_WORKSHEET
    worksheet_to_update.update_cell(row, col, value)
    print('\nChange saved\n')

def save_to_worksheet(info):
    """
    Function used when saving a contact
    to make changes to the worksheet.
    """
    print(f'\nNow saving {info}....\n')
    worksheet_to_update = BIRTHDAY_WORKSHEET
    worksheet_to_update.append_row(info)
    print('Save complete')

    user_input = pyip.inputYesNo(
        '\nWould you like to edit this contact? (Y/N): '
        )
    if user_input == 'yes':
        print('\nYou will now be taken to edit this contact...\n')
        edit_exisiting_birthday(info)
    else:
        another_task()

def birthday_id_creation():
    """
    Function generates a new birthday entry ID,
    based upon the previous entry in the worksheet.
    Needed when adding new birthday entry.
    """
    all_values = BIRTHDAY_WORKSHEET.get_all_values()
    previous_row = all_values[-1]
    previous_birthday_id = int(previous_row[5])
    new_birthday_id = str(previous_birthday_id + 1)
    return new_birthday_id

def convert_to_list_action(option, action):
    """
    Function to convert birthday dictionary to a list
    so it can be indexed when editing
    or deleting the birthday information.
    """
    values = option.values()
    values_list = list(values)
    if action == 'edit':
        edit_exisiting_birthday(values_list)
    elif action == 'delete':
        print('delete')
    else:
        print('Invalid action has been defined.')

def select_from_multiple_records(birthdays):
    """
    Function to choose a single record from a list
    of records that have been returned
    """
    def print_records_as_options(records, function=None):
        """
        Function to print a single contact with an record number.
        To be used in the contact search functions when multiple
        records are returned.
        """
        for idx, record in enumerate(records):
            print(f"\nRecord: {idx}\n")
            print_records_in_loop(record)

    print('\nList of contacts to choose from: ')
    print_records_as_options(birthdays, print_records_in_loop)
    user_input = user_response(
        '\nEnter the record number of the contact you would like to action: ',
        0, len(birthdays))
    return birthdays[user_input]


def add_new_birthday():
    """
    Function allows user to add new birthday entry data
    """
    print('\nTo add a new Birthday please enter the details below.\n\
\nAll fields with a * are required.\n\
\nType NA for any fields you wish to leave blank.\n')
    first_name = pyip.inputStr('*First Name: ').capitalize()
    last_name = pyip.inputStr('*Last Name: ').capitalize()
    age_turning = pyip.inputStr('*Age Turning: ')
    next_birthday = pyip.inputStr('*Birthday: ').capitalize()
    category = pyip.inputStr('*Category: ').capitalize()
    user_input = user_response('*Choose category: 1. Friends, \
2. Favourites, 3. Family or 4. General: ', 1, 4)
    if user_input == 1:
        category = 'Friends'
    elif user_input == 2:
        category = 'Favourites'
    elif user_input == 3:
        category = 'Family'
    else:
        category = 'General'
    birthday_id = birthday_id_creation()
    new_birthday_entry = [
        first_name, last_name, age_turning,
        next_birthday, category, birthday_id
        ]
    print(new_birthday_entry)
    save_to_worksheet(new_birthday_entry)

def edit(birthday, cell_index, info_type):
    """
    Allows user to update cells by adding new entry
    """
    # Converts to a string first to allow any integers to be searched for.
    cell = BIRTHDAY_WORKSHEET.find(birthday[cell_index])
    new_value = pyip.inputStr(f'Enter new {info_type}:').capitalize()
    birthday[cell_index] = new_value
    print(f'{info_type} now being updated...\n')
    update_worksheet(cell.row, cell.col, new_value)


def edit_exisiting_birthday(birthday):
    """
    Allows user to edit exisisting birthday entry 
    by individual input fields
    """
    print(birthday)
    print('\nWhich feild would you like to edit?\n 1. First Name\n 2. Last Name\n 3. Age Turning\n 4. Next Birthday\n 5. Category\n 6. Exit')
    user_input = user_response("\n Please enter an option number: ", 1, 7)
    if user_input == 1:
        edit(birthday, 0, 'first name')
        print(birthday)
        pass
    elif user_input == 2:
        edit(birthday, 1, 'last name')
        print(birthday)
        pass
    elif user_input == 3:
        edit(birthday, 2, 'age turning')
        print(birthday)
        pass
    elif user_input == 4:
        edit(birthday, 3, 'next birthday')
        print(birthday)
        pass
    elif user_input == 5:
        cell = BIRTHDAY_WORKSHEET.find(birthday[4])
        user_input = user_response('*Choose category: 1. Friends, \
2. Favourites, 3. Family or 4. General: ', 1, 4)
        if user_input == 1:
            new_value = 'Friends'
        elif user_input == 2:
            new_value = 'Favourites'
        elif user_input == 3:
            new_value = 'Family'
        else:
            new_value = 'General'
        birthday[4] = new_value
        print('\nCategory now being updated...\n')
        update_worksheet(cell.row, cell.col, new_value)
        print(birthday)
        pass
    else:
        another_task()

def run_programme():
    """
    This function will call on all of the other functions
    to run the programme
    """
    print('\nWelcome to your Birthday Book!\n')
    print('\nInstructions:\n\
- From the menu, type a number and then press enter.\n\
- For a Y or N choice, please type Y or N and press enter.\n\
- To restart the programme, press the "Run Programme" at the top.')
    print('\nmain menu...\n')
    main_menu_()



run_programme()
  



