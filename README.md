# Server Status Manager

A lightweight Python CLI application for managing a small persistent server inventory.

The project was built as a hands-on Python and DevOps learning project with a focus on clean business logic, input validation, persistence, testing, logging, and maintainable code structure.

## Features

- List all managed servers in a readable table
- Add servers with hostname, IPv4 address, operating system, and role
- Edit existing server metadata
- Toggle server status between `online` and `offline`
- Remove servers
- Validate IPv4 addresses and required text input
- Persist server state in JSON
- Recover cleanly when the JSON file is missing or invalid
- Log important mutations such as add, edit, toggle, and remove
- Automated tests with `pytest`
- Type hints for the central data model and functions

## Tech Stack

- Python 3.10+
- Python standard library
- pytest

The application itself has no external runtime dependencies. `pytest` is only required for running the test suite.

## Architecture

```text
User
  |
  v
CLI / main.py
  |
  +--> Validation
  |
  +--> Business Logic
  |      add / edit / remove / toggle
  |
  +--> JSON Persistence
  |
  +--> Logging
```

The current version is intentionally a local CLI application. A separate browser-based integration is planned later using a web frontend, FastAPI, Docker, CI/CD, and Azure.

## Data Model

Each server is stored under its hostname:

```json
{
  "web1": {
    "status": "offline",
    "ip": "192.168.1.10",
    "os": "Ubuntu Server",
    "role": "Webserver"
  }
}
```

The application creates `servers.json` automatically when no valid data file exists. The file is runtime state and is intentionally excluded from Git.

## Installation

Clone the repository:

```bash
git clone https://github.com/RusmirOmerovic/server-status-cli.git
cd server-status-cli
```

Create and activate a virtual environment.

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the development dependency:

```bash
python -m pip install pytest
```

## Run the Application

```bash
python main.py
```

On first start, the application creates the local server inventory automatically.

## CLI Commands

| Command | Description |
| --- | --- |
| `list` | Show all servers |
| `add <server_name>` | Add a new server |
| `edit <server_name>` | Edit IP, OS, or role |
| `toggle <server_name>` | Toggle status between online and offline |
| `remove <server_name>` | Remove a server |
| `help` | Show available commands |
| `exit` | Exit the application |

### Example

```text
> add web3
IP-Adresse: 192.168.1.30
Betriebssystem: Ubuntu Server
Rolle: Webserver
[OK] web3 hinzugefügt -> offline

> toggle web3
[OK] web3 -> online

> list
Hostname        Status     IP              OS                   Role
------------------------------------------------------------------------------------
web3            online     192.168.1.30    Ubuntu Server        Webserver
```

## Validation

The CLI validates:

- IPv4 addresses using Python's `ipaddress` module
- Empty operating-system values
- Empty role values
- Duplicate server names
- Unknown servers
- Unsupported edit fields
- Incorrect command argument counts

Invalid input is handled without an uncaught traceback in normal CLI use.

## Persistence

Server data is stored locally in:

```text
servers.json
```

The file is excluded through `.gitignore` because it represents mutable runtime data rather than source code.

If the file is missing or contains invalid JSON, the application initializes a fresh server inventory.

## Logging

Important mutations are written to:

```text
server_manager.log
```

Logged operations include:

- Server added
- Server edited
- Status toggled
- Server removed

Log files are excluded from Git.

## Tests

Run the test suite with:

```bash
python -m pytest
```

The tests cover core business logic and persistence behavior, including:

- Adding servers
- Duplicate protection
- Editing servers
- Invalid edit fields
- Removing servers
- Unknown-server handling
- Status toggling
- Saving and loading JSON
- Missing JSON files
- Invalid JSON files

## Project Structure

```text
server-status-cli/
├── main.py
├── tests/
│   └── test_main.py
├── .gitignore
└── README.md
```

Runtime files such as `servers.json` and `server_manager.log` are generated locally and are not versioned.

## Project Goals

This project focuses on practical Python engineering fundamentals:

- separating CLI handling from reusable functions
- working with nested dictionaries
- input validation
- mutation and persistence
- defensive error handling
- automated testing
- logging
- type hints
- incremental Git-based development

## Planned Follow-up

The CLI is the base application. A separate follow-up project is planned to expose the existing Python logic through a browser-based demo using:

```text
Browser
  |
  v
HTML / CSS / JavaScript
  |
  v
FastAPI
  |
  v
Python business logic
  |
  v
Docker -> CI/CD -> Azure -> omerovic.de
```

That deployment layer is intentionally kept outside the scope of the CLI v1.0 release.

## License

No license has been added yet.
