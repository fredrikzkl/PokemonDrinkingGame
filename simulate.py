"""
Monte Carlo simulation of the Poke Drinking Game board.
Pre-computes gym battle distributions, then simulates games.
"""

import random
import yaml
from collections import defaultdict

random.seed(42)

NUM_GAMES = 50_000
NUM_PLAYERS = 4
GYM_PRECOMPUTE = 10_000

with open("assets/tiles.yaml") as f:
    data = yaml.safe_load(f)

tile_defs = data["tiles"]
NUM_TILES = len(tile_defs)

GYMS = set()
OPTIONAL_STOPS = set()
ZONES = {}

for i, t in enumerate(tile_defs):
    bg = t.get("background_color", "")
    if bg == "gym":
        GYMS.add(i)
    if bg == "optional_stop":
        OPTIONAL_STOPS.add(i)
    if bg in ("viridian_forest", "rock_tunnel", "pokemon_tower", "silph_co", "safari_zone", "seafoam_islands"):
        ZONES[i] = bg


def gym_battle_once(atk, hp):
    """Single gym attempt. Returns (rounds, flashed)."""
    current_hp = hp
    rounds = 0
    while True:
        rounds += 1
        dice = sorted([random.randint(1, 6) for _ in range(3)], reverse=True)
        best_patk, best_pdef = 0, 0
        best_score = -1
        for a in range(4):
            patk = max(dice[:a]) if a > 0 else 0
            pdef = max(dice[a:]) if (3 - a) > 0 else 0
            if patk >= current_hp:
                score = 1000 + pdef
            else:
                score = pdef * 3 + patk
            if score > best_score:
                best_score = score
                best_patk, best_pdef = patk, pdef
        if best_patk >= current_hp:
            return rounds, True
        current_hp -= best_patk
        if current_hp < 0:
            current_hp = 0
        if atk > best_pdef:
            return rounds, False


def precompute_gym(name):
    """Pre-compute gym outcomes. Returns list of (drinks, rounds)."""
    results = []
    for _ in range(GYM_PRECOMPUTE):
        drinks = 0
        total_rounds = 0

        if "Pewter" in name:
            while True:
                r, flash = gym_battle_once(3, 4)
                total_rounds += r
                if flash:
                    break
                drinks += 2

        elif "Cerulean" in name:
            atk = 3
            while True:
                r, flash = gym_battle_once(atk, 5)
                total_rounds += r
                if flash:
                    break
                drinks += 2
                atk = 4  # +1 ATK if damaged

        elif "Vermilion" in name:
            while True:
                r, flash = gym_battle_once(4, 4)
                total_rounds += r
                if flash:
                    break
                drinks += 2

    elif "Celadon" in name:
        toxic_total = 0
        while True:
            r, flash = gym_battle_once(3, 7)
            for i in range(r):
                toxic_total += 1
                drinks += toxic_total
            total_rounds += r
            if flash:
                break
            drinks += 2
            toxic_total = 0  # faint resets toxicity

        elif "Fuchsia" in name:
            while True:
                r, flash = gym_battle_once(3, 5)
                total_rounds += r
                if flash:
                    break
                if r == 1:
                    drinks += 10
                else:
                    drinks += 3

        elif "Saffron" in name:
            while True:
                a, h = random.randint(1, 6), random.randint(1, 6)
                r, flash = gym_battle_once(a, h)
                total_rounds += r
                if flash:
                    break
                drinks += random.randint(1, 6)

        elif "Cinnabar" in name:
            while True:
                quiz = random.random() < 0.5
                ea = 0 if quiz else 5
                r, flash = gym_battle_once(ea, 5)
                total_rounds += r
                if flash:
                    break
                drinks += 4

        elif "Viridian Gym" in name:
            while True:
                a = random.randint(1, 6)
                r, flash = gym_battle_once(a, 6)
                total_rounds += r
                if flash:
                    break
                drinks += a

        elif "Elite" in name:
            hp = 10
            while True:
                total_rounds += 1
                dice = sorted([random.randint(1, 6) for _ in range(4)], reverse=True)
                patk = sum(dice[:2])
                pdef = max(dice[2:])
                if patk >= hp:
                    break
                hp -= patk
                if 4 > pdef:
                    drinks += 4
                    hp = 10

        elif "Champion" in name:
            drinks = 10
            total_rounds = 1

        results.append((drinks, total_rounds))
    return results


print("Pre-computing gym battles...")
gym_results = {}
for gi in GYMS:
    name = tile_defs[gi].get("header", f"Gym {gi}")
    gym_results[gi] = precompute_gym(name)
    avg_d = sum(d for d, _ in gym_results[gi]) / len(gym_results[gi])
    avg_r = sum(r for _, r in gym_results[gi]) / len(gym_results[gi])
    print(f"  {name}: avg {avg_d:.1f} drinks, {avg_r:.1f} rounds")


