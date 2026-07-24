
import os
import pyperclip
from getpass import getpass


from authentication.login import login
from authentication.register import register

from database.credentials import *
from database.users import create_user, get_user
from database.settings import *
from encryption.decrypt import decrypt_secret
from menus.system import *

# 'User': The user parameter is the list containing the database information from the user table
# 'Key' : The key parameter is the AES encryption key derived from the user's password

# Main Menu Navigation
breadcrumb = []
global settings_tab
settings_tab = "security"

# Header showing breadcrumb for menu navigation
def draw_header(user):
    clear_screen()
    
    line_length = 45
    if user is None:
        print(" SecureDB ")
    else:
        name = user[1]
        print(f" SecureDB ", end ="")
        print(" " * (line_length - 17 - len(name)), end = "")
        print(f"User: {name}")
    print("-" * line_length, end = "\n")
    print(" ", end = "")
    last = f"[{breadcrumb.pop()}]"
    breadcrumb.append(last)
    print(" > ".join(breadcrumb))
    last = breadcrumb.pop()[1:-1]
    breadcrumb.append(last)
    print("-" * line_length, end = "\n")

def draw_settings_header(current_tab, user = None):
    line_length = 45
    
    print(f" SecureDB > Settings", end ="")
    
    if user == None:
        print("")
    else:
        name = user[1]
        print(" " * (line_length - 26 - len(name)), end = "")
        print(f"User: {name}")
    print("-" * line_length, end = "\n")
    if current_tab == "security":  
        print(" [Security]    Credentials     User Account")
    elif current_tab == "credentials":  
        print("  Security    [Credentials]    User Account")
    elif current_tab == "accounts":
        print("  Security     Credentials    [User Account]")
    print("-" * line_length, end = "\n")

# Clears screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Removes a breadcrumb from the menu navitation
def back(n):
    for i in range(n):
        breadcrumb.pop()

# Exit program
def exit_program(fast_exit = False):
    if fast_exit == True:
        clear_screen()
        raise SystemExit(0)
    elif fast_exit == False:
        clear_screen()
        print(" SecureDB")
        print("-" * 45)
        print(" Application closed successfully.\n")
        print(" Today was a good day.")
        input("\n Press [ENTER] to continue.")
        clear_screen()
        raise SystemExit(0)


def main_menu(fail_status = None, cancelled_registration = None, short = None):
    breadcrumb.append("Password Vault")
    clear_screen()
    draw_header(None)
    if fail_status is True and cancelled_registration is None:
        print("//ERROR - Invalid username or password.\n")
    elif cancelled_registration is True:
        print("//USER - Registration cancelled.\n")
    elif cancelled_registration is False and short is False:
        print("Registration successful, please log-in.\n")
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
            back(1)
            login_menu()
            break
        elif page_main_menu == "2": # Register
            back(1)
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
    print(" Please enter log-in information.\n")
    username = input(" Username: ")
    password = getpass(" Password: ")

    user, key = login(username, password)
    if (user, key) == (None, None):
        back(1)
        main_menu(True, None, False)
    else: 
        login_options(user, key, True, None, None)

# Main Menu > Register
def register_menu(user_taken = False):
    breadcrumb.append("Register")
    draw_header(None)
    min_length = 4

    if user_taken == True:
        print("//DENIED - Username already taken.\n")
    else:
        print(" Please enter user information. (At least 4 characters long)\n")
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
        elif len(username) < min_length or len(email) < min_length or len(password) < min_length:
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
    breadcrumb.append("Menu")
    user, key = (u, k)
    draw_header(user)

    if login_success == True:
        print(f" Login successful! Welcome, {user[1]}.\n")
    elif no_credentials_stored == True:
        print("//ERROR - No credentials found.\n")
    elif add_success == True:
        print("//ACCEPTED - Successfully added new credential.\n")
    elif add_success == False:
        print("//USER - Cancelled operation.\n")
    elif login_success == None and no_credentials_stored == False and add_success == None:
        print(f" Welcome, {user[1]}.\n")
    else:
        draw_header(user)
        print("//ERROR - Please select a valid option.\n")

    while True:

        print("  1. Display Credentials")
        print("  2. Add New Credential")
        print()
        print("  S. Settings")
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
        elif page_login_options.lower() == "s":
            settings_menu(user, key)
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

