# ==============================================================================
# PROJEKT: Schere, Stein, Papier (Pro Edition)
# Kurs: Coding Humanities (Universität Tübingen) Rami Izzeddin
# Integration von Liste, Set, Tupel, RegEx & for-Schleife
# ==============================================================================

"""
ZUSAMMENFASSUNG:
Dieses Skript ist die Hauptsteuerung für das Spiel. Es integriert nun die
erweiterten Datenstrukturen (Liste, Set, Tupel) und reguläre Ausdrücke (RegEx),
um Eingaben strikt zu validieren und den Spielverlauf professionell zu protokollieren.
"""

import os
import random
import re  # Das Modul 're' (Regular Expressions) wird für die Namensprüfung benötigt.
import sys

# ------------------------------------------------------------------------------
# 1. TERMINAL-SCHUTZ & MODULE (Abhängigkeiten & System-Sicherheit)
# ------------------------------------------------------------------------------
try:
    import readchar
except ImportError:
    print("Fehler: Das Modul 'readchar' ist nicht installiert.")
    sys.exit(1)

if os.name != "nt":
    import termios

    fd = sys.stdin.fileno()
    original_termios = termios.tcgetattr(fd)
else:
    original_termios = None


def safe_exit(exit_code=0):
    """Beendet das Programm sicher und stellt das Terminal wieder her."""
    if os.name != "nt" and original_termios:
        import termios

        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, original_termios)
    sys.exit(exit_code)


# ------------------------------------------------------------------------------
# 2. DATENSTRUKTUREN: SETS & DICTIONARIES
# ------------------------------------------------------------------------------
REGELN = {"Schere": "Papier", "Stein": "Schere", "Papier": "Stein"}

P1_CHOICES = {"w": "Schere", "e": "Stein", "r": "Papier", "x": "exit"}
P2_CHOICES = {"1": "Schere", "2": "Stein", "3": "Papier", "x": "exit"}
COMPUTER_CHOICES = {1: "Schere", 2: "Stein", 3: "Papier"}

# DATENSTRUKTUR: SET
# WARUM: Ein 'Set' ist eine ungeordnete Sammlung eindeutiger Elemente. Es ist
# extrem schnell beim Suchen (O(1)-Komplexität).
# WIE: Wir nutzen Mengen (Sets), um alle erlaubten Tasten zusammenzufassen.
P1_ERLAUBTE_TASTEN = set(P1_CHOICES.keys())
P2_ERLAUBTE_TASTEN = set(P2_CHOICES.keys())


# ------------------------------------------------------------------------------
# 3. REGEX-VALIDIERUNG FÜR NAMENSLISTEN
# ------------------------------------------------------------------------------
def get_valid_name(prompt_text, default_name):
    r"""
    FUNKTION: get_valid_name
    WARUM: Wir wollen verhindern, dass Spieler ungültige Namen (wie Zahlen oder
           Sonderzeichen '!@#') eingeben. Dies entspricht dem Thema "RegEx Namensliste".
    WIE: Wir nutzen das Modul 're'. Der Ausdruck r"^[A-Za-zÄÖÜäöüß\s]+$" bedeutet:
         - ^ und $ : Überprüfe den gesamten String vom Anfang bis zum Ende.
         - [...] : Erlaube nur diese bestimmten Zeichen.
         - A-Za-z : Alle englischen Buchstaben.
         - ÄÖÜäöüß : Deutsche Umlaute (Das Fachwort: Diakritische Zeichen).
         - \s : Leerzeichen (falls jemand Vor- und Nachnamen eingibt).
         - + : Mindestens ein Zeichen muss vorhanden sein.
    VERBINDUNG: Wird im main()-Block aufgerufen, um die Spielernamen sicher zu erfassen.
    """
    while True:
        name = input(prompt_text).strip()

        # Wenn der Nutzer nur Enter drückt, wird der Standardname (Default) genommen.
        if not name:
            return default_name

        if name.lower() == "x":
            safe_exit(0)

        # RegEx-Überprüfung (Pattern Matching)
        if re.match(r"^[A-Za-zÄÖÜäöüß\s]+$", name):
            return name
        else:
            print(">> Ungültige Eingabe! Der Name darf nur aus Buchstaben bestehen.")


