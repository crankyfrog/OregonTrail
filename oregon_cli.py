#!/usr/bin/env python3
import random
import time

# Game setup
player_name = input("Enter your name, wagon leader: ")
days = 0
miles = 0
food = 100
health = 100

events = [
    "You found extra food!",
    "A river slowed you down.",
    "Dysentery hits your party!",
    "All is calm today.",
    "You hunted successfully and got food."
]

print(f"\nWelcome {player_name} to the Oregon Trail CLI Adventure!\n")
time.sleep(1)

while miles < 100:
    print(f"\nDay {days} - Miles traveled: {miles} - Food: {food} - Health: {health}")
    action = input("Do you want to (T)ravel or (R)est? ").lower()

    if action == "t":
        travel = random.randint(5, 15)
        miles += travel
        food -= random.randint(5, 10)
        print(f"You traveled {travel} miles.")
    elif action == "r":
        health += random.randint(5, 15)
        food -= random.randint(2, 5)
        print("You rested and regained some health.")
    else:
        print("Invalid choice. You lost a day.")
    
    # Random event
    event = random.choice(events)
    print(f"Event: {event}")
    if "Dysentery" in event:
        health -= random.randint(10, 30)
    elif "extra food" in event or "hunted" in event:
        food += random.randint(10, 25)
    
    # Check status
    if health <= 0:
        print("\nYour party has perished. Game Over!")
        break
    if food <= 0:
        print("\nYou ran out of food and starved. Game Over!")
        break
    
    days += 1
    time.sleep(1)

if miles >= 100:
    print(f"\nCongratulations {player_name}! You reached Oregon in {days} days.")
