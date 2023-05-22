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

    if armor_matches > 0:
        add_armor(armor_matches)
    if potion_matches > 0:
        add_health(potion_matches)
    if skill_matches > 0:
        skill_check(skill_matches)
    if sword_matches > 0:
        attack_enemy(sword_matches)
    if enemy_attacks > 0:
        enemy_attack_player(enemy_attacks)

    if player_armor > 0:
        player_status = f"{player_name}'s health: {player_health} | {player_name}'s armor: {player_armor}"
    else:
        player_status = f"{player_name}'s health: {player_health}"
    enemy_status = f"Enemy health: {enemy_health}"
    status_length = max(len(player_status), len(enemy_status))
    print("\n╔" + "═" * status_length + "╗")
    print("║" + player_status.center(status_length) + "║")
    print("║" + enemy_status.center(status_length) + "║")
    print("╚" + "═" * status_length + "╝")

def add_armor(armor_matches):
    global player_armor
    armor_points = 6
    total_armor_points = armor_points * armor_matches
    player_armor += total_armor_points
    print(f"\n{player_name} gains {total_armor_points} armor from matching two armor symbols in a column.")

def add_health(potion_matches):
    global player_health
    health_bonus = 25
    total_health_bonus = health_bonus * potion_matches
    player_health += total_health_bonus
    print(f"\n{player_name} gains {total_health_bonus} health from matching two heart symbols in a row.")

def skill_check(skill_matches):
    global player_attack_power, enemy_health
    skill_modifier = 1.75
    total_attack_power = int(player_attack_power * skill_modifier * skill_matches)
    print(f"\n{player_name} initiates a skilled attack from matching three exclamation symbols in a row.")
    print(f"{player_name} unleashes a powerful skill attack and deals {total_attack_power} damage to the enemy.")
    enemy_health -= total_attack_power

def attack_enemy(sword_matches):
    global player_attack_power, enemy_health, enemy_defense
    damage = max(player_attack_power - enemy_defense, 0)
    total_damage = damage * sword_matches
    enemy_health -= total_damage
    print(f"\n{player_name} initiates an attack from matching two sword symbols in a row.")
    print(f"{player_name} attacks enemy {sword_matches} times and deals {total_damage} damage.")

def enemy_attack_player(enemy_attacks):
    global player_health, player_armor
    player_defense = 5
    damage = max(enemy_attack_power * enemy_attacks, 0)
    total_damage = damage - player_defense

    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        print(f"\nThe enemy initiates an attack from a skull symbol appearing in a row.")
        print(f"Enemy attacks {player_name} {enemy_attacks} times and deals {total_damage} damage after armor absorbtion.")
        print(f"Armor absorbed {armor_reduction} damage.")
    else:
        print(f"\nEnemy attacks {player_name} {enemy_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

# Init #TODO Change these so they're more dynamic and add classes to choose enemies from
player_health = 300
player_attack_power = 14
player_defense = 5
enemy_health = 40
enemy_attack_power = 20
enemy_defense = 2
player_armor = 0

# Gameplay loop
os.system('cls' if os.name == 'nt' else 'clear')
print(logo)
player_name = input("    What is your name? ")
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("== Dungeon Reels ==")
    spin_result = spin_reels()
    process_spin(spin_result)

    if player_health <= 0:
        print(f"\nGame Over! {player_name} is defeated.")
        break
    elif enemy_health <= 0:
        print("\nCongratulations! You've defeated the enemy!")
        break

    choice = input("\nSpin again? (y/n): ")
    if choice.lower() != 'y':
        break

print(f"\nFinal player health: {player_health}")
print(f"Final enemy health: {enemy_health}")
print("\nGoodbye.\n")
