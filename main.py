import random
import os
import time
from art import logo
from enemylist import enemies


symbols = {
    'armor': '🛡️ ',
    'sword': '🗡️ ',
    'heart': '❤️ ',
    'skill': '➕',
    'escape': '🏃',
    'enemy': '💀'
}

player = {
    'level': 1,
    'xp': 0,
    'max_health': 300,
    'health': 300,
    'attack_power': 14,
    'defense': 5,
    'armor': 0
}

level_up_stats = {
    2: {'experience': 30, 'health': 350, 'attack_power': 3, 'defense': 2},
    3: {'experience': 60, 'health': 400, 'attack_power': 4, 'defense': 3},
    4: {'experience': 100, 'health': 450, 'attack_power': 8, 'defense': 4},
    5: {'experience': 150, 'health': 500, 'attack_power': 10, 'defense': 5},
    6: {'experience': 210, 'health': 550, 'attack_power': 12, 'defense': 6},
    7: {'experience': 280, 'health': 600, 'attack_power': 14, 'defense': 7},
    8: {'experience': 360, 'health': 650, 'attack_power': 16, 'defense': 8},
    9: {'experience': 450, 'health': 700, 'attack_power': 18, 'defense': 9},
    10: {'experience': 550, 'health': 750, 'attack_power': 20, 'defense': 10},
    11: {'experience': 660, 'health': 800, 'attack_power': 22, 'defense': 11},
    12: {'experience': 780, 'health': 850, 'attack_power': 24, 'defense': 12},
    13: {'experience': 910, 'health': 900, 'attack_power': 26, 'defense': 13},
    14: {'experience': 1050, 'health': 950, 'attack_power': 28, 'defense': 14},
    15: {'experience': 1200, 'health': 1000, 'attack_power': 30, 'defense': 15},
    16: {'experience': 1360, 'health': 1050, 'attack_power': 32, 'defense': 16},
    17: {'experience': 1530, 'health': 1100, 'attack_power': 34, 'defense': 17},
    18: {'experience': 1710, 'health': 1150, 'attack_power': 36, 'defense': 18},
    19: {'experience': 1900, 'health': 1200, 'attack_power': 38, 'defense': 19},
    20: {'experience': 2100, 'health': 1250, 'attack_power': 40, 'defense': 20}
}


def earn_experience(enemy_xp):
    global xp, player_level
    xp += enemy_xp
    while (player_level + 1) in level_up_stats and xp >= level_up_stats[player_level + 1]['experience']:
        level_up()

def level_up():
    global player_level, player_health, player_max_health, player_attack_power, player_defense
    if (player_level + 1) in level_up_stats:
        requirements = level_up_stats[player_level + 1]
        player_level += 1
        player_health = requirements['health']
        player_max_health = requirements['health']
        player_attack_power += requirements['attack_power']
        player_defense += requirements['defense']
        print(f"You have reached level {player_level}! Your attributes have increased and you've regained health!")

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

def process_spin(result):  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    global charge_modifier, xp
    for row in result:
        print("   ".join(row))
        time.sleep(0.3)

    escape_matches = 0
    armor_matches = 0
    heart_matches = 0
    skill_matches = 0
    critical_matches = 0
    sword_matches = 0
    enemy_attacks = 0
    enemy_critical_attacks = 0

    for col in range(len(result[0])):
        column_symbols = [result[row][col] for row in range(len(result))]
        if column_symbols.count('🏃') == 3:
            escape_matches += 1
        if column_symbols.count('🛡️ ') >= 2:
            armor_matches += 1
        if column_symbols.count('❤️ ') == 3:
            heart_matches += 1
    for row in result:
        if row.count('❤️ ') == 3:
            heart_matches += 1
        if row.count('➕') == 3:
            skill_matches += 1
        if row.count('🗡️ ') >= 3:
            critical_matches += 1
        if row.count('🗡️ ') >= 2:
            sword_matches += 1
        if row.count('💀') >= 3:
            enemy_critical_attacks += 1
        if row.count('💀') >= 2:
            enemy_attacks += 1
    print("━═━═━═━═━═━═")
    time.sleep(0.5)
    if charge_modifier > 1:
        print("\n─⊳ Charge active!")
    if escape_matches > 0:
        escape_combat()
    if armor_matches > 0 and escape_matches == 0:
        add_armor(armor_matches)
    if heart_matches > 0 and escape_matches == 0:
        add_health(heart_matches)
    if skill_matches > 0 and escape_matches == 0:
        skill_check()
    if critical_matches > 0 and escape_matches == 0 and skill_matches == 0:
        attack_enemy_crit(critical_matches)
    if sword_matches > 0 and escape_matches == 0 and skill_matches == 0 and critical_matches == 0:
        attack_enemy(sword_matches)
    if enemy_critical_attacks > 0 and escape_matches == 0 and not defeated_enemy:
        enemy_attack_player_crit(enemy_critical_attacks)
    if enemy_attacks > 0 and escape_matches == 0 and enemy_critical_attacks == 0 and not defeated_enemy:
        enemy_attack_player(enemy_attacks)
    charge_modifier = 1

    if player_armor > 0:
        player_status = f"{player_name}'s HP: {max(player_health, 0)}/{player_max_health} ({player_armor} Armor)"
    else:
        player_status = f"{player_name}'s HP: {max(player_health, 0)}/{player_max_health}"
    player_xp_status = f"Level {player_level} ({xp}/{level_up_stats[player_level + 1]['experience']} XP)"
    enemy_status = f"{enemy_name}'s HP: {max(enemy_health, 0)}"
    status_length = max(len(player_status), len(player_xp_status), len(enemy_status))
    print("\n╔" + "═" * status_length + "╗")
    print("║" + player_status.center(status_length) + "║")
    print("║" + player_xp_status.center(status_length) + "║")
    print("║" + " " * status_length + "║")
    print("║" + enemy_status.center(status_length) + "║")
    print("╚" + "═" * status_length + "╝")

