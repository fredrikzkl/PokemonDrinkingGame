# Game Simulation Results (Final Version)

Simulated **50,000 games** with **4 players**. Social/physical mechanics (Haunter's no-laughing, Seafoam's no-floor-touching) are estimated conservatively.

## Key Numbers

| Metric | Value |
|--------|-------|
| Average rounds to finish | **~40** (10th-90th: 36-45) |
| Turns per player | **~35** |
| Tiles landed on per player | **~28** |
| Drinks per player (direct) | **~52 sips (~5.2 beers)** |
| Drinks per player (with collateral) | **~67 sips (~6.7 beers)** |
| Estimated game time | **1.3-2.0 hours** |
| Drink variance | 10th: 37 sips, median: 50, 90th: 69 sips |

## Drink Breakdown by Section

| Section | Tiles | Heaviest Tiles |
|---------|-------|---------------|
| Start -> Pewter Gym | 1-10 | Rattata (10) |
| Pewter -> Cerulean | 11-17 | Gary (2), Super Nerd (2), Poke Mart (2), Poke Center (2) |
| Cerulean -> Vermilion | 18-24 | SS Anne (7), Tentacool (3), Pokemon Stadium (2) |
| Vermilion -> Celadon | 25-38 | Celadon Gym (7), Diglett (5), Geodude (3), haunter (3) |
| Celadon -> Saffron | 39-47 | Gary (3), team_rocket (3), saffron_city (2), magneton (2) |
| Saffron -> Fuchsia | 48-53 | scyther (5), kangaskhan (3), Tauros (2) |
| Fuchsia -> Cinnabar | 54-60 | muk (5), articuno (3) |
| Cinnabar -> Viridian | 61-67 | electrode (5), zapdos (4), Gary (4), mr_mime (2) |
| Viridian -> End | 68-73 | champion_gary (10), gyarados (5), the_elite_four (3) |

## Heaviest Tiles (3+ avg drinks)

- **Rattata** (#2): ~10.0 drinks
- **Champion Gary** (#72): ~10.0 drinks
- **Celadon Gym** (#38): ~7.2 drinks
- **SS Anne** (#19): ~6.8 drinks
- **Diglett** (#29): ~5.0 drinks
- **scyther** (#51): ~5.0 drinks
- **muk** (#54): ~5.0 drinks
- **gyarados** (#69): ~5.0 drinks
- **electrode** (#63): ~4.7 drinks
- **zapdos** (#66): ~4.0 drinks
- **Gary** (#62): ~3.5 drinks
- **Geodude** (#28): ~3.4 drinks
- **Gary** (#40): ~3.4 drinks
- **The Elite Four** (#71): ~3.0 drinks
- **Tentacool** (#21): ~3.0 drinks

## Gym Battle Statistics

| Gym | Avg Drinks | Avg Rounds |
|-----|-----------|------------|
| Pewter Gym | 0.1 | 1.1 |
| Cerulean Gym | 0.2 | 1.3 |
| Vermilion Gym | 0.1 | 1.1 |
| Celadon Gym | 6.9 | 3.1 |
| Saffron Gym | 0.3 | 1.2 |
| Fuchsia Gym | 0.4 | 1.3 |
| Cinnabar Gym | 0.7 | 1.4 |
| Viridian Gym | 1.5 | 1.9 |
| The Elite Four | 3.1 | 1.9 |
| Champion Gary | 10.0 | 1.0 |

## Cinnabar Lab Upgrade Probability

| Step | Probability |
|------|------------|
| Player gets a Fossil (stops at Super Nerd) | **51.7%** |
| Player gets upgrade (Fossil + Cinnabar Lab) | **18.7%** |
| At least 1 of 4 players gets upgrade | **56.3%** |

## Board Summary

- **Total tiles:** 73
- **Gyms:** 11 (mandatory stops)
- **Zones:** rock_tunnel (6), silph_co (6), viridian_forest (5), pokemon_tower (5), safari_zone (5), seafoam_islands (4)
- **Avg game length:** ~40 rounds
- **Drink range:** 37-69 sips per player (80% of games)
