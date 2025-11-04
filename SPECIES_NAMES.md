# Federation Species Name Lists

This document details the expanded name lists for all Federation species in the crew recruitment system.

## Overview

All 10 Federation species now have comprehensive, lore-accurate name lists with appropriate cultural flavor:

| Species    | First Names | Last Names | Total Combinations |
|------------|-------------|------------|--------------------|
| Human      | 142         | 102        | 14,484             |
| Vulcan     | 98          | 27         | 2,646              |
| Andorian   | 90          | 54         | 4,860              |
| Tellarite  | 88          | 54         | 4,752              |
| Betazoid   | 103         | 56         | 5,768              |
| Trill      | 96          | 56         | 5,376              |
| Bajoran    | 96          | 57         | 5,472              |
| Caitian    | 84          | 49         | 4,116              |
| Klingon    | 94          | 40         | 3,760              |
| Bolian     | 72          | 40         | 2,880              |
| **TOTAL**  | **963**     | **535**    | **54,114**         |

## Species Naming Conventions

### Human
- **Style**: Diverse, contemporary Earth names reflecting global cultures
- **Examples**: James Kirk, Kathryn Janeway, Sarah Chen, Marcus Rodriguez
- **Notes**: Mix of traditional Western names with representation from various Earth cultures

### Vulcan
- **Style**: Logical, precise names; often start with S, T, V, or K
- **Male Names**: Spock, Sarek, Tuvok, Soval, Stonn
- **Female Names**: T'Pol, T'Pau, Saavik (note: female names often use T' prefix)
- **Last Names**: Often include "of [place]" (e.g., "of Vulcan", "of ShiKahr", "of Gol")
- **Cultural Note**: Vulcans value brevity and meaning in names

### Andorian
- **Style**: Complex names with gender prefixes in surnames
- **Gender Prefixes**:
  - `th'` = thaan (male)
  - `ch'` = chaan (male)
  - `sh'` = shen (female)
  - `zh'` = zhen (female)
- **First Names**: Shran, Thy'lek, Talas, Thelev (often contain Th, Sh, Kh sounds)
- **Examples**: Shran th'Thane, Talas sh'Raav
- **Cultural Note**: Andorians have four genders, reflected in naming

### Tellarite
- **Style**: Gruff, consonant-heavy names reflecting their argumentative culture
- **Common Sounds**: Gr, Br, Kr, Dr, Sk combinations
- **Male Names**: Gral, Brok, Krog, Skalaar (harsh, strong)
- **Female Names**: Gora, Brava, Krana (slightly softer but still gruff)
- **Examples**: Gral Thag, Brava Krov
- **Cultural Note**: Names sound as blunt as their personalities

### Betazoid
- **Style**: Elegant, flowing names reflecting telepathic grace
- **Male Names**: Often end in -n, -s, -l (Lon, Aras, Varel)
- **Female Names**: Often end in -a, -na, -ra (Deanna, Lwaxana, Elara)
- **Examples**: Deanna Troi, Lwaxana Troi, Lon Suder
- **Cultural Note**: Names have a melodic, sophisticated quality

### Trill
- **Style**: Varied, often two-syllable names
- **Joined vs Unjoined**: Same naming pattern (symbiont name replaces surname if joined)
- **Male Names**: Curzon, Torias, Joran, Vered
- **Female Names**: Jadzia, Ezri, Lenara, Audrid
- **Last Names**: Short, often ending in -x, -n (Dax, Kahn, Ral, Pahl)
- **Examples**: Jadzia Dax, Ezri Tigan, Curzon (before joining)

### Bajoran
- **Style**: Spiritual, elegant names with unique name order
- **Name Order**: Family name FIRST, given name second (Bajoran custom)
  - Example: "Kira Nerys" = family Kira, given name Nerys
  - Properly addressed by family name: "Major Kira"
- **Male Names**: Bareil, Shakaar, Vedek, Tahna
- **Female Names**: Nerys, Kira, Leeta, Opaka
- **Examples**: Kira Nerys, Ro Laren, Bareil Antos
- **Cultural Note**: Names often reflect religious/spiritual heritage

### Caitian
- **Style**: Feline-inspired with frequent apostrophes
- **Common Prefixes**: M', R', S', T', K', L'
- **Male Names**: M'Raaw, R'Mor, S'Byrl (strong, sharp)
- **Female Names**: M'Ress, S'Ressa, T'Mara (graceful, melodic)
- **Examples**: M'Ress, R'Mor S'Taal
- **Cultural Note**: Names evoke their felinoid heritage

### Klingon
- **Style**: Harsh, warrior-like with strong consonants
- **Common Sounds**: K, G, M, Q (aggressive, forceful)
- **Male Names**: Worf, Martok, Gowron, Kang
- **Female Names**: K'Ehleyr, B'Elanna, Grilka (strong but slightly softer)
- **House Names**: "of House [name]" for noble families
- **Examples**: Worf of House Mogh, Martok of House Martok
- **Cultural Note**: Names reflect warrior culture and honor

### Bolian
- **Style**: Melodic, often with B, M, R, L sounds
- **Male Names**: Mot, Boq'ta, Rixx, Brex
- **Female Names**: Lysia, Bolka, Mitra, Riala
- **Examples**: Mot, Lysia Brex, Rixx Borath
- **Cultural Note**: Names have a pleasant, approachable quality

## Implementation Notes

### Name Generation
- Each officer randomly selects from their species' first and last name pools
- Some species (Vulcan, Klingon) may have empty last names, generating single names
- Bajoran names maintain proper family-first order
- All names are lore-appropriate and Star Trek canon-inspired

### Cultural Authenticity
- Names were chosen/created to match established Star Trek naming patterns
- Gender-specific names included where culturally appropriate
- Historical/canonical character names included as homages
- New names created following phonetic and cultural patterns

### Diversity
- Over 54,000 unique name combinations possible
- No name list has fewer than 72 entries
- Ensures minimal repetition in crew recruitment pools
- Players will rarely see duplicate names

## Testing

To test name generation:
```bash
python test_names.py
```

This will display:
- Name count statistics for all species
- Sample names (5 per species)
- Sample bridge crew roster

## Future Enhancements

Potential additions:
- Romulan names (if Romulan faction added)
- Cardassian names (if Cardassian faction added)
- Ferengi names (if Ferengi become playable)
- Name suffixes/titles (e.g., Vulcan "Master", Klingon "son of")
- Patronymic/matronymic names for certain species
- Noble titles for Klingon houses

---

**Total Name Diversity: 963 first names + 535 last names = 54,114+ unique combinations across all Federation species!**