def escape_combat():
    global enemy_health
    print(f"\n{player_name} triggers an escape by matching 3 🏃 symbols in a column.")
    print(f"{player_name} successfully runs from the {enemy_name.lower()}.")
    enemy_health = 0

def add_armor(armor_matches):
    global player_armor, charge_modifier
    armor_points = 4
    total_armor_points = round(armor_points * armor_matches * charge_modifier)
    player_armor += total_armor_points
    if armor_matches == 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols in a column.")
    elif armor_matches > 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols {armor_matches} times in a column.")

def add_health(heart_matches):
    global player_health, charge_modifier
    health_bonus = 20
    total_health_bonus = round(health_bonus * heart_matches * charge_modifier)
    player_health += total_health_bonus
    player_health = min(player_health, player_max_health)
    if heart_matches == 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols in a row.")
    elif heart_matches > 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols {heart_matches} times in a row.")

def skill_check():
    global player_attack_power, enemy_health, charge_modifier, defeated_enemy
    skill_modifier = 1.85 * charge_modifier
    total_attack_power = round(player_attack_power * skill_modifier)
    print(f"\n{player_name} unleashes a powerful skill attack from matching 3 ➕ symbols in a row.")
    print(f"{player_name} deals {total_attack_power} damage to the {enemy_name.lower()}, bypassing their defense.")
    enemy_health -= total_attack_power
    if enemy_health <= 0:
        defeated_enemy = True

def attack_enemy_crit(critical_matches):
    global player_attack_power, enemy_health, enemy_defense, charge_modifier, defeated_enemy
    damage = max(player_attack_power - enemy_defense, 0)
    total_damage = round(damage * critical_matches * charge_modifier * 1.5)
    enemy_health -= total_damage
    if enemy_health <= 0:
        defeated_enemy = True
    print(f"\n{player_name} initiates a critical attack from matching 3 🗡️  symbols in a row.")
    if critical_matches == 1:
        print(f"{player_name} attacks the {enemy_name.lower()} and deals {total_damage} damage.")
    elif critical_matches > 1:
        print(f"{player_name} attacks the {enemy_name.lower()} {critical_matches} times and deals {total_damage} damage.")

def attack_enemy(sword_matches):
    global player_attack_power, enemy_health, enemy_defense, charge_modifier, defeated_enemy
    damage = max(player_attack_power - enemy_defense, 0)
    total_damage = round(damage * sword_matches * charge_modifier)
    enemy_health -= total_damage
    if enemy_health <= 0:
        defeated_enemy = True
    print(f"\n{player_name} initiates an attack from matching 2 🗡️  symbols in a row.")
    if sword_matches == 1:
        print(f"{player_name} attacks the {enemy_name.lower()} and deals {total_damage} damage.")
    elif sword_matches > 1:
        print(f"{player_name} attacks the {enemy_name.lower()} {sword_matches} times and deals {total_damage} damage.")

