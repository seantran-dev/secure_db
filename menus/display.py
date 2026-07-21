
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
def main_menu(fail_status = False, cancelled_registration = False):
    clear_screen()
    draw_header()
    if fail_status is True:
        print("[DENIED] Invalid username or password.\n")
    if cancelled_registration is True:
        print("[USER] Registration cancelled.\n")
    print("  1. Log-in")
    print("  2. Register")
    print()
    print("  Q. Quit")
    print()
    page_main_menu = input("> ")
    print()
    
    if page_main_menu == "1": # Log-in
        login_menu()
        
    elif page_main_menu == "2": # Register
        register_menu()
    elif page_main_menu.lower() == "q":
        exit_program()
    else:
            draw_header()
            print("[ERROR] Please select a valid option.\n")

# Main Menu > Log-in
def login_menu():
    breadcrumb.append("Log-in")
    draw_header()
    
    username = input("Username: ")
    password = getpass("Password: ")

    user, key = login(username, password)
    if (user, key) == (None, None):
        back(1)
        main_menu(True)
    else: 
        login_options(user, key, True, None, None)

def register_menu(register_fail = False):
    breadcrumb.append("Register")
    draw_header()
    if register_fail == True:
        print("[DENIED] Username already taken.")
    
    
    username = input("Username: ")
    if get_user(username) is not None:
        back(1)
        register_menu(True)
    else:
        email = input("Email: ")
        password = getpass("Password: ")
        print()
        register_option = input("Register? (Y/N)")
        if register_option.lower() == "y":
            register(username, email, password)
        elif register_option.lower() == "n":
            back(1)
            main_menu(False, True)
        else:
            draw_header()
            print("[ERROR] Please enter a valid option.\n")
# Main Menu > Log-in > Credentials
def login_options(u, k, login_success, no_credentials_stored, add_success):
    breadcrumb.append("Credentials")
    draw_header()

    if login_success == True:
        print("[ACCEPTED] Login successful!\n")
    if no_credentials_stored == True:
        print("[ERROR] No credentials found.\n")
    if add_success == True:
        print("[ACCEPTED] Successfully added new credential.\n")
    elif add_success == False:
        print("[USER] Cancelled operation.\n")
    else:
            draw_header()
            print("[ERROR] Please select a valid option.\n")

    user, key = (u, k)
    while True:

        print("  1. View Credentials")
        print("  2. Add Credential")
        print()
        print("  B. Back (Logout)")
        print("  Q. Quit")
        print()
        page_login_options = input("> ")
        print()
        if page_login_options == "1":
            get_credentials_menu(user, key, None)
            break
        elif page_login_options == "2":
            breadcrumb.append("Add")
            draw_header()
            add_credentials_menu(user, key)
            break
        elif page_login_options.lower() == "b":
            back(2)
            main_menu()
            break
        elif page_login_options.lower() == "q":
            exit_program()
            break
        else:
            draw_header()
            print("[ERROR] Please select a valid option.\n")


# Main Menu > Log-in > Credentials > View
def get_credentials_menu(user, key, deletion_success = False):
    breadcrumb.append("View")
    draw_header()
    if deletion_success is True:
        print("[ACCEPTED] Successfully deleted credential.\n")
    credentials_list = get_credentials(user)
    if credentials_list == None:
        back(2)
        login_options(user, key, False, True, None)
    else:
        credentials_options(user, key, credentials_list)

def credentials_options(user, key, list):

    print()
    print("  B. Back")
    print("  Q. Quit Program")
    print()
    option_status = input("> ")
    
    if option_status.lower() == "b":
        back(2)
        login_options(user, key, None, None, None)
    elif option_status.lower() == "q":
        exit_program()
    elif option_status.isdigit():
        if int(option_status) > 0 and int(option_status) <= len(list):
            credential_options(user, key, list[int(option_status) - 1], False, False)
    else:
            draw_header()
            print("[ERROR] Please select a valid option.\n")

