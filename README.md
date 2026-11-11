# Rock-Paper-Scissors CLI (Pro Edition)

An interactive Command-Line Interface (CLI) game developed in Python for the *Coding Humanities* course at Eberhard Karls Universität Tübingen. Demonstrates POSIX `termios` terminal state protection, unbuffered keypress capture via `readchar`, RegEx name validation, and structured game logging using sets, tuples, and lists.

## 🎮 Terminal Preview

```text
==================================================
      SCHERE - STEIN - PAPIER (CODING HUMANITIES) 
==================================================

Wähle Modus (1: gegen Computer | 2: zwei Spieler): 1
Name von Spieler 1 [Default: Ramistein]: Ramistein
Wie viele Runden müssen gewonnen werden? 3

Match gestartet: Ramistein VS Computer (Ziel: 3 Siege)

--- RUNDE 1 ---
Ramistein, wähle (w/e/r | x = Abbruch): 
>> Ramistein hat verdeckt gewählt.
>> Computer hat verdeckt gezogen.

Auswertung: Ramistein (Stein) VS Computer (Schere)
>> Ergebnis: Ramistein gewinnt diese Runde!
Gesamtstand (Siege-Niederlagen-Unentschieden): 1-0-0