def sample_gym(tile_idx):
    return random.choice(gym_results[tile_idx])


def estimate_tile_drinks(tile_idx, player_state):
    t = tile_defs[tile_idx]
    name = t.get("name", "")
    text = t.get("text", "") or ""
    header = t.get("header", "") or ""

    if tile_idx in GYMS:
        d, r = sample_gym(tile_idx)
        return d, 0, r - 1, 0  # rounds - 1 = lost turns in gym

    drinks = 0
    extra_turns = 0
    lost_turns = 0
    move_back = 0
    low = name.lower()

    if low == "rattata":
        drinks = 10
    elif low == "pidgey":
        extra_turns = 1
    elif low == "weedle":
        drinks = 2
    elif low == "metapod":
        drinks = 2
    elif low == "super nerd":
        drinks = 2
        player_state["has_fossil"] = True
    elif low == "poke mart":
        drinks = 3
    elif "gary" in low:
        roll = random.randint(1, 6)
        drinks = (roll + 1) // 2 if "half" in text else roll
    elif "poke center" in header.lower():
        drinks = 2
    elif "ss anne" in header.lower():
        turns = (random.randint(1, 6) + 1) // 2
        drinks = turns * random.randint(1, 6)
        lost_turns = turns
    elif "stadium" in header.lower():
        drinks = 2
    elif low == "tentacool":
        drinks = 3
    elif low == "spearow":
        lost_turns = 1
    elif low == "zubat":
        drinks = 1
    elif low == "cubone":
        drinks = 1
    elif low == "geodude":
        drinks = random.randint(1, 6)
    elif low == "diglett":
        drinks = 5
    elif low == "machoke":
        roll = random.randint(1, 6)
        if roll <= 4:
            drinks = roll
            move_back = roll
    elif low == "channeler":
        drinks = 1
    elif low == "gastly":
        d = 0
        while random.randint(1, 6) % 2 == 0:
            d += 2
        drinks = d
    elif low == "haunter":
        drinks = 3
    elif low == "hypno":
        drinks = 2
    elif low == "snorlax":
        drinks = 2
    elif low == "mr_mime":
        drinks = 2
    elif "saffron city" in header.lower():
        drinks = 2
    elif low == "magneton":
        drinks = 2
    elif low == "porygon":
        drinks = 2
    elif "team_rocket" in low:
        drinks = 6 if player_state.get("met_rocket") else 3
        player_state["met_rocket"] = True
    elif low == "tauros":
        drinks = 2
    elif low == "scyther":
        drinks = 5
    elif low == "kangaskhan":
        drinks = 3
    elif low == "muk":
        drinks = 5
    elif low == "dewgong":
        drinks = 1
    elif low == "goldduck":
        rolls = 1
        while random.randint(1, 6) % 2 == 0:
            rolls += 1
        drinks = rolls if rolls > 1 else 0
    elif low == "articuno":
        lost_turns = 1
    elif "cinnabar lab" in header.lower() or low == "pokemon_lab":
        if player_state.get("has_fossil"):
            player_state["has_upgrade"] = True
    elif low == "electrode":
        roll = random.randint(1, 6)
        drinks = 10 if roll >= 5 else 2
        if roll >= 5:
            move_back = 1
    elif low == "golem":
        drinks = 2
        move_back = 2
    elif low == "zapdos":
        drinks = 3
    elif low == "dragonite":
        lost_turns = 1
    elif low == "gyarados":
        drinks = 5
    elif low == "moltres":
        pass

    return drinks, extra_turns, lost_turns, move_back


# Find forest boundaries
FOREST_START = None
FOREST_END = None
for i, td in enumerate(tile_defs):
    h = (td.get("header") or "").lower()
    if "viridian" in h or "virdian" in h:
        if FOREST_START is None:
            FOREST_START = i
    if td.get("background_color", "") == "viridian_forest":
        FOREST_END = i