# Main Menu > Log-in > Credentials > View > Service
def credential_options(user, key, credentials, cancelled = False, copied_password = False):
    clear_screen()
    breadcrumb.append("Service")
    draw_header()
    password_star = "********"
    if cancelled == True:
        print(f"['{credentials[2]}'] Operation cancelled, no changes made.\n")
    elif cancelled == False:
        print(f"['{credentials[2]}'] Please select an option.\n")
    elif cancelled == None and copied_password == None:
        print(f"['{credentials[2]}'] Changes updated successfully.\n")
    elif copied_password == True:
        print(f"'[{credentials[2]}'] Password copied to clipboard.\n")
        password_star = '******** [COPIED]'

    print(f"Username:     {credentials[3]}")
    print(f"Password:     {password_star}")
    print()
    print("  1. Reveal Password ")
    print("  2. Copy Password ")
    print("  3. Edit Information ")
    print("  4. Delete Information ")
    print()
    print("  B. Back")
    print("  Q. Quit")
    print()
    edit_option = input("> ")
    # Reveal password
    if edit_option.lower() == "1": 
        show_credentials_info(user, key, credentials)
    # Copy password
    elif edit_option.lower() == '2':
        back(1)
        password = decrypt_secret(key, credentials)
        pyperclip.copy(password)
        credential_options(user, key, credentials, None, True)
    # Edit Information
    elif edit_option.lower() == '3':
        edit_credentials_menu(user, key, credentials)
    # Delete Information
    elif edit_option.lower() == "4":
        breadcrumb.append("Delete")
        clear_screen()
        draw_header()
        print(f"[{credentials[2]}]", end = " ")
        print("Permanently delete log-in information? (Y/N)\n")
        confirm_delete = input("> ")
        if confirm_delete.lower() == "y":
            delete_credential(user, credentials)
            back(3)
            get_credentials_menu(user, key, True)
        elif confirm_delete.lower() == "n":
            back(2)
            credential_options(user, key, credentials, cancelled = True)
            print()
        else:
            draw_header()
            print("[ERROR] Please enter a valid option.\n")
    elif edit_option.lower() == "b":
        back(2)
        get_credentials_menu(user, key, False)
    elif edit_option.lower() == "q":
        exit_program()
    else:
        draw_header()
        print("[ERROR] Please select a valid option.\n")

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
    draw_header()
    if user[0] == credential[1]:
        print(f"[{service}] Password revealed. \n")
        print(f"Username:     {username}")
        print(f"Password:     {password}")
    else:
        print("[ERROR] Denied.")
    
    exit = input("\nPress enter to close.")
    back(3)
    get_credentials_menu(user, key, False)

def edit_credentials_menu(user, key, credential):
    breadcrumb.append("Edit Information")
    draw_header()
    print("Type to enter a new value, or press enter to keep.\n")
    print(f" Current service : {credential[2]}")
    new_service = input("    [New service]: ")
    print()
    print(f" Current username : {credential[3]}")
    new_username = input("    [New username]: ")
    print()

    new_password = getpass("    [New password]: ")
    retype_password = getpass(" [Retype password]: ")
    if new_password == retype_password:
        print()
        print("Proceed with the changes? (Y/N)\n")
        confirm_edit = input("> ")
        if confirm_edit.lower() == 'y':
            print("Changes made.")
            back(1)
            credential_options(user, key, credential, None, None)
        elif confirm_edit.lower() == 'n':
            back(1)
            credential_options(user, key, credential, True, False)




# Header showing breadcrumb for menu navitation
def draw_header():
    clear_screen()
    print("[Password Vault]")
    print(" > ".join(breadcrumb))
    print("-" * 40)

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Removes a breadcrumb from the menu navitation
def back(n):
    for i in range(n):
        breadcrumb.pop()

def exit_program():
    clear_screen()
    print("[Password Vault] \nSuccessfully logged out. User exited program.\n")
    SystemExit(0)

if __name__ ==  "__main__":
    print()