# ------------------------------------------------------------------------------
# 4. VERDECKTE EINGABEN (Single & Multiplayer)
# ------------------------------------------------------------------------------
def get_single_choice(player_name, choices_dict, erlaubte_tasten_set):
    tasten_hinweis = "/".join([k for k in choices_dict.keys() if k != "x"])
    print(
        f"\n{player_name}, wähle ({tasten_hinweis} | x = Abbruch): ", end="", flush=True
    )

    while True:
        taste = readchar.readkey().lower()

        # Wir prüfen zuerst im SET, ob die Taste existiert (Performance-Optimierung).
        if taste in erlaubte_tasten_set:
            wahl = choices_dict[taste]

            if wahl == "exit":
                print("\nDas Spiel wurde abgebrochen.")
                safe_exit(0)

            print(f"\n>> {player_name} hat verdeckt gewählt.")
            return wahl


def get_free_order_choices(p1_name, p2_name):
    print("\nBeide Spieler bereit machen!")
    print(f"{p1_name}: [w, e, r] | {p2_name}: [1, 2, 3] | x = Abbruch")
    print("Wartet auf Tastendruck beider Spieler... ", end="", flush=True)

    choice1 = None
    choice2 = None

    while choice1 is None or choice2 is None:
        taste = readchar.readkey().lower()

        if taste == "x":
            print("\nDas Spiel wurde vorzeitig abgebrochen.")
            safe_exit(0)

        # Nutzung des Sets für schnellere Validierung
        if choice1 is None and taste in P1_ERLAUBTE_TASTEN:
            choice1 = P1_CHOICES[taste]
            print(f"\n>> {p1_name} hat gewählt.")

        elif choice2 is None and taste in P2_ERLAUBTE_TASTEN:
            choice2 = P2_CHOICES[taste]
            print(f"\n>> {p2_name} hat gewählt.")

    print("-> Beide Wahlen sind registriert!")
    return choice1, choice2


# ------------------------------------------------------------------------------
# 5. RUNDEN-AUSWERTUNG
# ------------------------------------------------------------------------------
def evaluate_round(choice1, choice2):
    if choice1 == choice2:
        return "unentschieden"
    elif REGELN[choice1] == choice2:
        return "p1"
    else:
        return "p2"


