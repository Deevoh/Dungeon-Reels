import random
import os
import time
from art import logo
from tables import symbols, player, level_up_stats
from enemylist import enemies, bosses

# Earn XP
def earn_experience(enemy_xp):
    global xp, player_level, escaped_combat
    xp += round(enemy_xp / 2) if escaped_combat else enemy_xp
    while (player_level + 1) in level_up_stats and xp >= level_up_stats[player_level + 1]['experience']:
        level_up()
# Process level up
def level_up():
    global player_level, player_health, player_max_health, player_attack_power, player_defense, player_max_ap, player_ap
    if (player_level + 1) in level_up_stats:
        requirements = level_up_stats[player_level + 1]
        player_level += 1
        player_health = requirements['health']
        player_max_health = requirements['health']
        player_attack_power += requirements['attack_power']
        player_defense += requirements['defense']
        player_max_ap += 30
        player_ap = min(player_ap, player_max_ap)
        print(f"You have gained enough experience points to reach level {player_level}!\nYour attributes have increased and you've regained health!")
# Select an enemy
def select_enemy():
    return random.choice(enemies)
# Select a boss
def select_boss():
    return random.choice(bosses)
# Randomize and spin the reels
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
# Process spins and reels
def process_spin(result):  # sourcery skip: low-code-quality, use-fstring-for-concatenation
    global charge_modifier, score, player_max_ap, player_ap, enemy_max_health, xp, defeated_enemy_count
    for row in result:
        print("   ".join(row))
        time.sleep(0.3)
    # Match init
    escape_matches = 0
    armor_matches = 0
    heart_matches = 0
    skill_matches = 0
    critical_matches = 0
    sword_matches = 0
    enemy_critical_attacks = 0
    enemy_attacks = 0
    # Match conditions
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
    # Additional printouts
    print("━═━═━═━═━═━═")
    time.sleep(0.5)
    if charge_modifier > 1:
        print("\n◇ Charge active!")
    if defeated_enemy_count % 10 == 0 and defeated_enemy_count > 1:
        print("\n◆ Boss battle")
    # Count all the matches
    if escape_matches > 0:
        score += (escape_matches * 25) + 25
    if armor_matches > 0:
        score += (armor_matches * 10) + 15
    if heart_matches > 0:
        score += (heart_matches * 25) + 25
    if skill_matches > 0:
        score += (skill_matches * 25) + 25
    if critical_matches > 0:
        score += (critical_matches * 25) + 25
    if sword_matches > 0:
        score += (sword_matches * 10) + 15
    if enemy_critical_attacks > 0:
        score += (enemy_critical_attacks * 25) + 25
    if enemy_attacks > 0:
        score += (enemy_attacks * 10) + 15
    # Process roll matches
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
    # Post spin AP recharge and charge check
    if charge_modifier == 1:
        player_ap += 15
        player_ap = min(player_ap, player_max_ap)
    charge_modifier = 1
    # Player status printout
    if player_armor > 0:
        player_status = f"{player_name}'s HP: {max(player_health, 0)}/{player_max_health} ({player_armor} Armor)"
    else:
        player_status = f"{player_name}'s HP: {max(player_health, 0)}/{player_max_health}"
    player_ap_status = f"AP: {max(player_ap, 0)}/{player_max_ap}"
    player_xp_status = f"Level {player_level} ({xp}/{level_up_stats[player_level + 1]['experience']} XP)"
    enemy_status = f"{enemy_name}'s HP: {max(enemy_health, 0)}/{enemy_max_health}"
    dungeon_rooms = f"Rooms explored: {defeated_enemy_count}" #TODO Change this to room_count?
    status_length = max(len(player_status), len(player_ap_status), len(player_xp_status), len(enemy_status))
    print("\n╔" + "═" * status_length + "╗")
    print("║" + player_status.center(status_length) + "║")
    print("║" + player_ap_status.center(status_length) + "║")
    print("║" + player_xp_status.center(status_length) + "║")
    print("║" + " " * status_length + "║")
    print("║" + enemy_status.center(status_length) + "║")
    print("╚" + "═" * status_length + "╝")
    print(" " + dungeon_rooms.center(status_length))
# Escape
def escape_combat():
    global escaped_combat
    print(f"\n{player_name} triggers an escape by matching 3 🏃 symbols in a column.")
    print(f"{player_name} successfully runs from the {enemy_name.lower()}.")
    escaped_combat = True
