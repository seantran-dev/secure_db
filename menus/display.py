
import hashlib
import os
import pyperclip

from getpass import getpass
from authentication.login import login
from authentication.register import register
from database.credentials import *
from database.users import create_user, get_user
from encryption.decrypt import decrypt_secret
breadcrumb = []
breadcrumb.append("Main Menu")

# Main Menu
def main_menu(fail_status = None, cancelled_registration = None, short = None):
    clear_screen()
    draw_header(None)
    if fail_status is True and cancelled_registration is None:
        print("//ERROR - Invalid username or password.\n")
    elif cancelled_registration is True:
        print("//USER - Registration cancelled.\n")
    elif cancelled_registration is False and short is False:
        print("//ACCEPTED - Registration successful, please log-in.\n")
    elif short is True:
        print("//ERROR - All input must be 4 characters minimum.\n")
    
    while True:
        print("  1. Log-in")
        print("  2. Register")
        print()
        print("  Q. Quit Program")
        print()
        page_main_menu = input("> ")
        print()
        if page_main_menu == "1": # Log-in
            login_menu()
            break
        elif page_main_menu == "2": # Register
            register_menu()
            break
        elif page_main_menu.lower() == "q" or page_main_menu.lower() == "":
            exit_program()
            break
        else:
            draw_header(None)
            print("//ERROR - Please select a valid option.\n")
            continue

# Main Menu > Log-in
def login_menu():
    breadcrumb.append("Log-in")
    draw_header(None)
    
    username = input(" Username: ")
    password = getpass(" Password: ")

    user, key = login(username, password)
    if (user, key) == (None, None):
        back(1)
        main_menu(True, None, False)
    else: 
        login_options(user, key, True, None, None)

def register_menu(user_taken = False):
    breadcrumb.append("Register")
    draw_header(None)
    min_length = 4
    if user_taken == True:
        print("//DENIED - Username already taken.\n")
    else:
        print("[Register] Please enter user information. (At least 4 characters long)\n")
    username = input(" Username:  ")
    if get_user(username) is not None:
        back(1)
        register_menu(True)
    else:
        email = input(" Email:     ")

        password = getpass(" Password:  ")

        if username == "" or email == "" or password == "":
            back(1)
            main_menu(True, None, False)
        elif len(username) < 4 or len(email) < 4 or len(password) < 4:
            back(1)
            main_menu(False, False, True)
        else:
            print()
            while True: 
                print("Register? (Y/N)\n")
                register_option = input("> ")
                if register_option.lower() == "y":
                    register(username, email, password)
                    back(1)
                    main_menu(None, False, False)
                    break
                elif register_option.lower() == "n":
                    back(1)
                    main_menu(False, True, False)
                    break
                else:
                    draw_header(None)
                    print("//ERROR - Please enter a valid option.\n")
                    print(f" Username:  {username}")
                    print(f" Email:     {email}")
                    print(f" Password:  ********")
                    print()
                    continue
# Main Menu > Log-in > Credentials
def login_options(u, k, login_success, no_credentials_stored, add_success):
    breadcrumb.append("Credentials")
    user, key = (u, k)
    draw_header(user)

    if login_success == True:
        print("//ACCEPTED - Login successful!\n")
    elif no_credentials_stored == True:
        print("//ERROR - No credentials found.\n")
    elif add_success == True:
        print("//ACCEPTED - Successfully added new credential.\n")
    elif add_success == False:
        print("//USER - Cancelled operation.\n")
    elif login_success == None and no_credentials_stored == False and add_success == None:
        print("", end="")
    else:
        draw_header(user)
        print("//ERROR - Please select a valid option.\n")

    
    while True:

        print("  1. View Credentials")
        print("  2. Add Credential")
        print()
        print("  R. Return (Logout)")
        print("  Q. Quit Program")
        print()
        page_login_options = input("> ")
        print()
        if page_login_options == "1":
            get_credentials_menu(user, key, None)
            break
        elif page_login_options == "2":
            breadcrumb.append("Add")
            draw_header(user)
            add_credentials_menu(user, key)
            break
        elif page_login_options.lower() == "r" or page_login_options.lower() == "":
            back(2)
            main_menu(None, None, False)
            break
        elif page_login_options.lower() == "q":
            exit_program()
            break
        else:
            draw_header(user)
            print("//ERROR - Please select a valid option.\n")


