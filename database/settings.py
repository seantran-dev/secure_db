# settings
from .db import get_connection
import os
from getpass import getpass
from database.users import *
from authentication.login import login


def draw_settings_header(current_tab, user = None):
    clear_screen()
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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def load_user_settings(user_id):
    conn = get_connection() 
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM user_settings
        WHERE user_id = %s;
        """,
        (user_id,)
    )

    settings = cur.fetchone()

    cur.close()
    conn.close()

    return settings

def update_setting(user_id, setting, value):
        conn = get_connection() 
        cur = conn.cursor()

        # no SQL injections on my watch...
        allowed = {
        "hide_passwords",
        "clipboard_timeout",
        "auto_lock_timeout",
        "default_sort",
        }

        if setting not in allowed:
            raise ValueError("Invalid setting")
        
        cur.execute(
            f"""
            UPDATE user_settings
            SET {setting} = %s
            WHERE user_id = %s;
            """,
            (value, user_id)
        )

        conn.commit()

        cur.close()
        conn.close()

# Toggle hide password
def toggle_hide_passwords(user_id, setting, current_value):
    value_error = False
    value = ""
    while True:
        clear_screen()
        draw_settings_header("security")
        print(" Enabling this will hide all user/credential password entries and displays.\n")

        if value_error is True:
            print("Please enter a valid option.\n")
            value_error = False

        print("  1. Yes")
        print("  2. No")
        print()
        choice = input("> ")
        if choice == "1":
            value = "True"
            update_setting(user_id, setting, True)
            break
        elif choice == "2":
            value = "False"
            update_setting(user_id, setting, False)
            break
        elif choice == "":
            return None
        else: 
            value_error = True
            continue

    return value

# Clipboard timeout
def set_clipboard_timeout(user_id, setting, current_value):
    value_error = False
    value_negative = False
    while True:
        try:
            clear_screen()
            draw_settings_header("security")
            print(" Set the amount of time after copying a password until it is cleared from the clipboard.")
            print(f"\n Input '0' to disable this function. Current Value: {current_value}")

            if value_error is True:
                print("\nPlease enter a valid number.")
                value_error = False
            elif value_negative == True:
                print("\nPlease enter a number greater than 0, or input '0' to disable.")
                value_negative = False
            print()
            value = input("New Value:  ")
            if value == "":
                return None
            value = int(value)
            if value < 0:
                value_negative = True
                continue
            break
        except ValueError:
            value_error = True
    if value == current_value:
        print("No changes made.")
    else:
        update_setting(user_id, setting, value)

    return value

#
def set_auto_lock_timeout(user_id, setting, current_value):
    value_error = False
    value_negative = False
    while True:
        try:
            clear_screen()
            draw_settings_header("security")
            print(" Set the amount of time after log-in until the user is automatically logged out.")
            print(f"\n Input '0' to disable this function. Current Value: {current_value}")

            if value_error is True:
                print("\nPlease enter a valid number.")
                value_error = False
            elif value_negative == True:
                print("\nPlease enter a number greater than 0, or input '0' to disable.")
                value_negative = False
            print()
            value = input("New Value:  ")
            if value == "":
                return None
            value = int(value)
            if value < 0:
                value_negative = True
                continue
            break
        except ValueError:
            value_error = True
    if value == current_value:
        print("No changes made.")
    else:
        update_setting(user_id, setting, value)
        
    return value

def change_username_setting(user_id, current_username):
    draw_settings_header("accounts")
    password = getpass("Enter password to continue: ")
    user, key = login(current_username, password)
    
    if (user, key) == (None, None):
        return 0, None # failed
    username_taken = False
    while True:
        draw_settings_header("accounts")
        if username_taken is True:
            print(f"Username '{new_username}' is already in use.\n")
            username_taken = False
        print(f" Current Username: {current_username}\n")
        new_username = input(f"     New Username: ")
        if get_user(new_username) is not None:
            username_taken = True
            continue
        elif new_username.strip() == "" or new_username == current_username:
            return 1, None # cancel
        else:
            set_username(user_id, new_username)
            break
        
    return 2, new_username # success




    
def set_default_sort(user_id, setting, current_value):

    value_error = False
    while True:
        clear_screen()
        draw_settings_header("credentials")
        print(" Set how the credentials list is displayed by:\n")
        print("  1. Service name (A-Z)")
        print("  2. Date of creation (Newest)")
        print("  3. Last updated (Newest)")
        print()
        print("  0: Flip the display order of selections")
        print("    (Ex. A-Z becomes Z-A, Newest becomes Oldest)")
        print()
        if value_error == True:
            print("//ERROR - Invalid selection. Please try again.")
            value_error = False
        choice = input("> ")
        if current_value[-10:] == "(inversed)":
            suffix = " (inversed)"
        else:
            suffix = ""
        match choice:
            case "1":
                sort = f"service{suffix}"
                sort_type = "Service name"
            case "2":
                sort = f"created_at{suffix}"
                sort_type = "Date of first entry"
            case "3":
                sort = f"updated_at{suffix}"
                sort_type = "Most recently updated"
            case "0":
                if current_value[-10:] == "(inversed)":
                    sort = current_value[:-11]
                else:
                    sort = f"{current_value} (inversed)"
            case "":
                return None
            case _:
                value_error = True
        if value_error == False:
            update_setting(user_id, setting, sort)
            break
        
    return sort
        