def simulate_game():
    players = [{"pos": 0, "drinks": 0, "turns": 0, "tiles_landed": 0,
                "lost_turns": 0, "state": {}, "finished": False}
               for _ in range(NUM_PLAYERS)]

    total_rounds = 0
    while total_rounds < 200:
        total_rounds += 1
        all_done = True

        for p in players:
            if p["finished"]:
                continue
            all_done = False

            if p["lost_turns"] > 0:
                p["lost_turns"] -= 1
                p["turns"] += 1
                ti = p["pos"]
                t_text = (tile_defs[ti].get("text", "") or "").lower()
                if "start of turn" in t_text:
                    d, _, _, _ = estimate_tile_drinks(ti, p["state"])
                    p["drinks"] += d
                continue

            p["turns"] += 1
            roll = random.randint(1, 6)
            new_pos = p["pos"] + roll

            # Gym stops
            for gym_pos in sorted(GYMS):
                if p["pos"] < gym_pos <= new_pos:
                    if gym_pos not in p["state"].get("completed_gyms", set()):
                        new_pos = gym_pos
                        break

            # Optional stops (40% chance)
            for opt_pos in sorted(OPTIONAL_STOPS):
                if p["pos"] < opt_pos < new_pos:
                    if random.random() < 0.4:
                        new_pos = opt_pos
                        break

            # Forest loop
            if FOREST_START is not None and FOREST_END is not None:
                if FOREST_START <= new_pos <= FOREST_END and new_pos != p["pos"]:
                    if roll >= 5:
                        p["drinks"] += 1
                        new_pos = FOREST_START

            if new_pos >= NUM_TILES - 1:
                new_pos = NUM_TILES - 1
                p["finished"] = True

            p["pos"] = new_pos
            p["tiles_landed"] += 1

            d, extra, lost, back = estimate_tile_drinks(new_pos, p["state"])
            p["drinks"] += d
            p["lost_turns"] += lost

            if new_pos in GYMS:
                if "completed_gyms" not in p["state"]:
                    p["state"]["completed_gyms"] = set()
                p["state"]["completed_gyms"].add(new_pos)

            if back > 0:
                p["pos"] = max(0, p["pos"] - back)

            for _ in range(extra):
                p["turns"] += 1
                r2 = random.randint(1, 6)
                p["pos"] = min(p["pos"] + r2, NUM_TILES - 1)
                p["tiles_landed"] += 1
                d2, _, l2, b2 = estimate_tile_drinks(p["pos"], p["state"])
                p["drinks"] += d2
                p["lost_turns"] += l2

        if all_done:
            break

    return total_rounds, players


print(f"\nSimulating {NUM_GAMES:,} games...")
all_rounds = []
all_drinks = []
all_turns = []
all_tiles = []
fossils = 0
upgrades = 0
games_with_upgrade = 0

for g in range(NUM_GAMES):
    if g % 10000 == 0 and g > 0:
        print(f"  {g:,}...")
    rounds, players = simulate_game()
    all_rounds.append(rounds)
    gu = False
    for p in players:
        all_drinks.append(p["drinks"])
        all_turns.append(p["turns"])
        all_tiles.append(p["tiles_landed"])
        if p["state"].get("has_fossil"):
            fossils += 1
        if p["state"].get("has_upgrade"):
            upgrades += 1
            gu = True
    if gu:
        games_with_upgrade += 1

total_players = NUM_GAMES * NUM_PLAYERS
avg_rounds = sum(all_rounds) / len(all_rounds)
avg_drinks = sum(all_drinks) / len(all_drinks)
avg_turns = sum(all_turns) / len(all_turns)
avg_tiles = sum(all_tiles) / len(all_tiles)

sorted_drinks = sorted(all_drinks)
sorted_rounds = sorted(all_rounds)
p10_d = sorted_drinks[int(len(sorted_drinks) * 0.1)]
p50_d = sorted_drinks[int(len(sorted_drinks) * 0.5)]
p90_d = sorted_drinks[int(len(sorted_drinks) * 0.9)]
p10_r = sorted_rounds[int(len(sorted_rounds) * 0.1)]
p90_r = sorted_rounds[int(len(sorted_rounds) * 0.9)]

fossil_pct = fossils / total_players * 100
upgrade_pct = upgrades / total_players * 100
game_upgrade_pct = games_with_upgrade / NUM_GAMES * 100

collateral = avg_drinks * 1.3
est_min = avg_rounds * 2
est_max = avg_rounds * 3

# Heaviest tiles
heavy_tiles = []
for i in range(NUM_TILES):
    d_sum = 0
    n = 1000
    for _ in range(n):
        d, _, _, _ = estimate_tile_drinks(i, {})
        d_sum += d
    avg = d_sum / n
    if avg >= 2:
        heavy_tiles.append((tile_defs[i].get("name", ""), tile_defs[i].get("header", ""), i + 1, avg))
heavy_tiles.sort(key=lambda x: -x[3])

# Section breakdown
sections = [
    ("Start -> Pewter Gym", 0, 9),
    ("Pewter -> Cerulean", 10, 16),
    ("Cerulean -> Vermilion", 17, 23),
    ("Vermilion -> Celadon", 24, 38),
    ("Celadon -> Saffron", 39, 48),
    ("Saffron -> Fuchsia", 49, 54),
    ("Fuchsia -> Cinnabar", 55, 61),
    ("Cinnabar -> Viridian", 62, 66),
    ("Viridian -> End", 67, NUM_TILES - 1),
]