# Main Menu > Log-in > Credentials > View
def get_credentials_menu(user, key, deletion_success = False):
    breadcrumb.append("View")
    draw_header(user)
    if deletion_success is True:
        print("//ACCEPTED - Successfully deleted credential.\n")
    credentials_list = get_credentials(user)
    if credentials_list == None:
        back(2)
        login_options(user, key, False, True, None)
    else:
        credentials_options(user, key, credentials_list)

def credentials_options(user, key, list):

    print()
    print("  R. Return")
    print("  Q. Quit Program")
    print()
    option_status = input("> ")
    
    if option_status.lower() == "r" or option_status.lower() == "":
        back(2)
        login_options(user, key, None, False, None)
    elif option_status.lower() == "q":
        exit_program()
    elif option_status.isdigit():
        if int(option_status) > 0 and int(option_status) <= len(list):
            credential_options(user, key, list[int(option_status) - 1], False, False)
    else:
        draw_header(user)
        print("//ERROR - Please select a valid option.\n")

# Main Menu > Log-in > Credentials > View > Service
def credential_options(user, key, credentials, cancelled = False, copied_password = False):
    clear_screen()
    breadcrumb.append("Service")
    draw_header(user)
    password_star = "********"
    
    if cancelled == True:
        print(f" //USER - Operation cancelled, no changes made.\n")
    elif cancelled == None and copied_password == None:
        print(f" //ACCEPTED - Changes updated successfully.\n")
    elif copied_password == True:
        print(f" //USER - Password copied to clipboard.\n")
        password_star = '******** [COPIED]'
    while True:
        print(f" Service:      {credentials[2]}")
        print(f" Username:     {credentials[3]}")
        print(f" Password:     {password_star}")
        print()
        print("  1. Reveal Password ")
        print("  2. Copy Password ")
        print("  3. Edit Information ")
        print("  4. Delete Information ")
        print()
        print("  R. Return")
        print("  Q. Quit Program")
        print()
        edit_option = input("> ")
        # Reveal password
        if edit_option.lower() == "1": 
            show_credentials_info(user, key, credentials)
            break
        # Copy password
        elif edit_option.lower() == '2':
            back(1)
            password = decrypt_secret(key, credentials)
            pyperclip.copy(password)
            credential_options(user, key, credentials, None, True)
            break
        # Edit Information
        elif edit_option.lower() == '3':
            edit_credentials_menu(user, key, credentials)
            break
        # Delete Information
        elif edit_option.lower() == "4":
            delete_credentials_menu(user, key, credentials)
            break
        elif edit_option.lower() == "r" or edit_option.lower() == "":
            back(2)
            get_credentials_menu(user, key, False)
            break
        elif edit_option.lower() == "q":
            exit_program()
            break
        else:
            draw_header(user)
            print("//ERROR - Please select a valid option.\n")
            continue

# Main Menu > Log-in > Credentials > Add
def add_credentials_menu(user, key):
    service = input("Service: ")
    login_username = input("Username: ")
    password = getpass("Password: ")
    print("\nSave? (Y/N)")
    confirm_credential = input("> ")
    if confirm_credential.lower() == "y":
        add_credentials(user, service, login_username, password, key)
        back(2)
        login_options(user, key, login_success = False, no_credentials_stored = False, add_success = True)
        
    elif confirm_credential.lower() == "n":
        back(2)
        login_options(user, key, login_success = False, no_credentials_stored = False, add_success = False)

