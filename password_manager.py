import os
import sys
import string
import pyfiglet
from colorama import Fore, Style

MASTER_KEY = "7869"
SHIFT = 3
ALPHABET = string.ascii_letters + string.digits

def clear_screen_and_print_header(header_text):
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.MAGENTA + pyfiglet.figlet_format(header_text, font="slant") + Style.RESET_ALL)

def main_menu():
    clear_screen_and_print_header("Password Manager")
    options = "1:Add Credential\n2:Search Credential\n3:Edit Credential\n4:Delete Credential\n5:Exit"
    print(Fore.GREEN + options + Style.RESET_ALL)
    choice = int(input())
    handler(choice)

def handler(choice):
    if choice == 1:
        add_credential()
    elif choice == 2:
        search_credential()
    elif choice == 3:
        edit_credential()
    elif choice == 4:
        delete_credential()
    elif choice == 5:
        print("Thank you for using Password Manager.")
        sys.exit(0)
    else:
        print("Please select from the given options.")
    main_menu()

def shift_cipher(text, shift):
    result = ""
    for char in text:
        if char in ALPHABET:
            new_position = (ALPHABET.find(char) + shift) % len(ALPHABET)
            result += ALPHABET[new_position]
        else:
            result += char
    return result

def encryption(password):
    return shift_cipher(password, SHIFT)

def decryption(encrypted_text):
    return shift_cipher(encrypted_text, -SHIFT)

def add_credential():
    clear_screen_and_print_header("Add Credential")
    username = input("Enter Username, you want to save: ") or "UNKNOWN"
    password = input("Enter Strong Password: ") or "UNKNOWN"
    url = input("Enter URL or Application Name you want to Store: ")
    while not url:
        print("\nWarning, URL or Application cannot be empty.")
        url = input("Enter URL or Application Name you want to Store: ")

    encrypted_password = encryption(password)
    data = f"{username} {encrypted_password} {url}\n"
    with open("passwords.txt", 'a') as file:
        file.write(data)

def search_credential():
    clear_screen_and_print_header("Search Credential")
    option = int(input("1: See a Specific Credential \t 2: List All Saved Credentials\n"))

    if option == 1:
        url = input("Enter URL or APP name you want to search: ")
        results = search(url)
        if results:
            print("Search Results:\n")
            for record in results:
                print(record)
        else:
            print("No matching credentials found.")
    elif option == 2:
        key = input("Enter your Master Key: ")
        if key == MASTER_KEY:
            search_all()
        else:
            print("Incorrect Master Key.")

    input("Press Enter to go back to the Main Menu: ")

def search(url):
    with open("passwords.txt", "r") as file:
        results = []
        for line in file:
            if url in line:
                username, encrypted_password, stored_url = line.strip().split()
                password = decryption(encrypted_password)
                results.append(f"Username: {username}, Password: {password}, URL: {stored_url}")
        return results

def search_all():
    with open("passwords.txt", 'r') as file:
        print("Saved Credentials:")
        for line in file:
            username, encrypted_password, url = line.strip().split()
            password = decryption(encrypted_password)
            print(f"Username: {username}, Password: {password}, URL: {url}")

def edit_credential():
    clear_screen_and_print_header("Edit Credential")
    url = input("Enter URL or App name of the credential you want to edit: ")
    results = search(url)

    if not results:
        print("No matching credentials found.")
        return

    for index, record in enumerate(results, start=1):
        print(f"{index}: {record}")

    choice = int(input("\nSelect the credential you want to edit: ")) - 1
    if 0 <= choice < len(results):
        new_username = input("Enter new username (leave blank to keep current): ")
        new_password = input("Enter new password (leave blank to keep current): ")
        edit(url, choice, new_username, new_password)
    else:
        print("Invalid selection.")

    input("Press Enter to go back to the Main Menu: ")

def edit(url, choice, new_username, new_password):
    with open("passwords.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for i, line in enumerate(lines):
            if i == choice and url in line:
                parts = line.strip().split()
                if new_username:
                    parts[0] = new_username
                if new_password:
                    parts[1] = encryption(new_password)
                line = ' '.join(parts) + '\n'
            file.write(line)
        file.truncate()

def edit_credential():
    clear_screen_and_print_header("Edit Credential")
    url = input("Enter URL or App name of the credential you want to edit: ")
    results = search(url)

    if not results:
        print("No matching credentials found.")
        return

    for index, record in enumerate(results, start=1):
        print(f"{index}: {record}")

    choice = int(input("\nSelect the credential you want to edit: ")) - 1
    if 0 <= choice < len(results):
        new_username = input("Enter new username (leave blank to keep current): ")
        new_password = input("Enter new password (leave blank to keep current): ")
        edit(url, choice, new_username, new_password)
    else:
        print("Invalid selection.")

    input("Press Enter to go back to the Main Menu: ")

def edit(url, choice, new_username, new_password):
    with open("passwords.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for i, line in enumerate(lines):
            if i == choice and url in line:
                parts = line.strip().split()
                if new_username:
                    parts[0] = new_username
                if new_password:
                    parts[1] = encryption(new_password)
                line = ' '.join(parts) + '\n'
            file.write(line)
        file.truncate()

def delete_credential():
    clear_screen_and_print_header("Delete Credential")
    url = input("Enter URL or App name of the credential you want to delete: ")
    results = search(url)

    if not results:
        print("No matching credentials found.")
        return

    for index, record in enumerate(results, start=1):
        print(f"{index}: {record}")

    choice = int(input("\nSelect the credential you want to delete: ")) - 1
    if 0 <= choice < len(results):
        # Retrieve the full line to be deleted based on the choice
        line_to_delete = results[choice].split(", ")[2].split(": ")[1]
        delete_line_from_file(line_to_delete)
        print("Credential deleted successfully.")
    else:
        print("Invalid selection.")

    input("Press Enter to go back to the Main Menu: ")

def delete_line_from_file(line_to_delete):
    with open("passwords.txt", "r") as file:
        lines = file.readlines()
    with open("passwords.txt", "w") as file:
        for line in lines:
            if line_to_delete not in line:
                file.write(line)



if __name__ == "__main__":
    main_menu()





