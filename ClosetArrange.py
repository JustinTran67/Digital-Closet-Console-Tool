import random
import pickle
import os

class ClosetArrange:
    
    def __init__(self, user = "Guest", password = "", closet = {}):
        self.user = user
        self.password = password
        self.closet = closet
    
    def add_to_closet(self):
        type = input('what kind of item are you putting into your closet?: ')
        article = input('what exactly are you putting into your closet?: ')
        if type in self.closet:
            self.closet[type.lower()].append(article.lower())
        else:
            self.closet[type.lower()] = []
            self.closet[type.lower()].append(article.lower())
    
    def remove_from_closet(self):
        if not self.closet:
            print("Your closet is empty. Nothing to remove.")
        else:
            starting_input = input('What category of items do you want to remove from?: ')
            if starting_input in self.closet:
                item_to_remove = input(f'What item do you want to remove from {starting_input}?: ')
                if item_to_remove.lower() in self.closet[starting_input.lower()]:
                    condition = input(f"Are you sure you want to remove {item_to_remove} from {starting_input}? (yes/no): ")
                    if condition.lower() != 'yes':
                        print("Removal cancelled.")
                    else:
                        self.closet[starting_input.lower()].remove(item_to_remove.lower())
                        print(f"{item_to_remove.capitalize()} has been removed from {starting_input}.")
                else:
                    print(f"Sorry, {item_to_remove} is not in your {starting_input} category.")
            else:
                print(f'Sorry you dont have a category named "{starting_input}".')
    
    def display_closet(self):
        if not self.closet:
            print("Your closet is empty.")
        else:
            for type, articles in self.closet.items():
                print(f"{type.capitalize()}: {', '.join(articles)}")
    
    def choose_item(self):
        if not self.closet:
            print("Your closet is empty. Please add items before I choose one.")
        else:
            starting_input = input('What category of items do you want me to choose from? Or I can choose from all categories: ')
            if starting_input.lower() != "all":
                if starting_input in self.closet:
                    chosen_item = random.choice(self.closet[starting_input.lower()])
                    print(f"Today you should consider wearing your: {chosen_item.capitalize()}")
                else:
                    print(f"Sorry, you don't have any items in the category '{starting_input}'.")
                    self.choose_item()
            else:
                all_items = [item for articles in self.closet.values() for item in articles]
                chosen_item = random.choice(all_items)
                print(f"Today you should consider wearing your: {chosen_item.capitalize()}")

    def save_profile(self):
        if self.user.lower() != 'guest':
            with open(f'{self.user}_closet.pkl', 'wb') as file:
                pickle.dump(self.closet, file)
            print("Profile saved successfully.")
        else:
            print("Guest users cannot save profiles. Please create a user account to save your closet.")

    def load_profile(self):
        try:
            with open(f'{self.user}_closet.pkl', 'rb') as file:
                self.closet = pickle.load(file)
                print("Profile loaded successfully.")
        except FileNotFoundError:
            print("No saved profile found. Starting with an empty closet.")

    def set_password(self):
        with open(f'{self.user}_password.pkl', 'wb') as file:
            pickle.dump(self.password, file)
            print("Password set successfully.")
    
    def load_password(self):
        try:
            with open(f'{self.user}_password.pkl', 'rb') as file:
                self.password = pickle.load(file)
        except FileNotFoundError:
            self.password = input("New Account. Welcome! Please set a password: ")
            self.set_password()
            self.load_password()

    def login(self):
        prompt = input("Welcome to ClosetArrange! Would you like to use an account? (yes/no): ")
        if "yes" in prompt.lower() or "y" in prompt.lower():
            self.user = input('Enter your unsername: ')
            self.load_password()
            security = input('Please enter your password: ')
            security_count = 0
            while security != self.password:
                security = input('Incorrect password. Please try again: ')
                security_count += 1
                if security_count >= 2:
                    print("Too many incorrect attempts. Exiting.")
                    exit()
            print(f"Welcome, {self.user}!")
            self.load_profile()
        else:
            print("You are logged in as Guest. You can add items but cannot save your closet.")
        
    def delete_account_data(self):
        confirm = input("Are you sure you want to delete your account data? (yes/no): ")
        if 'yes' in confirm.lower() or 'y' in confirm.lower():
            try:
                os.remove(f'{self.user}_closet.pkl')
                os.remove(f'{self.user}_password.pkl')
                print("Account data deleted successfully.")
            except FileNotFoundError:
                print("No saved profile found to delete.")
        else:
            print("Account data deletion cancelled.")

    def start(self):
        starting_input = input('How would you like to use your closet?: ')
        if "add" in starting_input.lower() or "put" in starting_input.lower() or "place" in starting_input.lower() or "rack" in starting_input.lower():
            self.add_to_closet()
        elif "display" in starting_input.lower() or "show" in starting_input.lower() or "view" in starting_input.lower() or "list" in starting_input.lower():
            self.display_closet()
        elif "choose" in starting_input.lower() or "pick" in starting_input.lower() or "select" in starting_input.lower() or "random" in starting_input.lower():
            self.choose_item()
        elif "remove" in starting_input.lower() or "delete" in starting_input.lower():
            prompt = input('What would you like to delete?: ')
            if "account" in prompt.lower() or "data" in prompt.lower():
                self.delete_account_data()
            elif "item" in prompt.lower() or "article" in prompt.lower() or "clothes" in prompt.lower() or "clothing" in prompt.lower():
                self.remove_from_closet()
            else:
                print("Invalid input. Please try again.")
        elif "save" in starting_input.lower() or "store" in starting_input.lower():
            self.save_profile()
        else:
            print("Invalid input. Please try again.")
    
new_user = ClosetArrange()
new_user.login()
new_user.start()
continue_use = 'yes'
while continue_use == 'yes':
    continue_use = input("would you like to continue using your closet? (yes/no): ")
    if "yes" in continue_use.lower():
        new_user.start()