# Main Menu > Log-in > Credentials > View > Service > Reveal Password
def show_credentials_info(user, key, credential):
    breadcrumb.append("Reveal Password")
    service = credential[2]
    username = credential[3]
    password = decrypt_secret(key, credential)

    clear_screen()
    draw_header(user)
    if user[0] == credential[1]:
        print(f"[{service}] Password revealed. \n")
        print(f"Username:     {username}")
        print(f"Password:     {password}")
    else:
        print("//ERROR - Denied.")
    
    exit = input("\nPress [ENTER] to close.")
    back(3)
    get_credentials_menu(user, key, False)

# Main Menu > Log-in > Credentials > View > Service > Edit Information
def edit_credentials_menu(user, key, credential):
    breadcrumb.append("Edit")
    draw_header(user)
    password_fail = False
    while True:
        clear_screen()
        draw_header(user)
        if password_fail == True:
            print("//DENIED - Passwords do not match. Please try again.\n")
        else:
            print("Input changes to credential information, or press [ENTER] to keep.\n")
        print(f" Current service : {credential[2]}")
        new_service = input("    [New service]: ")
        if new_service == "":
            print("                   (no change)")
        print()
        print(f" Current username : {credential[3]}")
        new_username = input("    [New username]: ")
        if new_username == "":
            print("                   (no change)")
        print()

        print(f" Current password : ********")
        new_password = getpass("    [New password]: ")
        if new_password != "":
            retype_password = getpass(" [Retype password]: ")
        else: 
            retype_password = ""
            print("                   (no change)")
        if new_password == retype_password:
            if new_service == "" and new_username == "" and new_password == "":
                back(2)
                input("\n//USER - No changes made. Press [ENTER] to continue.")
                credential_options(user, key, credential, True, None)
                break
            print()
            print("Proceed with the changes? (Y/N)\n")
            confirm_edit = input("> ")
            if confirm_edit.lower() == 'y':
                updated_credential = edit_credentials(user, key, credential, new_service, new_username, new_password)
                back(2)
                credential_options(user, key, updated_credential, None, None)
                break
            elif confirm_edit.lower() == 'n':
                back(1)
                credential_options(user, key, credential, True, False)
                break
        else:
            password_fail = True
            continue

def delete_credentials_menu(user, key, credentials):
    breadcrumb.append("Delete")
    clear_screen()
    draw_header(user)

    while True: 
        print(f"'{credentials[2]}': ", end = " ")
        print("Permanently delete log-in information? (Y/N)\n")
        confirm_delete = input("> ")
        if confirm_delete.lower() == "y":
            delete_credential(user, credentials)
            back(3)
            get_credentials_menu(user, key, True)
            break
        elif confirm_delete.lower() == "n":
            back(2)
            credential_options(user, key, credentials, cancelled = True)
            print()
            break
        else:
            draw_header(user)
            print("//ERROR - Please enter a valid option.\n")
            continue

# Header showing breadcrumb for menu navigation
def draw_header(user):
    clear_screen()
    
    line_length = 41
    if user is None:
        print("[Password Vault]")
    else:
        name = user[1]
        print(f"[Password Vault]", end ="")
        print(" " * (line_length - 22 - len(name)), end = "")
        print(f"User: {name}")
    print(">", end = "")
    print("-" * line_length, end = "\n")
    print(" ", end = "")
    print(" > ".join(breadcrumb))
    print(">", end = "")
    print("-" * line_length, end = "\n")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Removes a breadcrumb from the menu navitation
def back(n):
    for i in range(n):
        breadcrumb.pop()

def exit_program():
    clear_screen()
    print("[Password Vault]")
    print("-" * 20)
    print("//USER - Application closed successfully.\n")
    input("Press [ENTER] to clear display.")
    clear_screen()
    SystemExit(0)

if __name__ ==  "__main__":
    print()