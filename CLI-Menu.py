# Function 1: Get Random Activity

import requests
import random
import os

FAVORITES_FILE = "favorites.txt"

# global list to save favorite activities in memory
favorite_activities = []


# ===============File Function===============#
def load_favorites():
    """load saved activities from file into memory"""
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                favorite_activities.append(line.strip())


def save_to_file(activity):
    """save a single activity to the favorites file"""
    with open(FAVORITES_FILE, "a", encoding="utf-8") as f:
        f.write(activity + "\n")


def save_option(activity):
    """ask user if they want to save an activity"""
    choice = input("Do you want to save this activity? (y/n): ").lower()
    if choice == "y":
        favorite_activities.append(activity["activity"])
        save_to_file(activity["activity"])
        print("activity saved!")


# ================Activity Function============#


def get_random_activity():
    """Get a completely random activity suggestion
    API: https://bored-api.appbrewery.com/random
    """
    try:
        response = requests.get("https://bored-api.appbrewery.com/random")
        response.raise_for_status()
        data = response.json()

        print("\nRandom Activity Suggestion:")
        print(f"Activity: {data['activity']}")
        print(f"Type: {data['type']}")
        print(f"Participants: {data['participants']}")

        save_option(data)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching random activity: {e}")


# Function 2: Get Activity by Type


def get_activity_by_type():
    """Let user choose an activity type and get a suggestion
    API: https://bored-api.appbrewery.com/filter?type={type}
    Types: education, recreational, social, diy, charity, cooking, relaxation, music, busywork
    """
    activity_types = [
        "education",
        "recreational",
        "social",
        "diy",
        "charity",
        "cooking",
        "relaxation",
        "music",
        "busywork",
    ]
    print("\nAvailable types:", ",".join(activity_types))
    chosen_type = input("Enter a type: ").lower().strip()

    if chosen_type not in activity_types:
        print("Invalid type! please choose from the list.")
        return

    try:
        response = requests.get(
            f"https://bored-api.appbrewery.com/filter?type={chosen_type}"
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            print("No activities found for this type.")
            return

        activity = random.choice(data)
        print("\nActivity Suggestion:")
        print(f"Activity: {activity['activity']}")
        print(f"Type: {activity['type']}")
        print(f"Participants: {activity['participants']}")

        save_option(activity)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching activity by type: {e}")


# Function 3: Get Activity by Participants


def get_activity_by_participants():
    """Get activity suggestions based on number of participants
    API: https://bored-api.appbrewery.com/filter?participants={number}
    """
    try:
        participants = int(input("\nEnter number of participants: "))
        if participants < 1:
            print("number must be at least 1.")
            return

        response = requests.get(
            f"https://bored-api.appbrewery.com/filter?participants={participants}"
        )
        response.raise_for_status()
        data = response.json()

        if not data:
            print("No activities found for that number of participants.")
            return

        activity = random.choice(data)
        print("\nActivity Suggestion:")
        print(f"Activity: {activity['activity']}")
        print(f"Type: {activity['type']}")
        print(f"Participants: {activity['participants']}")

        save_option(activity)

    except ValueError:
        print("please enter a valid number.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching activity by participants: {e}")


# Function 6: View Saved Activities


def view_saved_activities():
    """
    Read and display saved activities from file
    """
    if not favorite_activities:
        print("\nNo saved activities yet!")
        return

    print("\nYour saved activities:")
    for idx, act in enumerate(favorite_activities, 1):
        print(f"{idx}. {act}")


# Main Function & Menu System

import requests


def show_menu():
    """Display the main menu"""
    print("\nBored Activity Finder")
    print("=" * 21)
    print("1. Get a random activity")
    print("2. Get activity by type")
    print("3. Get activity by participants")
    print("4. View my saved activities")
    print("5. Exit")


def main():
    """Main function with menu loop"""
    print("Welcome to the Bored Activity Finder!")

    load_favorites()

    while True:
        show_menu()

        try:
            choice = input("\nChoose an option (1-7): ")

            if choice == "1":
                get_random_activity()
            elif choice == "2":
                get_activity_by_type()
            elif choice == "3":
                get_activity_by_participants()
            elif choice == "4":
                view_saved_activities()
            elif choice == "5":

                print("Thanks for using Bored Activity Finder!")
                break
            else:
                print("Invalid choice! Please choose 1-5.")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


# ===========Run App==============#

if __name__ == "__main__":
    main()
