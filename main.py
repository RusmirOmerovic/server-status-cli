import json
import time
import ipaddress
import logging
# ----------------------------------------------------------------------
# KONSTANTEN / STARTDATEN
# Definiert die initialen Server sowie den Dateinamen für die Persistenz.

SERVERS = ["web1", "web2", "db1"]
FILENAME = "servers.json"

# Konfiguriert das Logging, um Informationen in eine Datei zu schreiben.
logging.basicConfig(
    filename="server_manager.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------------------------------------------------
# INITIALISIERUNG

# Erstellt das initiale Server-Dictionary mit den Standardattributen.
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


# ----------------------------------------------------------------------
# FACHLOGIK

# Fügt einen neuen Server mit IP, Betriebssystem und Rolle hinzu.
def add_server(server_dict, server_name, ip, os_name, role):
    if server_name in server_dict:
        print(f"[ERROR] {server_name} existiert bereits.")
        return False

    server_dict[server_name] = {
        "status": "offline",
        "ip": ip,
        "os": os_name,
        "role": role
    }

    logging.info(f"Server added: {server_name}")
    print(f"[OK] {server_name} hinzugefügt -> offline")
    return True


# Entfernt einen Server aus dem Server-Dictionary.
def remove_server(server_dict, server_name):
    if server_name not in server_dict:
        print(f"[ERROR] {server_name} existiert nicht.")
        return False

    del server_dict[server_name]

    logging.info(f"Server removed: {server_name}")
    print(f"[OK] {server_name} entfernt")
    return True


# Wechselt den Status eines Servers zwischen "online" und "offline".
def toggle_status(server_dict, server_name):
    if server_name not in server_dict:
        print(f"[ERROR] {server_name} existiert nicht")
        return False

    current_status = server_dict[server_name]["status"]
    new_status = "online" if current_status == "offline" else "offline"

    server_dict[server_name]["status"] = new_status

    logging.info(f"Status toggled: {server_name} -> {new_status}")
    print(f"[OK] {server_name} -> {new_status}")
    return True

# Ändert ein Attribut eines bestehenden Servers.
def edit_server(server_dict, server_name, field, value):
    if server_name not in server_dict:
        return False
    
    allowed_fields = ["ip", "os", "role"]

    if field not in allowed_fields:
        return False

    server_dict[server_name][field] = value
    
    logging.info(f"Server edited: {server_name} -> {field} changed to {value}")

    return True

# ----------------------------------------------------------------------
# VALIDIERUNG
# Prüft, ob eine gültige IPv4-Adresse eingegeben wurde.
def validate_ip(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False


# Prüft, ob eine Eingabe nicht leer ist.
def validate_non_empty(value: str) -> bool:
    return bool(value.strip())


# ----------------------------------------------------------------------
# PERSISTENZ
# Speichert den aktuellen Serverbestand als JSON-Datei.
def save_servers_to_json(server_dict: dict, filename: str):
    with open(filename, "w") as file:
        json.dump(server_dict, file, indent=4)


# Lädt den Serverbestand aus der JSON-Datei.
# Gibt None zurück, wenn die Datei fehlt oder ungültiges JSON enthält.
def load_servers_from_json(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return None


# ----------------------------------------------------------------------
# AUSGABE / CLI-HILFSFUNKTIONEN

# Zeigt das ASCII-Logo beim Programmstart an.
def print_banner() -> None:
    banner = r"""
   _____                          __  __
  / ____|                        |  \/  |
 | (___   ___ _ ____   _____ _ _| \  / | __ _ _ __   __ _  __ _  ___ _ __
  \___ \ / _ \ '__\ \ / / _ \ '__| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
  ____) |  __/ |   \ V /  __/ |  | |  | | (_| | | | | (_| | (_| |  __/ |
 |_____/ \___|_|    \_/ \___|_|  |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|
                                                              __/ |
                                                             |___/

              +--------------------------------------+
              |       SERVER STATUS MANAGER          |
              |     Python CLI | Server Inventory    |
              +--------------------------------------+
"""
    print(banner)

# Gibt alle Server und ihre Attribute tabellarisch aus.
def list_servers(server_dict):
    print()
    print(
        f"{'Hostname':<15} "
        f"{'Status':<10} "
        f"{'IP':<15} "
        f"{'OS':<10} "
        f"{'Role':<10}"
    )
    print("-" * 60)

    for server, data in server_dict.items():
        print(
            f"{server:<15} "
            f"{str(data['status']):<10} "
            f"{str(data['ip']):<15} "
            f"{str(data['os']):<10} "
            f"{str(data['role']):<10}"
        )

    print()


# Simuliert beim Programmstart einen kurzen Ladevorgang.
def loading_dots(duration: float) -> None:
    end_time = time.time() + duration

    print("Lädt Daten", end="", flush=True)

    while time.time() < end_time:
        print(".", end="", flush=True)
        time.sleep(1)

    print(" Fertig!")


# Zeigt alle verfügbaren CLI-Befehle an.
def print_help()-> None:
    print("""
Verfügbare Befehle:
  list
  toggle <server_name>
  add <server_name>
  remove <server_name>
  help
  exit
""")


# ----------------------------------------------------------------------
# MAIN / CLI

# Startet das Programm, lädt die Daten und verarbeitet Benutzereingaben.
def main() -> None:
    print_banner()
    print()
    print("Willkommen zum Server Status Manager!")

    loading_dots(1)

    status = load_servers_from_json(FILENAME)

    if status is None:
        status = init_servers(SERVERS)
        save_servers_to_json(status, FILENAME)
        print("Neue Serverliste erstellt.")
    else:
        print("Status aus Datei geladen.")

    print("-" * 60)
    print("Befehle mit 'help' anzeigen.")

    list_servers(status)

    # Hauptschleife für die CLI-Befehle.
    while True:
        user_input = input("> ").strip()

        if not user_input:
            continue

        # Zerlegt die Eingabe in Befehl und Argumente.
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

            server_name = parts[1]

            if toggle_status(status, server_name):
                save_servers_to_json(status, FILENAME)

        elif command == "add":
            if len(parts) != 2:
                print("[ERROR] Nutzung: add <server_name>")
                continue

            server_name = parts[1]

            if server_name in status:
                print(f"[ERROR] {server_name} existiert bereits.")
                continue

            ip = input("IP-Adresse: ").strip()

            if not validate_ip(ip):
                print("[ERROR] Ungültige IP4-Adresse.")
                continue

            os_name = input("Betriebssystem: ").strip()

            if not validate_non_empty(os_name):
                print("[ERROR] Betriebssystem darf nicht leer sein.")
                continue

            role = input("Rolle: ").strip()

            if not validate_non_empty(role):
                print("[ERROR] Rolle darf nicht leer sein.")
                continue

            if add_server(status, server_name, ip, os_name, role):
                save_servers_to_json(status, FILENAME)

        elif command == "edit":
            if len(parts) != 2:
                print("[ERROR] Nutzung: edit <server_name>")
                continue
            server_name = parts[1]

            if server_name not in status:
                print(f"[ERROR] {server_name} existiert nicht.")
                continue

            field = input("Zu änderndes Attribut (ip/os/role): ").strip().lower()
            value = input("Neuer Wert: ").strip()

            if field == "ip":
                if not validate_ip(value):
                    print("[ERROR] Ungültige IP4-Adresse.")
                    continue

            if field in {"os", "role"}:
                if not validate_non_empty(value):
                    print(f"[ERROR] {field} darf nicht leer sein.")
                    continue

            if edit_server(status, server_name, field, value):
                save_servers_to_json(status, FILENAME)
                print(f"[OK] {server_name} -> {field} geändert zu {value}")
            else:
                print(f"[ERROR] Ungültiges Attribut: {field}")

        elif command == "remove":
            if len(parts) != 2:
                print("[ERROR] Nutzung: remove <server_name>")
                continue

            server_name = parts[1]

            if remove_server(status, server_name):
                save_servers_to_json(status, FILENAME)

        elif command == "help":
            print_help()

        else:
            print("[ERROR] Unbekannter Befehl. Nutze 'help'.")


# Führt main() nur aus, wenn die Datei direkt gestartet wird.
if __name__ == "__main__":
    main()