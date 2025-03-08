# GNUBank

GNUBank is a simple banking system simulation that provides both CLI and GUI interfaces for managing bank accounts, transactions, and user data.

## Features

- User Management
  - Registration and login system
  - Profile management
  - Admin dashboard
- Account Management
  - Create and close bank accounts
  - View account balances
  - Manage favorite accounts
- Transaction Features
  - Money transfers between accounts
  - Transaction history
  - Bill payments
  - Loan requests
- Admin Features
  - User information management
  - Account balance management
  - Account creation and closure

## Requirements

- Python 3.x
- Required Python packages:
  - pyfiglet
  - uuid
  - datetime
  - threading

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aaii-z/GNUBank.git
cd GNUBank
```

2. Install required packages:
```bash
pip install pyfiglet
```

## Usage

### CLI Version
Run the CLI version with:
```bash
python3 App-CLI.py
```

### GUI Version
Run the GUI version with:
```bash
python3 App-GUI.py
```

## File Structure

- `App-CLI.py` - Command Line Interface version
- `App-GUI.py` - Graphical User Interface version
- `DB.py` - Database management system
- `schema.txt` - Database schema definition
- `*.txt` - Data storage files (User.txt, Bank_acc.txt, etc.)

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.

## Author

AAII (https://github.com/aaii-z)

## Security Notice

This is a simulation project and should not be used for real banking operations. The current implementation uses text files for storage and lacks proper security measures required for a production banking system.
