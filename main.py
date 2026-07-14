import json
import time



# erstelle Serverliste mit Statusen, ändere einen Status und gebe die Liste als Dictionary aus
servers = ["web1", "web2", "db1"]

# Datei definieren
FILENAME = "servers.json"

# Initialisierungsfunktion, die Server mit Attributen
# Status, IP, OS und role in verschachtelten Dictionary aufsetzt
def init_servers(servers):
    server_dict = {}
    for server in servers:
        server_dict[server] = {
            "status": "offline",
            "ip": None,
            "os": None,
            "role": None
        }
    return server_dict


# Erweitere um eine Funktion: Toggle-Status eines Servers, prüfen ob Server existiert, wenn ja 
# Status wechseln, 
# wenn nicht Fehlermeldung ausgeben.
# Toggle-Status ohne Parameter und automatischer Wechsel zwischen "online" und "offline", aktuellen 
# Status lesen, entscheiden, ausgeben.
# CLI Tool bauen, um den Status eines Servers zu toggeln, Servernamen als Argument übergeben, 
# Funktion aufrufen, Ergebnis ausgeben. while Schleife für CLI Tool, Eingabeaufforderung, 
# Möglichkeit zum Beenden.
# Beispiel: User gibt Servername ein -> es wird getoggelt -> aktueller Status wird ausgegeben; 
# bei exit wird beendet.
def toggle_status(server_dict, server_name):
    if server_name in server_dict:
        current_status = server_dict[server_name]["status"]
        new_status = "online" if current_status == "offline" else "offline"
        server_dict[server_name]["status"] = new_status
        print(f"[OK] {server_name} → {new_status}")
    else:
        print(f"[ERROR] {server_name} existiert nicht")

# Aktuellen Status aller Server ausgeben
def list_servers(server_dict):
    print("\nAktueller Status:")
    for server, data in server_dict.items():
        print(f"Hostname: {server}")
        print(f"  Status: {data['status']}")
        print(f"  IP: {data['ip']}")
        print(f"  OS: {data['os']}")
        print(f"  Role: {data['role']}")
        print()
    print()


# Erstelle eine Funktion, die die Serverliste als JSON-Datei speichert, und eine weitere Funktion, 
# die die JSON-Datei liest und die Serverliste wiederherstellt.
def save_servers_to_json(server_dict, filename):
    with open(filename, "w") as f:
        json.dump(server_dict, f, indent=4)

def load_servers_from_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Ladefunktion die zeitverzögert lädt, um den Ladeprozess zu simulieren, 
# z.B. durch eine kurze Pause oder durch das Anzeigen von Punkten.
def loading_dots(duration):
    end_time = time.time() + duration
    print("Lädt Daten", end="", flush=True)
    
    while time.time() < end_time:
        print(".", end="", flush=True)
        time.sleep(0.2)  # Geschwindigkeit der Punkte (alle 1 Sek ein Punkt)
    
    print(" Fertig!")

# Server hinzufügen
def add_server(server_dict, server_name):
    if server_name in server_dict:
        print(f"[ERROR] {server_name} existiert bereits.")
        return False

    server_dict[server_name] = "offline"
    print(f"[OK] {server_name} hinzugefügt -> offline")
    return True

# Server entfernen
def remove_server(server_dict, server_name):
    if server_name not in server_dict:
        print(f"[ERROR] {server_name} existiert nicht.")
        return False

    del server_dict[server_name]
    print(f"[OK] {server_name} entfernt")
    return True

# Einstiegspunkt für CLI Tool
def main():
    print("Willkommen zum Server Status Manager!")
    loading_dots(1)
    status = load_servers_from_json(FILENAME)

    if status is None:
        status = init_servers(servers)
        save_servers_to_json(status, FILENAME)
        print("Neue Serverliste erstellt.")
    else:
        print("Status aus Datei geladen.")
    
    list_servers(status)

#Nutzereingaben und Programmsteuerung
    while True:
        user_input = input("> ").strip()

        if not user_input:
            continue
        parts = user_input.split()
        command = parts[0].lower()

        if command == "exit":
            print("Beende das Programm.")
            break
        elif command == "list":
            list_servers(status)
        elif command == "toggle":
            if len(parts) != 2:
                print("[ERROR] Nutzung: toggle <server_name>")
                continue
        elif command == "add":
            if len(parts) != 2:
                print("[ERROR] Nutzung: add <server_name>")
                continue
            server_name = parts[1]
            if add_server(status, server_name):
                save_servers_to_json(status, FILENAME)
        elif command == "remove":
            if len(parts) != 2:
                print("[ERROR] Nutzung: remove <server_name>")
                continue
            server_name = parts[1]
            if remove_server(status, server_name):
                save_servers_to_json(status, FILENAME)
        elif command == "help":
            print("""
        Verfügbare Befehle:
        list
        toggle <server_name>
        add <server_name>
        remove <server_name>
        help
        exit
        """)
        else:
            print("[ERROR] Unbekannter Befehl. Nutze 'help'.")
        


if __name__ == "__main__":
    main()