# Armor buff
def add_armor(armor_matches):
    global player_armor, charge_modifier
    armor_points = 5
    if player_level > 1:
        total_armor_points = round(armor_points * armor_matches * charge_modifier * (player_level * 0.6))
    else:
        total_armor_points = round(armor_points * armor_matches * charge_modifier)
    player_armor += total_armor_points
    if armor_matches == 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols in a column.")
    elif armor_matches > 1:
        print(f"\n{player_name} gains {total_armor_points} armor from matching 2 🛡️  symbols {armor_matches} times in a column.")
# Health buff
def add_health(heart_matches):
    global player_health, charge_modifier
    health_bonus = 20
    if player_level > 1:
        total_health_bonus = round(health_bonus * heart_matches * charge_modifier * (player_level * 0.58))
    else:
        total_health_bonus = round(health_bonus * heart_matches * charge_modifier)
    player_health += total_health_bonus
    player_health = min(player_health, player_max_health)
    if heart_matches == 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols in a row.")
    elif heart_matches > 1:
        print(f"\n{player_name} gains {total_health_bonus} health from matching 3 ❤️  symbols {heart_matches} times in a row.")
# Player skill attack
def skill_check():
    global player_attack_power, enemy_health, charge_modifier, defeated_enemy
    skill_modifier = 1.85 * charge_modifier
    total_attack_power = round(player_attack_power * skill_modifier)
    print(f"\n{player_name} unleashes a powerful skill attack from matching 3 ➕ symbols in a row.")
    print(f"{player_name} deals {total_attack_power} damage to the {enemy_name.lower()}, bypassing their defenses.")
    enemy_health -= total_attack_power
    if enemy_health <= 0:
        defeated_enemy = True
