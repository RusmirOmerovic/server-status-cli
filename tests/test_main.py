from main import add_server, edit_server

# Prüft, ob ein vorhandener Server doppelt hinzugefügt wird.
def test_add_server_rejects_duplicate():
    servers = {
        "web1": {
            "status": "offline",
            "ip": "192.168.1.10",
            "os": "Linux",
            "role": "Webserver"
        }
    }

    result = add_server(
        servers,
        "web1",
        "192.168.1.20",
        "Linux",
        "Webserver"
    )

    assert result is False
    assert servers["web1"]["ip"] == "192.168.1.10" # Vorhandenen Server nicht überschreiben.


# Prüft, ob ein neuer Server erfolgreich hinzugefügt wird.
def test_add_server_success():
    servers = {}

    result = add_server(
        servers,
        "web1",
        "192.168.1.10",
        "Linux",
        "Webserver"
    )

    assert result is True
    assert "web1" in servers


# Prüft, ob die IP eines vorhandenen Servers erfolgreich geändert wird.
def test_edit_server_updates_ip():
    servers = {
        "web1": {
            "status": "offline",
            "ip": None,
            "os": None,
            "role": None
        }
    }

    result = edit_server(
        servers,
        "web1",
        "ip",
        "192.168.1.10"
    )

    assert result is True
    assert servers["web1"]["ip"] == "192.168.1.10"


# Prüft, ob die Funktion bei einem unbekannten Server False zurückgibt.
def test_edit_server_unknown_server_returns_false():
    servers = {
        "web1": {
            "status": "offline",
            "ip": None,
            "os": None,
            "role": None
        }
    }

    result = edit_server(
        servers,
        "web99",
        "ip",
        "192.168.1.10"
    )

    assert result is False


# Prüft, ob ein ungültiges Attribut nicht angelegt oder geändert wird.
def test_edit_server_rejects_invalid_field():
    servers = {
        "web1": {
            "status": "offline",
            "ip": None,
            "os": None,
            "role": None
        }
    }

    result = edit_server(
        servers,
        "web1",
        "location",
        "serverraum"
    )

    assert result is False
    assert "location" not in servers["web1"]