# ZeroTier API CLI

A command-line interface for managing ZeroTier networks, built with Python.

## Features

- List all members in your ZeroTier network
- View pending (unauthorized) members
- Authorize new members
- Remove members from the network
- JSON output support
- Rich terminal output with tables

## Installation

### Recommended: Using pipx

```bash
pipx install zerotier-api-cli
```

### Alternative: Using pip

```bash
pip install zerotier-api-cli
```

### Development: Using Poetry

```bash
# Clone the repository
git clone https://github.com/yourusername/zerotier-api-cli.git
cd zerotier-api-cli

# Install dependencies
poetry install

# Install the package
poetry build
pip install dist/*.whl
```

## Configuration

The CLI requires two pieces of information to work:

1. ZeroTier API Token
2. Network ID

You can provide these in three ways:

### 1. Environment Variables

```bash
export ZEROTIER_TOKEN="your_api_token"
export ZEROTIER_NETWORK_ID="your_network_id"
```

### 2. Command Line Arguments

```bash
ztcli --token your_api_token --network-id your_network_id [command]
```

### 3. Configuration File

You can save your settings to a configuration file using the `save-settings` command:

```bash
ztcli --token your_api_token --network-id your_network_id save-settings
```

The configuration file will be saved to:

- Linux: `~/.config/zerotier-cli/config.yaml`
- macOS: `~/Library/Application Support/zerotier-cli/config.yaml`
- Windows: `%APPDATA%\zerotier-cli\config.yaml`

Once saved, you won't need to provide the token and network ID in subsequent commands.

## Usage

### List Network Members

```bash
# List all members
ztcli list

# List only pending members
ztcli list --pending

# Output as JSON
ztcli list --json
```

### Authorize a Member

```bash
ztcli approve MEMBER_ID
```

### Remove a Member

```bash
ztcli remove MEMBER_ID
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/zerotier-api-cli.git
cd zerotier-api-cli

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Running Tests

```bash
poetry run pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
