import paramiko
import re
import time
import cmd


class RadiusShell(cmd.Cmd):
    intro = "Welcome to the RGNetsTool shell. Type help or ? to list commands.\n"
    prompt = "(RGNetsTool) "

    def __init__(self):
        super().__init__()
        self.client = None
        self.shell = None
        self.ip = None
        self.username = None
        self.ssh_key_path = None

    def do_connect(self, args):
        "Connect to the SSH server: connect <IP> <username> <ssh_key_path>"
        try:
            ip, username, ssh_key_path = args.split()
            self.ip = ip
            self.username = username
            self.ssh_key_path = ssh_key_path
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            print(f"Connecting to {ip} as {username} with key {ssh_key_path}")
            self.client.connect(ip, username=username, key_filename=ssh_key_path)
            self.shell = self.client.invoke_shell()
            print("Connected successfully.")
            self.clear_shell_output()  # Clear any initial output
        except Exception as e:
            print(f"Failed to connect: {e}")

    def do_disconnect(self, args):
        "Disconnect from the SSH server."
        if self.shell:
            self.shell.close()
        if self.client:
            self.client.close()
            self.client = None
            print("Disconnected successfully.")
        else:
            print("No active connection to disconnect.")

    def do_check_mac(self, mac):
        "Check a MAC address for a matching RADIUS realm: check_mac <MAC>"
        if not self.shell:
            print("Not connected. Use the connect command first.")
            return

        mac_formatted = self.format_mac_address(mac)
        command = f'tf /var/log/radius/radius.log | grep -A 12 "{mac_formatted}"\n'

        try:
            self.shell.send(command)
            time.sleep(2)  # Adjust the sleep time if necessary
            output = self.read_shell_output()

            if output:
                print("Parsing logs...")
                self.parse_logs(output)
            else:
                print("No logs found for the specified MAC address.")
        except Exception as e:
            print(f"Failed to execute command: {e}")

    def do_bind_test(self, args):
        "Check if the system is bound to LDAP: bind_test"
        if not self.shell:
            print("Not connected. Use the connect command first.")
            return

        command = 'wbinfo -p\n'
        print(f"Running command: {command.strip()}")

        try:
            self.shell.send(command)
            time.sleep(2)  # Adjust the sleep time if necessary
            output = self.read_shell_output()

            if "Ping to winbindd succeeded" in output:
                print("LDAP Bind Test: Succeeded")
            else:
                print("LDAP Bind Test: Failed")
        except Exception as e:
            print(f"Failed to execute command: {e}")

    def do_check_firewall(self, args):
        "Check the firewall logs for a specific host: check_firewall"
        if not self.shell:
            print("Not connected. Use the connect command first.")
            return

        try:
            # Get the root password from the 'iui' command
            command = 'iui\n'
            print(command)
            self.shell.send(command)
            time.sleep(8)
            iui_output = self.read_shell_output()
            time.sleep(15)
            root_password = iui_output.split('\n')[0]
            print(root_password)

            # Switch to the root user
            self.shell.send('su -\n')
            self.shell.send(f'{root_password}\n')
            time.sleep(2)
            self.clear_shell_output()

            host = input("Enter the host to check: ")
            action = input("Enter 'block' to see blocked packets or 'pass' to see passed packets: ").strip().lower()

            if action not in ['block', 'pass']:
                print("Invalid action. Please enter 'block' or 'pass'.")
                return

            command = f'tcpdump -n -eee -i pflog0 | grep {action}\n'
            # print(f"Running command: {command.strip()}")
            self.shell.send(command)

            while True:
                output = self.read_shell_output()
                if output:
                    print(output.strip())
                else:
                    time.sleep(2)  # Adjust the sleep time if necessary
        except Exception as e:
            print(f"Failed to execute command: {e}")

    def do_exit(self, args):
        "Exit the shell."
        print("Exiting the shell.")
        if self.shell:
            self.shell.close()
        if self.client:
            self.client.close()
        return True

    def read_shell_output(self):
        output = ""
        while self.shell.recv_ready():
            output += self.shell.recv(1024).decode()
        return output

    def clear_shell_output(self):
        """Clear any existing output in the shell buffer."""
        if self.shell.recv_ready():
            self.shell.recv(1024).decode()

    @staticmethod
    def format_mac_address(mac):
        return mac.replace(':', '-').upper()

    @staticmethod
    def parse_logs(logs):
        realms = []
        access_result = None
        rule = None

        for line in logs.splitlines():
            if "INFO> main::realm_matches_request request matches pattern set in RadiusServer" in line:
                match = re.search(r'pattern set in RadiusServer "(.*?)"', line)
                if match:
                    realms.append(match.group(1))

            if "INFO> main::realm_matches_request excluding RadiusServer" in line:
                match = re.search(r'excluding RadiusServer "(.*?)"', line)
                if match:
                    realms.append(f"Excluding {match.group(1)}")

            if "INFO> main::realm_matches_request selected highest priority" in line:
                match = re.search(r'selected highest priority\((\d+)\) matching RadiusAttributePattern "(.*?)"', line)
                if match:
                    rule = match.group(2)

            if "INFO> main::log_request_to_database logging Access-Accept" in line:
                access_result = "Access-Accept"
            elif "INFO> main::log_request_to_database logging Access-Reject" in line:
                access_result = "Access-Reject"

        if access_result:
            print(f"Access Result: {access_result}")
        if rule:
            print(f"Matched Rule: {rule}")
        if realms:
            print("Matched Realms:")
            for realm in realms:
                print(f"- {realm}")


if __name__ == "__main__":
    RadiusShell().cmdloop()
