# Ideas

Parking lot for tiles and mechanics that aren't on the board yet. Moved out of
`assets/tiles.yaml` so the tile file stays readable.

## Tile drafts

Ready to paste into `assets/tiles.yaml` — drop the leading `#` comments and place
them in the right zone.

### Scientist

```yaml
- name: scientist
  text: "You meet a Scientist, and he lets you use his device.\nRoll a die.\nOptional: Move that many squares, but also drink that many"
  background_color: "silph_co"
```

### MissingNo

Note: place this 4 squares before the last tile of Rock Tunnel, so that rolling
e.g. a 5 sends you 5 squares backwards.

```yaml
- name: MissingNo
  text: "A wild Missingno!\nThe game is glitching! Next turn, move backwards instead of forward"
  poke_api_image: "pokemon/missingno" # Does not exist in PokeAPI — needs a local image
```

### Weedle — belongs in Viridian Forest

```yaml
- name: Weedle
  text: |
    Weedle used Poison Sting!
    Drink 2. Next time someone passes you, they must stop at whatever square you're on
  poke_api_image: "pokemon/weedle"
  background_color: "viridian_forest"
```

### Electabuzz

```yaml
- name: electabuzz
  text: "Electabuzz used Thunder Punch!\nYou're paralyzed; miss your next turn"
  poke_api_image: pokemon/electabuzz
```

### Ditto

```yaml
- name: ditto
  text: "Ditto used Transform!\nSelect a move from any Pokemon you've passed. You must decide within 60 seconds, or Ditto flees"
  poke_api_image: "pokemon/ditto"
```

### Koffing / Weezing (Team Rocket staple)

```yaml
- name: koffing
  text: |
    Koffing used Smokescreen!
    All players close their eyes. You may move someone's piece 1-2 squares in secret.
  poke_api_image: "pokemon/koffing"
```

### Hitmonlee

A physical challenge — the board only has Tentacool and Lickitung in this vein,
and this one gets funnier the longer the game runs. Hitmonlee lives in the
Fighting Dojo in Saffron City, if placement should follow the games.

```yaml
- name: hitmonlee
  text: "Hitmonlee used High Jump Kick!\nStand on one leg until your next turn. Put your foot down, drink 3"
  poke_api_image: "pokemon/hitmonlee"
```

### Charizard

```yaml
- name: charizard
  text: |
    Charziard used Fly!
    Move 8 squares ahead. Every player you passed gets scorched, and must drink 6

  poke_api_image: "pokemon/charizard"
```

### Alakazam — used, kept for reference

The guess-the-die mechanic below now lives on the **Hypno** tile as Hypnosis, and
Alakazam is already the Saffron Gym boss. Kept here only so the idea isn't
rediscovered as new.

```yaml
- name: Alakazam
  text: "Alakazam used Psychic! Player to your left rolls a die. If you correctly guess the number on the die, new turn. Otherwise, drink 4"
  poke_api_image: "pokemon/alakazam"
  image_scale: 0.85
```

## Mechanic ideas

### Stomp

Stun all players one square away in all axes, 1 round.

Because the board is an inward spiral (see `assets/layout.txt`), "one square in
all axes" also reaches into neighbouring lanes — and those neighbours can be
20-30 squares apart in turn order. Tile 20 touches 47, tile 63 touches 42, tile
05 touches 36.

Open questions: is the player who landed on it affected? Do diagonals count?
Consider drinks plus a 1-square knockback instead of a stun, so nobody sits out.

### Wild grass

Have 5-6 "Tall grass" tiles on the board where you meet a random Pokemon,
including Pokemon that aren't on the board. Needs a clever way to seamlessly
roll for and display a random Pokemon.

Options considered:

- **Per-tile d6 encounter table** — each grass tile prints its own six Pokemon,
  themed to where it sits on the board (like route encounter tables in the real
  games). No new components; use `font_size` to fit the extra lines. Costs
  ~36 new one-liner effects to write.
- **Encounter deck** — draw the top card of a Wild Pokemon pile. Only option
  that gives many Pokemon *with* art, and catching becomes physical (keep the
  card). Requires printing and cutting cards.
- **QR code to a web roller** — a static page using the existing PokeAPI
  plumbing in `src/api/pokeapi.py`. Fully random across all 151, but puts phones
  on the table and needs a connection.

Grass tiles would also give the **Pokeball** and **Repel** items a lot more to
do, since both only matter when encounters happen.
