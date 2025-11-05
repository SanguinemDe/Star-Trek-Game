"""
Combat Analysis Script
Analyzes combat log and generates detailed reports
"""
import re
from pathlib import Path
from collections import defaultdict


class CombatAnalyzer:
    """Analyze combat events from log file"""
    
    def __init__(self, log_file="logs/latest.log"):
        self.log_file = Path(log_file)
        self.turns = []
        self.current_turn = None
        
    def analyze(self):
        """Analyze the entire combat log"""
        if not self.log_file.exists():
            print(f"Error: Log file not found: {self.log_file}")
            return
        
        print("=" * 80)
        print("COMBAT ANALYSIS REPORT")
        print("=" * 80)
        print()
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Parse combat events
        for line in lines:
            self._parse_line(line.strip())
        
        # Generate report
        self._generate_report()
    
    def _parse_line(self, line):
        """Parse a single log line"""
        if not line:
            return
        
        # Extract message from log format
        parts = line.split(" - ", 3)
        if len(parts) < 4:
            return
        
        timestamp, module, level, message = parts
        
        # Turn start
        if "=== Turn" in message and "Started ===" in message:
            turn_match = re.search(r'Turn (\d+)', message)
            if turn_match:
                turn_num = int(turn_match.group(1))
                self.current_turn = {
                    'number': turn_num,
                    'phases': [],
                    'hits': [],
                    'misses': [],
                    'damage': [],
                    'events': []
                }
                self.turns.append(self.current_turn)
        
        # Phase transitions
        elif "Combat phase advanced to:" in message and self.current_turn:
            phase = message.split(":")[-1].strip()
            self.current_turn['phases'].append(phase)
        
        # Weapon hits
        elif "HIT" in message and "for" in message and "damage" in message and self.current_turn:
            # Extract: "Enterprise phaser HIT Target Drone for 85 damage"
            match = re.search(r'(\w+.*?) (\w+) HIT (.*?) for (\d+) damage', message)
            if match:
                attacker, weapon, target, damage = match.groups()
                self.current_turn['hits'].append({
                    'attacker': attacker,
                    'weapon': weapon,
                    'target': target,
                    'damage': int(damage)
                })
        
        # Weapon misses
        elif "MISSED" in message and self.current_turn:
            # Extract: "Enterprise phaser MISSED Target Drone"
            match = re.search(r'(\w+.*?) (\w+) MISSED (.*?)$', message)
            if match:
                attacker, weapon, target = match.groups()
                self.current_turn['misses'].append({
                    'attacker': attacker,
                    'weapon': weapon,
                    'target': target
                })
    
    def _generate_report(self):
        """Generate human-readable combat report"""
        if not self.turns:
            print("No combat data found in log file.")
            return
        
        print(f"Total Turns Analyzed: {len(self.turns)}")
        print()
        
        for turn in self.turns:
            self._print_turn_report(turn)
    
    def _print_turn_report(self, turn):
        """Print report for a single turn"""
        print("─" * 80)
        print(f"TURN {turn['number']}")
        print("─" * 80)
        
        # Phases
        if turn['phases']:
            print(f"Phases: {' → '.join(turn['phases'])}")
        
        # Hits
        if turn['hits']:
            print(f"\n✓ HITS ({len(turn['hits'])}):")
            for hit in turn['hits']:
                print(f"  • {hit['attacker']} [{hit['weapon']}] → {hit['target']}: {hit['damage']} dmg")
        
        # Misses
        if turn['misses']:
            print(f"\n✗ MISSES ({len(turn['misses'])}):")
            for miss in turn['misses']:
                print(f"  • {miss['attacker']} [{miss['weapon']}] → {miss['target']}")
        
        # Statistics
        total_hits = len(turn['hits'])
        total_shots = total_hits + len(turn['misses'])
        total_damage = sum(hit['damage'] for hit in turn['hits'])
        
        if total_shots > 0:
            accuracy = (total_hits / total_shots) * 100
            print(f"\n📊 STATISTICS:")
            print(f"  • Accuracy: {accuracy:.1f}% ({total_hits}/{total_shots})")
            print(f"  • Total Damage: {total_damage}")
            if total_hits > 0:
                print(f"  • Avg Damage per Hit: {total_damage / total_hits:.1f}")
        
        print()


def main():
    """Run combat analysis"""
    analyzer = CombatAnalyzer()
    analyzer.analyze()
    
    print("=" * 80)
    print("Analysis complete. Press Enter to exit...")
    input()


if __name__ == "__main__":
    main()
