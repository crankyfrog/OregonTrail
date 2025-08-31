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
medicine = 2
party = {
    "Alice": 100,
    "Bob": 100,
    "Charlie": 100
}

landmarks = {20: "Trading Post", 40: "River", 60: "Fort", 80: "River"}

# Events: (text, food_change, health_change, ammo_change, spare_parts_change)
events = [
    ("You found extra food!", 15, 0, 0, 0),
    ("A storm slowed you down.", -2, -5, 0, 0),
    ("Dysentery hits your party!", -10, -20, 0, 0),
    ("All is calm today.", 0, 0, 0, 0),
    ("You hunted successfully and got food.", 20, 0, -5, 0),
    ("Broken wagon wheel! You lost some supplies.", -5, 0, 0, -1),
    ("Bandits stole some supplies!", -10, -5, -5, 0)
]

# -------------------- Functions --------------------
def pause():
    input(GREEN + "\nPress Enter to continue..." + RESET)

def print_status():
    print(CLEAR)
    print(GREEN + f"Day {days} | Miles: {miles}/{max_miles} | Health: {health} | Food: {food} | Ammo: {ammo} | Spare Parts: {spare_parts} | Medicine: {medicine}")
    party_status = ", ".join([f"{name}:{hp}" for name, hp in party.items()])
    print(f"Party: {party_status}" + RESET)

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
    food_loss = random.randint(5, 10)
    food -= food_loss
    print(GREEN + f"\nYou traveled {travel_distance} miles and used {food_loss} food." + RESET)
    pause()

def rest():
    global health, food
    heal = random.randint(5, 15)
    health += heal
    food_loss = random.randint(2, 5)
    food -= food_loss
    print(GREEN + f"\nYou rested and regained {heal} health. Food used: {food_loss}" + RESET)
    pause()

def hunt():
    global food, ammo
    if ammo <= 0:
        print(GREEN + "\nYou have no ammo to hunt!" + RESET)
        pause()
        return
    print(GREEN + "\nHunting... Press Enter at the right moment to shoot!" + RESET)
    pause()
    success = random.choice([True, False])
    ammo_loss = random.randint(2, 5)
    ammo -= ammo_loss
    if success:
        gained = random.randint(10, 30)
        food += gained
        print(GREEN + f"Hunt successful! Gained {gained} food. Ammo used: {ammo_loss}" + RESET)
    else:
        print(GREEN + f"Hunt failed. Ammo used: {ammo_loss}" + RESET)
    pause()

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
        print(GREEN + "You waited a day. Food decreased." + RESET)
        food -= 5
    else:
        print(GREEN + "Invalid choice, you lost a day." + RESET)
        food -= 5
    pause()

def trading_post():
    global food, ammo, spare_parts, medicine
    print(GREEN + "\nWelcome to the Trading Post!" + RESET)
    print(f"Inventory: Food: {food}, Ammo: {ammo}, Spare Parts: {spare_parts}, Medicine: {medicine}")
    print("You can buy supplies (food=10, ammo=5, spare=3, medicine=2 each)")
    choice = input("Buy (F)ood, (A)mmo, (S)pare, (M)edicine, or (N)othing? ").lower()
    if choice == "f":
        food += 10
    elif choice == "a":
        ammo += 5
    elif choice == "s":
        spare_parts += 3
    elif choice == "m":
        medicine += 2
    else:
        print("Nothing purchased.")
    pause()

def random_event():
    global food, health, ammo, spare_parts
    event = random.choice(events)
    text, f_change, h_change, a_change, s_change = event
    food += f_change
    health += h_change
    ammo += a_change
    spare_parts += s_change
    print(GREEN + f"\nEvent: {text}" + RESET)
    pause()

def check_status():
    global health, food, party
    for name in list(party.keys()):
        if party[name] <= 0:
            print(GREEN + f"{name} has died." + RESET)
            del party[name]
            pause()
    if health <= 0 or len(party) == 0:
        game_over("Your party has perished.")
    if food <= 0:
        game_over("You ran out of food and starved.")

# -------------------- Main Loop --------------------
print(GREEN + "\nWelcome to Oregon Trail CLI Ultimate Edition!" + RESET)
pause()

while miles < max_miles:
    print_status()
    ascii_wagon()
    if miles in landmarks:
        landmark = landmarks[miles]
        if landmark == "Trading Post":
            trading_post()
        elif landmark == "River":
            river_crossing()
        elif landmark == "Fort":
            print(GREEN + "\nYou arrived at a Fort. Health restored slightly." + RESET)
            health += 10
            pause()
    
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
        pause()
    
    random_event()
    check_status()
    
    days += 1

# Win condition
print_status()
ascii_wagon()
print(GREEN + f"\nCongratulations {player_name}! You reached Oregon in {days} days!" + RESET)