with open("rules/simulation.md", "w") as f:
    f.write("# Game Simulation Results\n\n")
    f.write(f"Simulated **{NUM_GAMES:,} games** with **{NUM_PLAYERS} players**. ")
    f.write("Social/physical mechanics (Haunter's no-laughing, Seafoam's no-floor-touching) are estimated conservatively.\n\n")

    f.write("## Key Numbers\n\n")
    f.write("| Metric | Value |\n")
    f.write("|--------|-------|\n")
    f.write(f"| Average rounds to finish | **~{avg_rounds:.0f}** (10th-90th percentile: {p10_r}-{p90_r}) |\n")
    f.write(f"| Turns per player | **~{avg_turns:.0f}** |\n")
    f.write(f"| Tiles landed on per player | **~{avg_tiles:.0f}** |\n")
    f.write(f"| Drinks per player (direct) | **~{avg_drinks:.0f} sips (~{avg_drinks/10:.1f} beers)** |\n")
    f.write(f"| Drinks per player (with collateral) | **~{collateral:.0f} sips (~{collateral/10:.1f} beers)** |\n")
    f.write(f"| Estimated game time | **{est_min/60:.1f}-{est_max/60:.1f} hours** |\n")
    f.write(f"| Drink variance | 10th: {p10_d} sips, median: {p50_d}, 90th: {p90_d} sips |\n")
    f.write("\n")

    f.write("## Drink Breakdown by Section\n\n")
    f.write("| Section | Tiles | Heaviest Tiles |\n")
    f.write("|---------|-------|---------------|\n")
    for sec_name, start, end in sections:
        sec_heavy = [(n or h, d) for n, h, pos, d in heavy_tiles if start < pos <= end + 1]
        sec_heavy.sort(key=lambda x: -x[1])
        heavy_str = ", ".join(f"{n} ({d:.0f})" for n, d in sec_heavy[:4]) if sec_heavy else "-"
        f.write(f"| {sec_name} | {start+1}-{end+1} | {heavy_str} |\n")
    f.write("\n")

    f.write("## Heaviest Tiles (3+ avg drinks)\n\n")
    for name, header, pos, d in heavy_tiles[:15]:
        label = header if header else name
        f.write(f"- **{label}** (#{pos}): ~{d:.1f} drinks\n")
    f.write("\n")

    f.write("## Gym Battle Statistics\n\n")
    f.write("| Gym | Avg Drinks | Avg Rounds |\n")
    f.write("|-----|-----------|------------|\n")
    for gi in sorted(GYMS):
        res = gym_results[gi]
        ad = sum(d for d, _ in res) / len(res)
        ar = sum(r for _, r in res) / len(res)
        f.write(f"| {tile_defs[gi].get('header', '')} | {ad:.1f} | {ar:.1f} |\n")
    f.write("\n")

    f.write("## Cinnabar Lab Upgrade Probability\n\n")
    f.write("| Step | Probability |\n")
    f.write("|------|------------|\n")
    f.write(f"| Player gets a Fossil (lands on Super Nerd) | **{fossil_pct:.1f}%** |\n")
    f.write(f"| Player gets upgrade (Fossil + Cinnabar Lab) | **{upgrade_pct:.1f}%** |\n")
    f.write(f"| At least 1 of {NUM_PLAYERS} players gets upgrade | **{game_upgrade_pct:.1f}%** |\n")
    f.write("\n")

    f.write("## Board Summary\n\n")
    f.write(f"- **Total tiles:** {NUM_TILES}\n")
    f.write(f"- **Gyms:** {len(GYMS)} (mandatory stops)\n")
    f.write(f"- **Optional stops:** {len(OPTIONAL_STOPS)}\n")
    zone_counts = defaultdict(int)
    for z in ZONES.values():
        zone_counts[z] += 1
    f.write(f"- **Zones:** {', '.join(f'{z} ({c})' for z, c in sorted(zone_counts.items(), key=lambda x: -x[1]))}\n")
    f.write(f"- **Avg game length:** ~{avg_rounds:.0f} rounds\n")

print(f"\nDone! Results written to rules/simulation.md")
print(f"  Rounds: {avg_rounds:.1f} avg ({p10_r}-{p90_r})")
print(f"  Drinks/player: {avg_drinks:.1f} sips ({avg_drinks/10:.1f} beers)")
print(f"  Turns/player: {avg_turns:.1f}")
print(f"  Fossil: {fossil_pct:.1f}%, Upgrade: {upgrade_pct:.1f}%, Game w/ upgrade: {game_upgrade_pct:.1f}%")
