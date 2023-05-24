import random
import os
import time
from art import logo


symbols = {
    'armor': '🛡️ ',
    'sword': '🗡️ ',
    'heart': '❤️ ',
    'skill': '➕',
    'escape': '🏃',
    'enemy': '💀'
}

enemies = [
    {
        'name': 'Goblin',
        'health': 40,
        'attack_power': 15,
        'defense': 2,
        'xp': 12
    },
    {
        'name': 'Skeleton',
        'health': 50,
        'attack_power': 13,
        'defense': 3,
        'xp': 20
    },
    {
        'name': 'Orc',
        'health': 60,
        'attack_power': 20,
        'defense': 5,
        'xp': 30
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

def process_spin(result):  # sourcery skip: use-fstring-for-concatenation
    global charge_modifier, xp
    for row in result:
        print("   ".join(row))
        time.sleep(0.3)

    armor_matches = 0
    sword_matches = 0
    heart_matches = 0
    enemy_attacks = 0
    skill_matches = 0
    escape_matches = 0

    for col in range(len(result[0])):
        column_symbols = [result[row][col] for row in range(len(result))]
        if column_symbols.count('❤️ ') == 3:
            heart_matches += 1
        if column_symbols.count('🛡️ ') >= 2:
            armor_matches += 1
        if column_symbols.count('🏃') == 3:
            escape_matches += 1
    for row in result:
        if row.count('❤️ ') == 3:
            heart_matches += 1
        if row.count('➕') == 3:
            skill_matches += 1
        if row.count('🗡️ ') >= 2:
            sword_matches += 1
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
    if sword_matches > 0 and escape_matches == 0 and skill_matches == 0:
        attack_enemy(sword_matches)
    if enemy_attacks > 0 and escape_matches == 0:
        enemy_attack_player(enemy_attacks)
    charge_modifier = 1

    if player_armor > 0:
        player_status = f"{player_name}'s Health(Armor): {player_health}({player_armor})"
    else:
        player_status = f"{player_name}'s Health: {player_health}"
    player_xp_status = f"{xp} XP"
    enemy_status = f"{enemy_name}'s Health: {enemy_health}"
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
    print(f"{player_name} successfully dodges and runs from {enemy_name}.")
    enemy_health = 0

def add_armor(armor_matches):
    global player_armor, charge_modifier
    armor_points = 6
    total_armor_points = armor_points * armor_matches * charge_modifier
    player_armor += total_armor_points
    if armor_matches == 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols in a column.")
    elif armor_matches > 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols {armor_matches} times in a column.")

def add_health(heart_matches):
    global player_health, charge_modifier
    health_bonus = 20
    total_health_bonus = health_bonus * heart_matches * charge_modifier
    player_health += total_health_bonus
    if heart_matches == 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols in a row.")
    elif heart_matches > 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols {heart_matches} times in a row.")

def skill_check():
    global player_attack_power, enemy_health, charge_modifier
    skill_modifier = 1.85 * charge_modifier
    total_attack_power = int(player_attack_power * skill_modifier)
    print(f"\n{player_name} unleashes a powerful skill attack from matching 3 ➕ symbols in a row.")
    print(f"{player_name} deals {total_attack_power} damage to {enemy_name}, bypassing their defense.")
    enemy_health -= total_attack_power

def attack_enemy(sword_matches):
    global player_attack_power, enemy_health, enemy_defense, charge_modifier
    damage = max(player_attack_power - enemy_defense, 0)
    total_damage = damage * sword_matches * charge_modifier
    enemy_health -= total_damage
    print(f"\n{player_name} initiates an attack from matching 2 🗡️  symbols in a row.")
    if sword_matches == 1:
        print(f"{player_name} attacks {enemy_name} and deals {total_damage} damage.")
    elif sword_matches > 1:
        print(f"{player_name} attacks {enemy_name} {sword_matches} times and deals {total_damage} damage.")

def enemy_attack_player(enemy_attacks):
    global player_health, player_armor, player_defense, charge_modifier
    damage = max(enemy_attack_power - player_defense, 0)
    total_damage = damage * enemy_attacks * charge_modifier
    print(f"\n{enemy_name} initiates an attack from matching 2 💀 symbols in a row.")
    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        if enemy_attacks == 1:
            print(f"{enemy_name} attacks {player_name} and deals {total_damage} damage after armor absorption.")
        elif enemy_attacks > 1:
            print(f"{enemy_name} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage after armor absorption.")
        print(f"Your armor absorbed {armor_reduction} damage.")
    elif enemy_attacks == 1:
        print(f"{enemy_name} attacks {player_name} and deals {total_damage} damage.")
    elif enemy_attacks > 1:
        print(f"{enemy_name} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

#! Program init
def start_game():  # sourcery skip: extract-method, low-code-quality
    global player_name, enemy, enemy_name, enemy_health, enemy_attack_power, enemy_defense, player_health, player_attack_power, player_defense, player_armor, xp, defeated_enemy_count, charge_modifier
    enemy = select_enemy()
    enemy_name = enemy['name']
    enemy_health = enemy['health']
    enemy_attack_power = enemy['attack_power']
    enemy_defense = enemy['defense']
    player_health = 300
    player_attack_power = 14
    player_defense = 6
    player_armor = 0
    xp = 0
    defeated_enemy_count = 0
    charge_modifier = 1
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
            print("➕: 3 in a row for a SKILLED ATTACK")
            print("💀: 2 in a row for an ENEMY ATTACK")
            print("🛡️ : 2 in a column to buff ARMOR")
            print("❤️ : 3 in a row or column to buff HEALTH")
            print("🏃: 3 in a column to ESCAPE")
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
            print(f"\nGame Over! {player_name} was killed by {enemy_name}.")
            break
        elif enemy_health <= 0:
            defeated_enemy_count += 1
            xp += enemy['xp']
            print(f"\nCongratulations! You've defeated {enemy_name}!")
            while not game_over:
                choice = input("\nKeep exploring the dungeon? (y/n): ") #TODO Add in the option to 2x, maybe see enemy beforehand?
                if choice.lower() == 'n':
                    game_over = True
                    break
                elif choice.lower() == 'y':
                    break
                else:
                    continue
            enemy = select_enemy()
            enemy_name = enemy['name']
            enemy_health = enemy['health']
            enemy_attack_power = enemy['attack_power']
            enemy_defense = enemy['defense']
            continue
        while not game_over:
            print("\n1. Attack")
            print("2. Charge (2x modifier)")
            print("3. Flee the Dungeon")
            choice = input("\nChoose one (1/2/3): ")
            if choice.lower() == '3':
                game_over = True
                break
            elif choice.lower() == '2':
                charge_modifier = 2
                break
            elif choice.lower() == '1':
                break
            else:
                continue

    if defeated_enemy_count == 1:
        print("\nYou have defeated 1 enemy.")
    elif defeated_enemy_count > 1:
        print(f"\nYou have defeated {defeated_enemy_count} enemies.")
        print(f"You have gained a total of {xp} XP.")
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