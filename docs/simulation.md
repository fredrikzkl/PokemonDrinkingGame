# Game Simulation Results (Final Version)

Simulated **50,000 games** with **4 players**. Social/physical mechanics (Haunter's no-laughing, Seafoam's no-floor-touching) are estimated conservatively.

## Key Numbers

| Metric | Value |
|--------|-------|
| Average rounds to finish | **~39** (10th-90th: 35-43) |
| Turns per player | **~34** |
| Tiles landed on per player | **~27** |
| Drinks per player (direct) | **~51 sips (~5.1 beers)** |
| Drinks per player (with collateral) | **~66 sips (~6.6 beers)** |
| Estimated game time | **1.3-1.9 hours** |
| Drink variance | 10th: 36 sips, median: 49, 90th: 67 sips |

## Drink Breakdown by Section

| Section | Tiles | Heaviest Tiles |
|---------|-------|---------------|
| Start -> Pewter Gym | 1-10 | Rattata (10) |
| Pewter -> Cerulean | 11-17 | Super Nerd (2), Poke Mart (2), Poke Center (2) |
| Cerulean -> Vermilion | 18-24 | SS Anne (7), Tentacool (3), Pokemon Stadium (2) |
| Vermilion -> Celadon | 25-39 | Celadon Gym (7), Diglett (5), Geodude (4), Gary (3) |
| Celadon -> Saffron | 40-49 | Gary (4), team_rocket (3), mr_mime (2), saffron_city_mall (2) |
| Saffron -> Fuchsia | 50-55 | scyther (5), kangaskhan (3), Tauros (2) |
| Fuchsia -> Cinnabar | 56-62 | muk (5) |
| Cinnabar -> Viridian | 63-67 | electrode (5), zapdos (4), golem (2) |
| Viridian -> End | 68-73 | champion_gary (10), gyarados (5), the_elite_four (3) |

## Heaviest Tiles (3+ avg drinks)

- **Rattata** (#2): ~10.0 drinks
- **Champion Gary** (#72): ~10.0 drinks
- **SS Anne** (#19): ~7.2 drinks
- **Celadon Gym** (#39): ~7.0 drinks
- **Diglett** (#29): ~5.0 drinks
- **scyther** (#53): ~5.0 drinks
- **muk** (#56): ~5.0 drinks
- **gyarados** (#69): ~5.0 drinks
- **electrode** (#63): ~4.7 drinks
- **zapdos** (#66): ~4.0 drinks
- **Geodude** (#28): ~3.6 drinks
- **Gary** (#42): ~3.5 drinks
- **Gary** (#37): ~3.4 drinks
- **Tentacool** (#22): ~3.0 drinks
- **haunter** (#35): ~3.0 drinks

## Gym Battle Statistics

| Gym | Avg Drinks | Avg Rounds |
|-----|-----------|------------|
| Pewter Gym | 0.1 | 1.1 |
| Cerulean Gym | 0.1 | 1.3 |
| Vermilion Gym | 0.3 | 1.1 |
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
| At least 1 of 4 players gets upgrade | **56.4%** |

## Board Summary

- **Total tiles:** 73
- **Gyms:** 11 (mandatory stops)
- **Zones:** rock_tunnel (6), silph_co (6), viridian_forest (5), pokemon_tower (5), safari_zone (5), seafoam_islands (4)
- **Avg game length:** ~39 rounds
- **Drink range:** 36-67 sips per player (80% of games)