def settings_menu(user, key):
    if settings_tab == "security":
        security_settings_menu(user, key)
    elif settings_tab == "credentials":
        credentials_settings_menu(user, key)
    elif settings_tab == "accounts":
        account_settings_menu(user, key)


# SECURITY SETTINGS MENU (default)
def security_settings_menu(user, key):
    global settings_tab
    settings_tab = "security"
    updated = None
    while True:
        user_id = user[0]
        settings = load_user_settings(user_id)
        hide_passwords = settings[1] # boolean (default = False)
        clipboard_timeout = settings[2] # integer (default = 60) seconds
        auto_lock_timeout = settings[3] # integer (default = 15) minutes

        clear_screen()
        
        draw_settings_header(settings_tab, user)

        if updated is True:
            print("//ACCEPTED - Setting has been updated.\n")
            updated = False
        elif updated is False:
            print("//USER - No changes made.\n")
        print(" Select an option to edit value.\n")
        print(f"  1. Hide passwords:                   {get_title(str(hide_passwords))}")
        print(f"  2. Clipboard Timeout:                {clipboard_timeout} seconds")
        print(f"  3. Log-out Timer:                    {auto_lock_timeout} minutes")
        print(f"  4. Silence Quit Message:             No")
        print()
        print("  N: Next Page")
        print()
        print("  X: Exit Settings")
        print("  Q: Quit Program")
        print()

        choice = input("> ").strip().lower()
        match choice:
            case "1":
                new_value = toggle_hide_passwords(user_id, "hide_passwords", hide_passwords)
                if hide_passwords != new_value and new_value != None:
                    updated = True
                else:
                    updated = False
            case "2":
                new_value = set_clipboard_timeout(user_id, "clipboard_timeout", clipboard_timeout)
                if clipboard_timeout != new_value and new_value != None:
                    updated = True
                else:
                    updated = False
            case "3":
                new_value = set_auto_lock_timeout(user_id, "auto_lock_timeout", auto_lock_timeout)
                if auto_lock_timeout != new_value and new_value != None:
                    updated = True
                else:
                    updated = False
            case "n":
                credentials_settings_menu(user, key)
            case "x":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "q":
                exit_program()
                break

def get_title(variable):
    match variable:
        case "service":
            variable = "Service (A-Z)"
        case "created_at":
            variable = "Created at (Newest)"
        case "updated_at":
            variable = "Updated at (Newest)"
        case "service (inversed)":
            variable = "Service (Z-A)"
        case "created_at (inversed)":
            variable = "Created at (Oldest)"
        case "updated_at (inversed)":
            variable = "Updated at (Oldest)"

        case "True":
            variable = "Yes"
        case "False":
            variable = "No"

    return variable

def credentials_settings_menu(user, key):
    global settings_tab
    settings_tab = "credentials"
    updated = None
    while True:
        user_id = user[0]
        settings = load_user_settings(user_id)
        default_sort = settings[4] # string (default service)

        clear_screen()
        
        draw_settings_header(settings_tab, user)

        if updated is True:
            print("//ACCEPTED - Setting has been updated.\n")
            updated = False
        elif updated is False:
            print("//USER - No changes made.\n")
        print(" Select an option to edit value.\n")
        print(f"  1. Sort credentials by:        {get_title(default_sort)}")
        print()
        print("  N: Next Page")
        print("  B: Previous Page")
        print()
        print("  X: Exit Settings")
        print("  Q: Quit Program")
        print()
        choice = input("> ").strip().lower()
        match choice:
            case "1":
                new_value = set_default_sort(user_id, "default_sort", default_sort)
                if default_sort != new_value and new_value != None:
                    updated = True
                else:
                    updated = False
            case "b": 
                security_settings_menu(user, key)
            case "n":
                account_settings_menu(user, key)
            case "x":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "q":
                exit_program()
                break

