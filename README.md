# RGNetsTool

RGNetsTool is an interactive shell tool designed to assist network administrators in checking RADIUS realm logs, verifying LDAP bindings, and inspecting firewall logs on the RGNets RXG.

## Features

- **Check MAC Address**: Verify a MAC address for a matching RADIUS realm.
- **LDAP Bind Test**: Check if the system is successfully bound to LDAP.
- **Check Firewall Logs**: Inspect firewall logs for blocked or passed packets on specific hosts.

## Requirements

- Python 3.x
- Paramiko library for SSH connections

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lmesserStep/RGNetsTool.git
   cd RGNetsTool


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lmesserStep/RGNetsTool.git
   cd RGNetsTool
   ```

2. Install the required dependencies:
   ```bash
   pip install paramiko
   ```

3. (Optional) To build the project into an executable, install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

## Usage

Run the interactive shell:
```bash
python RXGRealmChecker.py
```

Or, if you prefer the Windows executable (it is in the dist directory):
```bash
./RXGRealmChecker.exe
```

### Commands

- **connect**: Connect to the RXG.
  ```bash
  connect <IP> <username> <ssh_key_path>
  ```

- **disconnect**: Disconnect from the SSH server.
  ```bash
  disconnect
  ```

- **check_mac**: Check a MAC address for a matching RADIUS realm.
  ```bash
  check_mac <MAC>
  ```

- **bind_test**: Check if the system is bound to LDAP.
  ```bash
  bind_test
  ```

- **check_firewall**: Check the firewall logs for a specific host.
  ```bash
  check_firewall
  ```

- **exit**: Exit the shell.
  ```bash
  exit
  ```

### Example

1. **Connect to the RXG**:
   ```bash
   (RGNetsTool) connect 192.168.1.1 admin /path/to/ssh_key.pem
   ```

2. **Check a MAC address**:
   ```bash
   (RGNetsTool) check_mac 32-A9-C4-7C-00-4E
   (RGNetsTool) check_mac 32-A9-C4-7C-00-4E
   Parsing logs...
   Matched Rule: Clinton-Secure
   Matched Realms:
   1X local Auth
   ```

3. **Perform LDAP bind test**:
   ```bash
   (RGNetsTool) bind_test
   (RGNetsTool) bind_test
   LDAP Bind Test: Succeeded
  (RGNetsTool)
   ```

4. **Check firewall logs**:
   ```bash
   (RGNetsTool) check_firewall
   ```

5. **Disconnect from the SSH server**:
   ```bash
   (RGNetsTool) disconnect
   ```

## Building the Executable

To build the project into an executable, run:
```bash
pyinstaller --onefile RXGRealmChecker.py
```

The executable will be created in the `dist` directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

For any questions or suggestions, feel free to open an issue or contact the project maintainer.
```
