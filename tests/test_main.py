from main import edit_server


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