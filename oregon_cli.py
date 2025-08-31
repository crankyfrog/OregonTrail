#!/usr/bin/env python3
import random
import time
import sys

# -------------------- Terminal Colors --------------------
GREEN = "\033[1;32m"
RESET = "\033[0m"
CLEAR = "\033[2J\033[H"

# -------------------- Game Setup --------------------
player_name = input(GREEN + "Enter your name, wagon leader: " + RESET)
days = 0
miles = 0
max_miles = 100
health = 100
food = 100
ammo = 50
spare_parts = 3
party = ["Alice", "Bob", "Charlie"]

# Events: (text, food_change, health_change, ammo_change, spare_parts_change)
events = [
    ("You found extra food!", 15, 0, 0, 0),
    ("A river slowed you down.", -2, 0, 0, 0),
    ("Dysentery hits your party!", -10, -20, 0, 0),
    ("All is calm today.", 0, 0, 0, 0),
    ("You hunted successfully and got food.", 20, 0, -5, 0),
    ("Broken wagon wheel! You lost some supplies.", -5, 0, 0, -1),
    ("Bandits stole some supplies!", -10, -5, -5, 0),
    ("Storm slowed your travel.", -3, -5, 0, 0)
]

# -------------------- Functions --------------------
def print_status():
    print(CLEAR)
    print(GREEN + f"Day {days} | Miles: {miles}/{max_miles} | Health: {health} | Food: {food} | Ammo: {ammo} | Spare Parts: {spare_parts}")
    print(f"Party: {', '.join(party)}" + RESET)

def ascii_wagon():
    wagon = GREEN + r"""
       ______
     _/[] []\_
    /_ [] [] _\
      O    O
    """ + RESET
    print(wagon)

def game_over(reason):
    print(GREEN + "\n" + reason)
    print("Game Over!" + RESET)
    sys.exit()

def travel():
    global miles, food
    travel_distance = random.randint(5, 15)
    miles += travel_distance
    food -= random.randint(5, 10)
    print(GREEN + f"\nYou traveled {travel_distance} miles." + RESET)

def rest():
    global health, food
    heal = random.randint(5, 15)
    health += heal
    food -= random.randint(2, 5)
    print(GREEN + f"\nYou rested and regained {heal} health." + RESET)

def hunt():
    global food, ammo
    if ammo <= 0:
        print(GREEN + "\nYou have no ammo to hunt!" + RESET)
        return
    success = random.choice([True, False])
    ammo -= random.randint(2, 5)
    if success:
        gained = random.randint(10, 30)
        food += gained
        print(GREEN + f"\nHunt successful! Gained {gained} food." + RESET)
    else:
        print(GREEN + "\nHunt failed, ammo spent." + RESET)

def river_crossing():
    global health, spare_parts, miles
    print(GREEN + "\nYou encounter a river!" + RESET)
    choice = input("Do you want to (F)ord, (R)aft, or (W)ait? ").lower()
    if choice == "f":
        if random.randint(0, 1):
            print(GREEN + "You forded safely." + RESET)
            miles += 5
        else:
            print(GREEN + "Wagon damaged! Health lost." + RESET)
            health -= 15
            spare_parts -= 1
    elif choice == "r":
        if spare_parts > 0:
            print(GREEN + "You built a raft and crossed safely." + RESET)
            spare_parts -= 1
            miles += 5
        else:
            print(GREEN + "No spare parts! Forced to wait." + RESET)
            health -= 5
    elif choice == "w":
        print(GREEN + "You waited a day. Nothing happened." + RESET)
        food -= 5
    else:
        print(GREEN + "Invalid choice, you lost a day." + RESET)
        food -= 5

def random_event():
    global food, health, ammo, spare_parts
    event = random.choice(events)
    text, f_change, h_change, a_change, s_change = event
    food += f_change
    health += h_change
    ammo += a_change
    spare_parts += s_change
    print(GREEN + f"\nEvent: {text}" + RESET)

def check_status():
    global health, food
    if health <= 0:
        game_over("Your party has perished due to illness or injury.")
    if food <= 0:
        game_over("You ran out of food and starved.")

# -------------------- Main Loop --------------------
print(GREEN + "\nWelcome to Oregon Trail CLI Deluxe!" + RESET)
time.sleep(1)

while miles < max_miles:
    print_status()
    ascii_wagon()
    print("\nActions: (T)ravel, (R)est, (H)unt, (C)ross River")
    action = input("Choose action: ").lower()
    
    if action == "t":
        travel()
    elif action == "r":
        rest()
    elif action == "h":
        hunt()
    elif action == "c":
        river_crossing()
    else:
        print(GREEN + "\nInvalid choice. You lost a day." + RESET)
    
    # Random event
    random_event()
    check_status()
    
    days += 1
    time.sleep(1)

# Win condition
print_status()
ascii_wagon()
print(GREEN + f"\nCongratulations {player_name}! You reached Oregon in {days} days!" + RESET)
