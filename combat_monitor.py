"""
Combat Monitor - Real-time combat event viewer
Monitors the game log file and displays combat events in a readable format
"""
import time
import os
from pathlib import Path
from datetime import datetime


class CombatMonitor:
    """Monitor and display combat events from log file"""
    
    def __init__(self, log_file="logs/latest.log"):
        self.log_file = Path(log_file)
        self.last_position = 0
        self.combat_active = False
        
    def start(self):
        """Start monitoring the log file"""
        print("=" * 80)
        print("COMBAT MONITOR - Real-time Event Tracker")
        print("=" * 80)
        print(f"Monitoring: {self.log_file}")
        print("Waiting for combat events...")
        print("=" * 80)
        print()
        
        # Wait for log file to exist
        while not self.log_file.exists():
            time.sleep(0.5)
        
        # Get initial file size
        self.last_position = self.log_file.stat().st_size
        
        try:
            while True:
                self._check_for_new_lines()
                time.sleep(0.1)  # Check every 100ms
        except KeyboardInterrupt:
            print("\n" + "=" * 80)
            print("Combat Monitor stopped")
            print("=" * 80)
    
    def _check_for_new_lines(self):
        """Check log file for new lines"""
        current_size = self.log_file.stat().st_size
        
        if current_size > self.last_position:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = current_size
                
                for line in new_lines:
                    self._process_line(line.strip())
    
    def _process_line(self, line):
        """Process and display relevant combat log lines"""
        if not line:
            return
        
        # Combat turn events
        if "=== Turn" in line and "Started ===" in line:
            self.combat_active = True
            print("\n" + "━" * 80)
            self._print_highlight(line, "CYAN")
            print("━" * 80)
        
        # Phase transitions
        elif "Combat phase advanced to:" in line:
            phase = line.split(":")[-1].strip()
            self._print_info(f"⚡ PHASE: {phase}")
        
        # Weapon hits
        elif "HIT" in line and "for" in line and "damage" in line:
            self._print_success(f"💥 {self._extract_message(line)}")
        
        # Weapon misses
        elif "MISSED" in line:
            self._print_warning(f"❌ {self._extract_message(line)}")
        
        # Shield status
        elif "shields" in line.lower() and "reduced" in line.lower():
            self._print_info(f"🛡️  {self._extract_message(line)}")
        
        # Hull damage
        elif "hull" in line.lower() and "damage" in line.lower():
            self._print_error(f"🚨 {self._extract_message(line)}")
        
        # Ship destroyed
        elif "DESTROYED" in line:
            self._print_error(f"💀 {self._extract_message(line)}")
        
        # Errors
        elif "ERROR" in line or "Error" in line:
            self._print_error(f"⚠️  {self._extract_message(line)}")
    
    def _extract_message(self, line):
        """Extract the actual message from log line"""
        # Log format: timestamp - module - level - message
        parts = line.split(" - ", 3)
        if len(parts) >= 4:
            return parts[3]
        return line
    
    def _print_highlight(self, text, color="WHITE"):
        """Print highlighted text"""
        colors = {
            "RED": "\033[91m",
            "GREEN": "\033[92m",
            "YELLOW": "\033[93m",
            "BLUE": "\033[94m",
            "MAGENTA": "\033[95m",
            "CYAN": "\033[96m",
            "WHITE": "\033[97m",
            "RESET": "\033[0m"
        }
        print(f"{colors.get(color, '')}{text}{colors['RESET']}")
    
    def _print_success(self, text):
        """Print success message in green"""
        self._print_highlight(f"  ✓ {text}", "GREEN")
    
    def _print_error(self, text):
        """Print error message in red"""
        self._print_highlight(f"  ✗ {text}", "RED")
    
    def _print_warning(self, text):
        """Print warning message in yellow"""
        self._print_highlight(f"  ! {text}", "YELLOW")
    
    def _print_info(self, text):
        """Print info message in blue"""
        self._print_highlight(f"  ℹ {text}", "BLUE")


def main():
    """Run the combat monitor"""
    monitor = CombatMonitor()
    monitor.start()


if __name__ == "__main__":
    main()
