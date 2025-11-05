# Combat Monitoring & Analysis Tools

Two tools to help you monitor and analyze combat in real-time.

## 1. Combat Monitor (Real-time)

**File:** `combat_monitor.py`

Monitors the game log file in real-time and displays combat events as they happen.

### Usage:

**Option A - Double-click the batch file:**
```
run_combat_monitor.bat
```

**Option B - Run from terminal:**
```powershell
python combat_monitor.py
```

### What it shows:
- ⚡ Phase transitions (MOVEMENT → TARGETING → FIRING)
- 💥 Weapon hits with damage numbers
- ❌ Weapon misses
- 🛡️ Shield status changes
- 🚨 Hull damage
- 💀 Ship destruction

### Usage Tips:
1. Start the monitor BEFORE launching the game
2. Keep the monitor window visible while playing
3. Watch combat events appear in real-time
4. Press Ctrl+C to stop monitoring

## 2. Combat Analyzer (Post-Combat)

**File:** `combat_analyzer.py`

Analyzes completed combat from the log file and generates detailed reports.

### Usage:

```powershell
python combat_analyzer.py
```

### What it shows:
- Turn-by-turn breakdown
- All hits and misses per turn
- Damage dealt per weapon
- Accuracy statistics (hits/total shots)
- Average damage per hit

### Example Output:
```
TURN 2
────────────────────────────────────
Phases: MOVEMENT → TARGETING → FIRING

✓ HITS (4):
  • Enterprise [phaser] → Target Drone: 70 dmg
  • Enterprise [phaser] → Target Drone: 70 dmg

📊 STATISTICS:
  • Accuracy: 100.0% (4/4)
  • Total Damage: 280
  • Avg Damage per Hit: 70.0
```

## Troubleshooting

**Monitor shows "Waiting for combat events..."**
- This is normal - start the game and begin combat
- The monitor is watching `logs/latest.log`

**Analyzer shows "No combat data found"**
- Make sure you've played at least one combat turn
- Check that `logs/latest.log` exists and has content

**Colors not showing in terminal:**
- Colors work in PowerShell and most terminals
- If colors don't work, the symbols still show the info

## Log File Location

Both tools monitor: `logs/latest.log`

This file is created automatically when the game starts and contains all combat events with timestamps.

---

*Created for debugging and balancing combat mechanics*