def enemy_attack_player_crit(enemy_critical_attacks):
    global enemy_attack_power, player_health, player_armor, player_defense, charge_modifier
    damage = max(enemy_attack_power - player_defense, 0)
    total_damage = round(damage * enemy_critical_attacks * charge_modifier * 1.5)
    print(f"\nThe {enemy_name.lower()} initiates a critical attack from matching 3 💀 symbols in a row.")
    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        if enemy_critical_attacks == 1:
            print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage after armor absorption.")
        elif enemy_critical_attacks > 1:
            print(f"The {enemy_name.lower()} attacks {player_name} {enemy_critical_attacks} times and deals {total_damage} damage after armor absorption.")
        print(f"Your armor absorbed {armor_reduction} damage.")
    elif enemy_critical_attacks == 1:
        print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage.")
    elif enemy_critical_attacks > 1:
        print(f"The {enemy_name.lower()} attacks {player_name} {enemy_critical_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

def enemy_attack_player(enemy_attacks):
    global enemy_attack_power, player_health, player_armor, player_defense, charge_modifier
    damage = max(enemy_attack_power - player_defense, 0)
    total_damage = round(damage * enemy_attacks * charge_modifier)
    print(f"\nThe {enemy_name.lower()} initiates an attack from matching 2 💀 symbols in a row.")
    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        if enemy_attacks == 1:
            print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage after armor absorption.")
        elif enemy_attacks > 1:
            print(f"The {enemy_name.lower()} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage after armor absorption.")
        print(f"Your armor absorbed {armor_reduction} damage.")
    elif enemy_attacks == 1:
        print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage.")
    elif enemy_attacks > 1:
        print(f"The {enemy_name.lower()} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

#! Program init
def start_game():  # sourcery skip: extract-method, low-code-quality
    global player_name, enemy, enemy_name, enemy_health, enemy_attack_power, enemy_defense, enemy_xp, player_max_health, player_health, player_attack_power, player_defense, player_armor, player_level, xp, defeated_enemy_count, defeated_enemy, charge_modifier, score
    enemy = select_enemy()
    enemy_name = enemy['name']
    enemy_health = enemy['health']
    enemy_attack_power = enemy['attack_power']
    enemy_defense = enemy['defense']
    enemy_xp = enemy['xp']
    player_max_health = player['max_health']
    player_health = player['health']
    player_attack_power = player['attack_power']
    player_defense = player['defense']
    player_armor = player['armor']
    player_level = player['level']
    xp = player["xp"]
    defeated_enemy_count = 0
    defeated_enemy = False
    charge_modifier = 1
    score = 0
    game_over = False
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    time.sleep(0.8)
    while True:
        choice = input("\nNeed instructions? (y/n): ")
        if choice.lower() == 'n':
            break
        elif choice.lower() == 'y':
            print("\nMatched symbols:")
            print("🗡️ : 2 in a row for an ATTACK")
            print("🗡️ : 3 in a row for a CRITICAL HIT")
            print("➕: 3 in a row for a SKILLED ATTACK")
            print("💀: 2 in a row for an ENEMY ATTACK")
            print("💀: 3 in a row for an ENEMY CRITICAL HIT")
            print("🛡️ : 2 in a column to buff ARMOR")
            print("❤️ : 3 in a row or column to buff HEALTH")
            print("🏃: 3 in a column to ESCAPE")
            print("\nSurvive and defeat as many enemies as possible.")
            input("\nPress any key to continue..")
            break
        else:
            continue
    os.system('cls' if os.name == 'nt' else 'clear')
    print(logo)
    player_name = input("\n    What is your name? ")
    #! Gameplay loop
    while not game_over:
        os.system('cls' if os.name == 'nt' else 'clear')
        time.sleep(0.2)
        print("━═━═━═━═━═━═")
        spin_result = spin_reels()
        time.sleep(0.3)
        process_spin(spin_result)

        if player_health <= 0:
            game_over = True
            print(f"\nGame Over! {player_name} was killed by the {enemy_name.lower()}.")
            break
        elif enemy_health <= 0:
            defeated_enemy_count += 1
            print(f"\nCongratulations! You've defeated the {enemy_name.lower()} and gained {enemy_xp} XP!")
            earn_experience(enemy_xp)
            while not game_over:
                choice = input("\nKeep exploring the dungeon? (y/n): ")
                if choice.lower() == 'n':
                    game_over = True
                    break
                elif choice.lower() == 'y':
                    break
                else:
                    continue
            enemy = select_enemy()
            defeated_enemy = False
            enemy_name = enemy['name']
            enemy_health = enemy['health']
            enemy_attack_power = enemy['attack_power']
            enemy_defense = enemy['defense']
            enemy_xp = enemy['xp']
            continue
        while not game_over:
            print("\n1. Attack")
            print("2. Charge (2.5x modifier)")
            print("3. Flee the dungeon")
            choice = input("\nChoose one (1/2/3): ")
            if choice.lower() == '3':
                game_over = True
                break
            elif choice.lower() == '2':
                charge_modifier = 2.5
                break
            elif choice.lower() == '1':
                break
            else:
                continue

    score = xp + (20 * defeated_enemy_count)

    if defeated_enemy_count == 1:
        print("\nYou have defeated 1 enemy.")
        print(f"You have gained a total of {xp} XP.")
    elif defeated_enemy_count > 1:
        print(f"\nYou have defeated {defeated_enemy_count} enemies.")
        print(f"You have gained a total of {xp} XP.")
        print(f"Your final score is {score}.")
    while True:
        choice = input("\nStart a new game? (y/n): ")
        if choice.lower() == 'n':
            print("\nThanks for playing!\n")
            exit()
        elif choice.lower() == 'y':
            start_game()
        else:
            continue


start_game()