# Player critical hit
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
# Player attack
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
# Enemy critical hit
def enemy_attack_player_crit(enemy_critical_attacks):
    global enemy_attack_power, player_health, player_armor, player_defense, charge_modifier
    damage = max(enemy_attack_power - player_defense, 0)
    total_damage = round(damage * enemy_critical_attacks * charge_modifier * 1.38)
    print(f"\nThe {enemy_name.lower()} initiates a critical attack from matching 3 💀 symbols in a row.")
    if player_armor > 0:
        armor_reduction = min(player_armor, total_damage)
        player_armor -= armor_reduction
        total_damage -= armor_reduction
        if enemy_critical_attacks == 1:
            print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage after armor absorption.")
        elif enemy_critical_attacks > 1:
            print(f"The {enemy_name.lower()} attacks {player_name} {enemy_critical_attacks} times and deals {total_damage} damage after armor absorption.")
        print(f"{player_name}'s armor absorbed {armor_reduction} damage.")
    elif enemy_critical_attacks == 1:
        print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage.")
    elif enemy_critical_attacks > 1:
        print(f"The {enemy_name.lower()} attacks {player_name} {enemy_critical_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage
# Enemy attack
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
        print(f"{player_name}'s armor absorbed {armor_reduction} damage.")
    elif enemy_attacks == 1:
        print(f"The {enemy_name.lower()} attacks {player_name} and deals {total_damage} damage.")
    elif enemy_attacks > 1:
        print(f"The {enemy_name.lower()} attacks {player_name} {enemy_attacks} times and deals {total_damage} damage.")
    player_health -= total_damage

#! Program init
def start_game():  # sourcery skip: extract-method, low-code-quality
    global player_name, enemy, enemy_name, enemy_max_health, enemy_health, enemy_attack_power, enemy_defense, enemy_xp, player_max_health, player_health, player_attack_power, player_defense, player_armor, player_level, player_max_ap, player_ap, xp, defeated_enemy_count, defeated_enemy, charge_modifier, score, escaped_combat
    enemy = select_enemy()
    enemy_name = enemy['name']
    enemy_max_health = enemy['health']
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
    player_max_ap = player['ap']
    player_ap = player['ap']
    xp = player["xp"]
    defeated_enemy_count = 0
    defeated_enemy = False
    charge_modifier = 1
    score = 0
    escaped_combat = False
    boss_count = 0
    game_over = False
    early_flee = False
    player_died = False
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
            print("Every 10 rooms explored will result in a boss fight.")
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
        # Game over and combat resolutions
        if escaped_combat:
            if defeated_enemy_count % 10 == 0 and defeated_enemy_count > 1:
                boss_count += 1
            defeated_enemy_count += 1
            print(f"\nYou have gained {round(enemy_xp / 2)} XP.")
            earn_experience(enemy_xp)
            # Post escape new round input loop
            while not game_over:
                choice = input("\nKeep exploring the dungeon? (y/n): ")
                if choice.lower() == 'n':
                    game_over = True
                    break
                elif choice.lower() == 'y':
                    escaped_combat = False
                    break
                else:
                    continue
            # New round setup and boss check
            enemy = select_enemy() if defeated_enemy_count % 10 != 0 else select_boss()
            enemy_name = enemy['name']
            if player_level > 1:
                enemy_max_health = round(enemy['health'] * (player_level * 0.58))
                enemy_health = round(enemy['health'] * (player_level * 0.58))
                enemy_attack_power = round(enemy['attack_power'] * (player_level * 0.58))
                enemy_defense = round(enemy['defense'] * (player_level * 0.55))
                enemy_xp = round(enemy['xp'] * (player_level * 0.52))
            else:
                enemy_max_health = enemy['health']
                enemy_health = enemy['health']
                enemy_attack_power = enemy['attack_power']
                enemy_defense = enemy['defense']
                enemy_xp = enemy['xp']
            continue
        elif player_health <= 0:
            game_over = True
            player_died = True
            print(f"\nGame Over! {player_name} was killed by the {enemy_name.lower()}.")
            break
        elif enemy_health <= 0:
            if defeated_enemy_count % 10 == 0 and defeated_enemy_count > 1:
                boss_count += 1
            defeated_enemy_count += 1
            print(f"\nCongratulations! You've defeated the {enemy_name.lower()} and gained {enemy_xp} XP!")
            earn_experience(enemy_xp)
            # New round input loop
            while not game_over:
                choice = input("\nKeep exploring the dungeon? (y/n): ")
                if choice.lower() == 'n':
                    game_over = True
                    break
                elif choice.lower() == 'y':
                    break
                else:
                    continue
            # New round setup and boss check
            defeated_enemy = False
            enemy = select_enemy() if defeated_enemy_count % 10 != 0 else select_boss()
            enemy_name = enemy['name']
            if player_level > 1:
                enemy_max_health = round(enemy['health'] * (player_level * 0.58))
                enemy_health = round(enemy['health'] * (player_level * 0.58))
                enemy_attack_power = round(enemy['attack_power'] * (player_level * 0.56))
                enemy_defense = round(enemy['defense'] * (player_level * 0.55))
                enemy_xp = round(enemy['xp'] * (player_level * 0.52))
            else:
                enemy_max_health = enemy['health']
                enemy_health = enemy['health']
                enemy_attack_power = enemy['attack_power']
                enemy_defense = enemy['defense']
                enemy_xp = enemy['xp']
            continue
        # Main action loop
        while not game_over:
            print("\n1. Attack")
            print("2. Charge - 10 AP (2.5x modifier)")
            print("3. Flee the dungeon (Penalty to final score)")
            choice = input("\nChoose (1/2/3): ")
            if choice.lower() == '3':
                game_over = True
                early_flee = True
                break
            elif choice.lower() == '2' and player_ap < 10:
                print("\nInsufficient ability points.")
                continue
            elif choice.lower() == '2' and player_ap >= 10:
                player_ap -= 10
                charge_modifier = 2.5
                break
            elif choice.lower() == '1':
                break
            else:
                continue
    # Final scoring
    if defeated_enemy_count >= 1:
        score += round((xp + (55 * defeated_enemy_count)))
        score += round((player_level * 300))
    if boss_count >= 1:
        score += round(boss_count * 400)
    if early_flee == True:
        score = score / 1.4
    if player_died == True:
        score = score / 2
    score = round(score)
    # End game printout
    if defeated_enemy_count == 1:
        print("\nYou have defeated 1 enemy.")
    else:
        print(f"\nYou have defeated {defeated_enemy_count} enemies.")
    if boss_count == 1:
        print("You have defeated 1 boss.")
    else:
        print(f"You have defeated {boss_count} bosses.")
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

#! Program start
start_game()