def account_settings_menu(user, key):
    global settings_tab
    settings_tab = "accounts"
    updated = 100
    user_id = user[0]
    username = user[1]

    while True:

        user = get_user(username)
        clear_screen()
        
        draw_settings_header(settings_tab, user)

        if updated == 2:
            print("//ACCEPTED - Setting has been updated.\n")
            updated = False
        elif updated == 1:
            print("//USER - No changes made.\n")
        elif updated == 0: 
            print("//DENIED - Password is incorrect.\n")

        print(f" Username:         {user[1]}")
        print(f" E-mail:           {user[2]}")
        print()
        print(f" Account created:  {user[4].strftime('%b %d, %Y %I:%M %p')}")
        print()
        print("  1. Change Username")
        print("  2. Change E-mail")
        print("  3. Change Master Password")
        print("  4. Delete Account")
        print()
        print("  B: Previous Page")
        print()
        print("  X: Exit Settings")
        print("  Q: Quit Program")
        print()
        choice = input("> ").strip().lower()
        match choice:
            case "1":
                updated, name = change_username_setting(user_id, username)
                if name is not None:
                    username = name
                continue
            case "b": 
                credentials_settings_menu(user, key)
            case "x":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "":
                if breadcrumb[-1].lower() == "menu":
                    back(1)
                    login_options(user, key, None, False, None)
                elif breadcrumb[-1].lower() == "display":
                    back(1)
                    clear_screen()
                    draw_header(user)
                    get_credentials_menu(user, key, False)
                break
            case "q":
                exit_program()
                break

# Main Menu > Log-in > Credentials > Display
def get_credentials_menu(user, key, deletion_success = False):
    breadcrumb.append("Display")
    draw_header(user)

    credentials_list = get_credentials(user)
    
    if deletion_success is True:
        print("//ACCEPTED - Successfully deleted credential.\n")
    
    if credentials_list == None:
        back(2)
        login_options(user, key, False, True, None)
    else:
        credentials_options(user, key, credentials_list)

def sort_credentials(credentials_list, sort_by):
    if not credentials_list:
            return None

    sort_title = ""
    if sort_by == "service":
        credentials_list.sort(key=lambda x: x[2].lower())
        sort_title = "Service (A-Z)"
    elif sort_by == "created_at":
        credentials_list.sort(key=lambda x: x[6])
        sort_title = "Created at (Newest)"
    elif sort_by == "updated_at":
        credentials_list.sort(key=lambda x: x[7])
        sort_title = "Updated at (Newest)"
    elif sort_by == "service (inversed)":
        credentials_list.sort(key=lambda x: x[2].lower(), reverse = True)
        sort_title = "Service (Z-A)"
    elif sort_by == "created_at (inversed)":
        credentials_list.sort(key=lambda x: x[6], reverse = True)
        sort_title = "Created at (Oldest)"
    elif sort_by == "updated_at (inversed)":
        credentials_list.sort(key=lambda x: x[7], reverse = True)
        sort_title = "Updated at (Oldest)"

    return credentials_list, sort_title

def display_credentials(credentials_list, sort_by):
    credentials_list, sort_title = sort_credentials(credentials_list, sort_by)
    count = 0
    print(f" Select an entry for more options.\n")
    for cred_id, user_id, service, username, ciphertext, nonce, created_at, updated_at in credentials_list:
        count += 1
        print(f"  {count}. {service}")
    print(f"\n Displaying by: {sort_title}")

def credentials_options(user, key, credentials_list):
    user_settings = load_user_settings(user[0])
    sort_by = user_settings [4]

    display_credentials(credentials_list, sort_by)

    print()
    print("  S. Settings")
    print("  R. Return")
    print("  Q. Quit Program")
    print()
    option_status = input("> ")
    
    if option_status.lower() == "r" or option_status.lower() == "":
        back(2)
        login_options(user, key, None, False, None)
    elif option_status.lower() == "s":
        settings_menu(user, key)
    elif option_status.lower() == "q":
        exit_program()
    elif option_status.isdigit():
        if int(option_status) > 0 and int(option_status) <= len(credentials_list):
        
            credential_options(user, key, credentials_list[int(option_status) - 1], user_settings, False, False)
    else:
        draw_header(user)
        print("//ERROR - Please select a valid option.\n")

