import random
import os
from art import logo


symbols = {
    'armor': '🛡️ ',
    'sword': '🗡️ ',
    'potion': '❤️ ',
    'skill': ' ‼️',
    'escape': '🏃',
    'enemy': '💀'
}

enemies = [
    {
        'name': 'Goblin',
        'health': 40,
        'attack_power': 20,
        'defense': 2
    },
    {
        'name': 'Skeleton',
        'health': 50,
        'attack_power': 18,
        'defense': 3
    },
    {
        'name': 'Orc',
        'health': 60,
        'attack_power': 25,
        'defense': 5
    }
]


def select_enemy():
    return random.choice(enemies)

def spin_reels():
    num_reels = 3
    num_rows = 3
    result = []
    for _ in range(num_rows):
        row_result = []
        for _ in range(num_reels):
            symbol = random.choice(list(symbols.keys()))
            row_result.append(symbols[symbol])
        result.append(row_result)
    return result

def process_spin(result):
    for row in result:
        print("   ".join(row))

    armor_matches = 0
    sword_matches = 0
    potion_matches = 0
    enemy_attacks = 0
    skill_matches = 0

    for col in range(len(result[0])):
        column_symbols = [result[row][col] for row in range(len(result))]
        if column_symbols.count('🛡️ ') >= 2:
            armor_matches += 1
    for row in result:
        if row.count('❤️ ') >= 2:
            potion_matches += 1
        if row.count(' ‼️') == 3:
            skill_matches += 1
        if row.count('🗡️ ') >= 2:
            sword_matches += 1
        if '💀' in row:
            enemy_attacks += 1
    print("============")
    if armor_matches > 0:
        add_armor(armor_matches)
    if potion_matches > 0:
        add_health(potion_matches)
    if skill_matches > 0:
        skill_check()
    if sword_matches > 0:
        attack_enemy(sword_matches)
    if enemy_attacks > 0:
        enemy_attack_player(enemy_attacks)

    if player_armor > 0:
        player_status = f"{player_name}'s health: {player_health} | {player_name}'s armor: {player_armor}"
    else:
        player_status = f"{player_name}'s health: {player_health}"
    enemy_status = f"{enemy_name}'s health: {enemy_health}"
    status_length = max(len(player_status), len(enemy_status))
    print("\n╔" + "═" * status_length + "╗")
    print("║" + player_status.center(status_length) + "║")
    print("║" + enemy_status.center(status_length) + "║")
    print("╚" + "═" * status_length + "╝")

def add_armor(armor_matches):
    global player_armor
    armor_points = 10
    total_armor_points = armor_points * armor_matches
    player_armor += total_armor_points
    if armor_matches == 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching two armor symbols in a column.")
    elif armor_matches > 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching two armor symbols {armor_matches} times in each column.")

def add_health(potion_matches):
    global player_health
    health_bonus = 15
    total_health_bonus = health_bonus * potion_matches
    player_health += total_health_bonus
    if potion_matches == 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching two heart symbols in a row.")
    elif potion_matches > 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching two heart symbols {potion_matches} times in each row.")

def skill_check():
    global player_attack_power, enemy_health
    skill_modifier = 1.75
    total_attack_power = int(player_attack_power * skill_modifier)
    print(f"\n{player_name} unleashes a powerful skill attack from matching three exclamation symbols in a row.")
    print(f"{player_name} deals {total_attack_power} damage to {enemy_name}.")
    enemy_health -= total_attack_power

def attack_enemy(sword_matches):
    global player_attack_power, enemy_health, enemy_defense
    damage = max(player_attack_power - enemy_defense, 0)
    total_damage = damage * sword_matches
    enemy_health -= total_damage
    print(f"\n{player_name} initiates an attack from matching two sword symbols in a row.")
    print(f"{player_name} attacks {enemy_name} {sword_matches} times and deals {total_damage} damage.")

def enemy_attack_player(enemy_attacks):
    global player_health, player_armor, player_defense
    damage = max(enemy_attack_power - player_defense, 0)
    total_damage = damage * enemy_attacks

    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        print(f"\n{enemy_name} initiates an attack from a skull symbol appearing in a row.")
        print(f"{enemy_name} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage after armor absorption.")
        print(f"Your armor absorbed {armor_reduction} damage.")
    else:
        print(f"\n{enemy_name} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

#! Program init
def start_game():
    global player_name, enemy, enemy_name, enemy_health, enemy_attack_power, enemy_defense, player_health, player_attack_power, player_armor, player_defense, defeated_enemy_count
    enemy = select_enemy()
    enemy_name = enemy['name']
    enemy_health = enemy['health']
    enemy_attack_power = enemy['attack_power']
    enemy_defense = enemy['defense']
    player_health = 300
    player_attack_power = 14
    player_defense = 6
    player_armor = 0
    defeated_enemy_count = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    choice = input("Need instructions? (y/n): ")
    if choice.lower() == 'y':
        print("\nGame instructions go here..")
        input("\nPress any key to continue")
        os.system('cls' if os.name == 'nt' else 'clear')
        print(logo)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(logo)
    player_name = input("    What is your name? ")
    #! Gameplay loop
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("============")
        spin_result = spin_reels()
        process_spin(spin_result)

        if player_health <= 0:
            print(f"\nGame Over! {player_name} was killed by {enemy_name}.")
            break
        elif enemy_health <= 0:
            defeated_enemy_count += 1
            print(f"\nCongratulations! You've defeated {enemy_name}!")

            choice = input("\nKeep exploring the dungeon? (y/n): ")
            if choice.lower() != 'y':
                break
            enemy = select_enemy()
            enemy_name = enemy['name']
            enemy_health = enemy['health']
            enemy_attack_power = enemy['attack_power']
            enemy_defense = enemy['defense']
            continue
        choice = input("\nSpin again? (y/n): ")
        if choice.lower() != 'y':
            break

    if defeated_enemy_count == 1:
        print(f"\nYou have defeated {defeated_enemy_count} enemy.")
    elif defeated_enemy_count > 1:
        print(f"\nYou have defeated {defeated_enemy_count} enemies.")
    choice = input("\nStart a new game? (y/n): ")
    if choice.lower() == 'n':
        print("\nGoodbye.\n")
        exit()
    elif choice.lower() == 'y':
        start_game()


start_game()