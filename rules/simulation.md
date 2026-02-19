# Game Simulation Results

Simulated 100,000 games with 4 players. Social/physical mechanics (e.g. Haunter's no-laughing, Seafoam's no-floor-touching) are estimated conservatively since they depend on player behavior.

## Key Numbers

| Metric | Value |
|--------|-------|
| Average rounds to finish | **~25** (range: 18-36) |
| Turns per player | **~29** |
| Tiles landed on per player | **~27** |
| Drinks per player (direct) | **~63 sips (~6.3 beers)** |
| Drinks per player (with collateral) | **~83 sips (~8.3 beers)** |
| Estimated game time | **2-3 hours** |

## Drink Breakdown by Section

These are estimated drinks **per player** from tiles they land on. "Collateral" (drinks caused by other players' tiles) adds ~20 sips on top.

| Section | Tiles | Heaviest Tiles | Est. Drinks |
|---------|-------|---------------|-------------|
| Start → Pewter Gym | 0-9 | Rattata (10!), Weedle (2), Metapod (2), Forest loops (1 each) | 3-12 |
| Pewter → Cerulean | 10-16 | Gary 1 (2), Super Nerd (2) | 2-4 |
| Cerulean → Vermilion | 17-23 | SS Anne (7!), Tentacool (3) | 3-10 |
| Vermilion → Celadon | 24-38 | Geodude (3.5), Diglett (5), Haunter (4-6), Gary 2 (3.5) | 8-15 |
| Celadon → Saffron | 39-48 | Gary 3 (3.5), Team Rocket (3-6), Celadon Gym toxic (5+) | 5-12 |
| Saffron → Fuchsia | 49-54 | Scyther (5), Kangaskhan (2-3) | 3-7 |
| Fuchsia → Cinnabar | 55-61 | Muk (8!), Cinnabar Gym (4) | 4-12 |
| Cinnabar → Viridian | 62-66 | Gyarados (5), Zapdos (3), Viridian Gym (4) | 5-10 |
| Viridian → End | 67-72 | Elite Four (4), Champion Gary (10!) | 14-20 |

**Drink spikes:** Rattata (finish drink early), SS Anne (cascading lost turns), Muk (combined drinks), and Champion Gary (fill + finish) are the biggest single-tile drink events.

## Cinnabar Lab Upgrade Probability

To get a permanent upgrade, a player needs:

1. **Land on Super Nerd** (tile 11, between Pewter and Cerulean Gym) to get a Fossil
2. **Land on Cinnabar Lab** (tile 60, between Fuchsia and Cinnabar Gym) to trade it

| Step | Probability |
|------|------------|
| Land on Super Nerd (from Pewter Gym) | **19.3%** |
| Land on Cinnabar Lab (from Fuchsia Gym) | **36.2%** |
| Both (per player) | **7.0%** |
| At least 1 of 4 players gets upgrade | **25.1%** |

The upgrade is quite rare. Only ~1 in 14 players will get one. Consider one of:
- Moving Super Nerd closer to the center of its gym gap (currently reachable only by rolling exactly 2 from Pewter Gym)
- Adding a second fossil source elsewhere on the board
- Having the fossil available as a Poke Mart purchase

## Viridian Forest Loop Analysis

The zone rule ("roll 5 or 6 = drink 1 and return to entrance") creates a significant early-game trap:

- **Expected turns to escape:** ~4.8 turns (vs ~1.5 without the rule)
- **Expected loop-backs:** ~1.6 times
- **Expected drinks from looping alone:** ~1.6 sips

This is fine mechanically, but see the rules clarity issue below about gym stop priority.

## Rules That Need Clarification

### High Priority

1. **Trainer battles (Rule 4):** "Challenge them to a trainer battle" -- but PvP battle mechanics are never defined. How do two players fight? Same 3-dice split as gyms? What does the loser drink? This also applies to **Pokemon Stadium**.

2. **Confusion status:** Defined in `tiles.yaml` ("roll 4/5/6 = drink 2 and lose turn") but **not mentioned anywhere in rules.md**. Gastly inflicts it -- players won't know what it means without reading the YAML.

3. **Champion Gary:** "Fill up your drink. Finish it." -- No gym battle mechanics. Is this literally just "chug a full beer"? This seems like it should be a climactic boss fight, not just a chug.

4. **Viridian Forest vs Gym stop priority:** If you're on tile 8 (Beedrill, last forest tile) and roll 5, do you stop at Pewter Gym (tile 9, Rule 5) or return to forest entrance (zone rule)? Gym stops and zone rules conflict here.

5. **Gym dice split -- 0 defense allowed?** Can a player go 3 ATK / 0 DEF? If so, they auto-faint whenever they don't one-shot. Should be explicitly stated.

### Medium Priority

6. **Haunter:** "Smile or laugh until your next turn, you drink 6" -- Grammatically ambiguous. Should probably read: "**If** you smile or laugh before your next turn, drink 6."

7. **Diglett / Electrode / Team Rocket -- "At the start of your turn":** These are one-time effects when you land, or persistent while on the tile? Important distinction, especially for Electrode where Golem/Zapdos can send you.

8. **Muk:** "Have every player combine their drinks in a glass, and finish the drink!" -- Who finishes? Everyone? Just the landing player? And literally mix all drinks together?

9. **Rock Tunnel zone:** "If you finish your drink... fill it up and return here." Fill with what? Another beer? This could mean unlimited refills.

10. **Scyther:** "Drink half your drink, and move that many sips ahead." Move by the number of sips taken? If drink is 80% full, that's 4 sips = 4 squares? Needs explicit wording.

11. **Seafoam Islands:** "May not touch the floor." Physical rule that's fun, but for how long? Until leaving the zone? What if you're sent back here?

### Low Priority

12. **Golem:** "Every player must drink 2 and move 2 squares back" -- Does this include the landing player? (Probably yes, but worth clarifying.)

13. **SS Anne:** Can potentially lock a player for 3 turns drinking 5-6 each turn (~15-18 sips). Very swingy for a mid-game tile. May be intentional, but worth noting.

14. **Lapras:** "All players ahead of you" -- What if nobody is ahead?

15. **Rattata:** "You seriously rolled a 1?" -- Flavor text implies this only happens on a roll of 1, but mechanically it's just the tile effect for anyone who lands there. The text could confuse players.

## Game Balance Observations

- **Early game is front-loaded with punishment:** Rattata (finish drink on tile 1!) is brutal for whoever rolls a 1 first. The Viridian Forest loop adds ~3 extra turns per player.
- **Mid-game slog (Vermilion → Celadon):** The longest gym gap (15 tiles) combined with Rock Tunnel and Pokemon Tower zones makes this the most drink-heavy section.
- **Late game escalates well:** Elite Four + Champion Gary being back-to-back mandatory stops with heavy drinks is a strong finish.
- **Muk is the wildcard:** "Combine all drinks and finish" could be the heaviest single-tile event in the entire game depending on interpretation.
- **Game length is reasonable:** 2-3 hours with 4 players is solid for a drinking board game. Adding more players would increase time significantly due to collateral effects and trainer battles.