# Main Menu > Log-in > Credentials > View > Service
def credential_options(user, key, credentials, user_settings, cancelled = False, copied_password = False):
    clear_screen()
    breadcrumb.append(credentials[2])
    draw_header(user)
    password_star = "********"
    clipboard_timeout = user_settings[2]
    if cancelled == True:
        print(f" //USER - Operation cancelled, no changes made.\n")
    elif cancelled == None and copied_password == None:
        print(f" //ACCEPTED - Changes updated successfully.\n")
    elif copied_password == True:
        print(f" //USER - Password copied. Clipboard will clear in {clipboard_timeout} seconds.\n")
        password_star = '******** [COPIED]'
    while True:
        print(f" Service:      {credentials[2]}")
        print(f" Created:      {credentials[6].strftime('%b %d, %Y %I:%M %p')}")
        print(f" Last Updated: {credentials[7].strftime('%b %d, %Y %I:%M %p')}")
        print()
        print(f" Username:     {credentials[3]}")
        print(f" Password:     {password_star}")
        print()
        
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
            copy_to_clipboard(password, clipboard_timeout)
            credential_options(user, key, credentials, user_settings, None, True)
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
    settings = load_user_settings(user[0])
    service = input(" Service: ")
    if service.strip() == "":
        login_options(user, key, login_success = False, no_credentials_stored = False, add_success = False)
    
    login_username = input(" Username: ")


    if settings[1] is True:
        password = getpass(" Password: ")
        print_password = "********"
    elif settings[1] is False:
        password = input(" Password: ")
        print_password = password


    value_error = None
    while True:
        if value_error is True:
            print(f" Service:  {service}")
            print(f" Username: {login_username}")
            print(f" Password: {print_password}")
            value_error = False
        print("\nAdd credentials? (Y/N)\n")
        confirm_credential = input("> ")
        if confirm_credential.lower() == "y":
            add_credentials(user, service, login_username, password, key)
            back(2)
            login_options(user, key, login_success = False, no_credentials_stored = False, add_success = True)
            break
        elif confirm_credential.lower() == "n":
            back(2)
            login_options(user, key, login_success = False, no_credentials_stored = False, add_success = False)
            break
        else:
            draw_header(user)
            print("//ERROR - Please select a valid option.\n")
            value_error = True
            continue

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
    user_settings = load_user_settings(user[0])
    hide_password = user_settings[1]

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
        new_password = ""
        if hide_password is True:
            print(f" Current password : ********")
            new_password = getpass("    [New password]: ")
            if new_password != "":
                retype_password = getpass(" [Retype password]: ")
            else: 
                retype_password = ""
                print("                   (no change)")

        elif hide_password is False:
            password = decrypt_secret(key, credential)
            print(f" Current password : {password}")
            new_password = input("    [New password]: ")
            if new_password != "":
                retype_password = input(" [Retype password]: ")
            else: 
                retype_password = ""
                print("                   (no change)")
        if new_password == retype_password:
            if new_service == "" and new_username == "" and new_password == "":
                back(2)
                input("\n//USER - No changes made. Press [ENTER] to continue.")
                credential_options(user, key, credential, user_settings, True, None)
                break
            print()
            print("Proceed with the changes? (Y/N)\n")
            confirm_edit = input("> ")
            if confirm_edit.lower() == 'y':
                updated_credential = edit_credentials(user, key, credential, new_service, new_username, new_password)
                back(2)
                credential_options(user, key, updated_credential, user_settings, None, None)
                break
            elif confirm_edit.lower() == 'n':
                back(1)
                credential_options(user, key, credential, user_settings, True, False)
                break
        else:
            password_fail = True
            continue

def delete_credentials_menu(user, key, credentials):
    breadcrumb.append("Delete")
    clear_screen()
    draw_header(user)
    user_settings = load_user_settings(user[0])

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
            credential_options(user, key, credentials, user_settings, cancelled = True)
            print()
            break
        else:
            draw_header(user)
            print("//ERROR - Please enter a valid option.\n")
            continue



if __name__ ==  "__main__":
    print()