# ------------------------------------------------------------------------------
# 6. HAUPTSCHLEIFE (Orchestrator mit Liste & Tupel & For-Schleife)
# ------------------------------------------------------------------------------
def main():
    print("==================================================")
    print("      SCHERE - STEIN - PAPIER (CODING HUMANITIES) ")
    print("==================================================")

    modus = ""
    while modus not in ["1", "2"]:
        modus = (
            input("\nWähle Modus (1: gegen Computer | 2: zwei Spieler): ")
            .strip()
            .lower()
        )
        if modus == "x":
            safe_exit(0)

    # Nutzung der RegEx-Funktion für die Namensvergabe
    p1_name = get_valid_name("\nName von Spieler 1 [Default: Ramistein]: ", "Ramistein")

    if modus == "1":
        p2_name = "Computer"
    else:
        p2_name = get_valid_name(
            "Name von Spieler 2 [Default: Spieler 2]: ", "Spieler 2"
        )

    ziel_siege = 0
    while True:
        ziel_eingabe = (
            input("\nWie viele Runden müssen gewonnen werden? ").strip().lower()
        )
        if ziel_eingabe == "x":
            safe_exit(0)

        if ziel_eingabe.isdecimal() and int(ziel_eingabe) > 0:
            ziel_siege = int(ziel_eingabe)
            break
        print("Bitte eine gültige positive Zahl eingeben.")

    p1_siege = 0
    p2_siege = 0
    unentschieden = 0
    runden_zaehler = 1

    # DATENSTRUKTUR: LISTE
    # WARUM: Eine Liste ist veränderbar (mutable) und geordnet. Wir nutzen sie
    # als Tagebuch (Log-Datei), um den gesamten Spielverlauf aufzuzeichnen.
    spiel_verlauf = []

    print(f"\nMatch gestartet: {p1_name} VS {p2_name} (Ziel: {ziel_siege} Siege)")

    try:
        while p1_siege < ziel_siege and p2_siege < ziel_siege:
            print(f"\n--- RUNDE {runden_zaehler} ---")

            if modus == "1":
                choice1 = get_single_choice(p1_name, P1_CHOICES, P1_ERLAUBTE_TASTEN)
                zufalls_zahl = random.randint(1, 3)
                choice2 = COMPUTER_CHOICES[zufalls_zahl]
                print(f">> {p2_name} hat verdeckt gezogen.")
            else:
                choice1, choice2 = get_free_order_choices(p1_name, p2_name)

            ergebnis = evaluate_round(choice1, choice2)
            print(f"\nAuswertung: {p1_name} ({choice1}) VS {p2_name} ({choice2})")

            if ergebnis == "unentschieden":
                unentschieden += 1
                runden_status = "Unentschieden"
                print(">> Ergebnis: Unentschieden!")
            elif ergebnis == "p1":
                p1_siege += 1
                runden_status = f"{p1_name} gewinnt"
                print(f">> Ergebnis: {p1_name} gewinnt diese Runde!")
            else:
                p2_siege += 1
                runden_status = f"{p2_name} gewinnt"
                print(f">> Ergebnis: {p2_name} gewinnt diese Runde!")

            # DATENSTRUKTUR: TUPEL
            # WARUM: Ein Tupel ist unveränderlich (immutable). Da das Ergebnis
            # einer gespielten Runde in der Vergangenheit liegt und nicht mehr
            # verfälscht werden darf, speichern wir es sicher als Tupel.
            # WIE: Wir hängen (append) das Tupel an unsere Liste an.
            runden_protokoll = (runden_zaehler, choice1, choice2, runden_status)
            spiel_verlauf.append(runden_protokoll)

            print(
                f"Gesamtstand (Siege-Niederlagen-Unentschieden): {p1_siege}-{p2_siege}-{unentschieden}"
            )
            runden_zaehler += 1

        gesamtsieger = p1_name if p1_siege == ziel_siege else p2_name

        # ----------------------------------------------------------------------
        # PROTOKOLL-AUSGABE MIT FOR-SCHLEIFE & RANGE
        # ----------------------------------------------------------------------
        print("\n==================================================")
        print("            SPIELPROTOKOLL (LOG)                  ")
        print("==================================================")

        # WARUM: "for-Schleife (for, range)"
        # WIE: Wir nutzen die for-Schleife, um durch unsere Liste zu iterieren.
        # Mit 'len(spiel_verlauf)' ermitteln wir die Anzahl der gespielten Runden
        # und nutzen 'range()', um einen Index (i) zu generieren.
        for i in range(len(spiel_verlauf)):
            # Das Tupel entpacken (Unpacking)
            runde, wahl1, wahl2, result = spiel_verlauf[i]
            print(
                f"Runde {runde:02d}: {p1_name} ({wahl1}) vs {p2_name} ({wahl2}) -> {result}"
            )

        print("\n==================================================")
        print(f"  MATCH ENDE! GESAMTSIEGER: {gesamtsieger}")
        print(f"  Endstand: {p1_siege}-{p2_siege}-{unentschieden}")
        print("==================================================")

    except KeyboardInterrupt:
        print("\n\n[System] Spiel durch Tastatur-Interrupt (Strg+C) abgebrochen!")
    finally:
        safe_exit(1)


if __name__ == "__main__":
    main()
