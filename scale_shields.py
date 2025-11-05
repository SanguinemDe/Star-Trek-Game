import re

# Read the file
with open('game/ships/federation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all shield definitions
pattern = r"ship\.shields = \{'fore': (\d+), 'aft': (\d+), 'port': (\d+), 'starboard': (\d+)\}"
matches = re.findall(pattern, content)

# Calculate new values (multiply by 2.67, round to nearest 5)
print('Shield scaling by 2.67x:')
print('=' * 60)

replacements = []
for i, (fore, aft, port, starboard) in enumerate(matches):
    fore_old, aft_old, port_old, star_old = int(fore), int(aft), int(port), int(starboard)
    fore_new = round(fore_old * 2.67 / 5) * 5
    aft_new = round(aft_old * 2.67 / 5) * 5
    port_new = round(port_old * 2.67 / 5) * 5
    star_new = round(star_old * 2.67 / 5) * 5
    
    old_str = f"{{'fore': {fore_old}, 'aft': {aft_old}, 'port': {port_old}, 'starboard': {star_old}}}"
    new_str = f"{{'fore': {fore_new}, 'aft': {aft_new}, 'port': {port_new}, 'starboard': {star_new}}}"
    
    replacements.append((old_str, new_str))
    
    print(f'{i+1}. {fore_old}/{aft_old}/{port_old}/{star_old} -> {fore_new}/{aft_new}/{port_new}/{star_new}')

# Apply replacements
for old, new in replacements:
    content = content.replace(f"ship.shields = {old}", f"ship.shields = {new}", 1)

# Write back
with open('game/ships/federation.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('\nDone! All shields scaled by 2.67x')
