import nmap
import os
from datetime import datetime

# Create reports directory if it doesn't exist
if not os.path.exists("reports"):
    os.makedirs("reports")

# Get target IP
target = input("Enter target IP: ")

# Current date/time
start_time = datetime.now()

# Create unique filename
filename = f"reports/report_{start_time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

# Nmap scanner
scanner = nmap.PortScanner()

print(f"\nScanning {target}...")
print("Please wait...\n")

# Run scan
scanner.scan(target, arguments="-sV")

# Open report file
with open(filename, "w") as report:

    report.write("=" * 50 + "\n")
    report.write("NETWORK ASSET SCANNER REPORT\n")
    report.write("=" * 50 + "\n\n")

    report.write(f"Target: {target}\n")
    report.write(f"Scan Start: {start_time}\n\n")

    for host in scanner.all_hosts():

        print(f"Host: {host}")
        report.write(f"Host: {host}\n")

        report.write(
            f"State: {scanner[host].state()}\n\n"
        )

        for protocol in scanner[host].all_protocols():

            print(f"\nProtocol: {protocol}")
            report.write(f"\nProtocol: {protocol}\n")

            ports = sorted(
                scanner[host][protocol].keys()
            )

            for port in ports:

                service = scanner[host][protocol][port]["name"]

                try:
                    version = (
                        scanner[host][protocol][port]["product"]
                    )
                except:
                    version = "Unknown"

                result = (
                    f"Port: {port} | "
                    f"Service: {service} | "
                    f"Version: {version}"
                )

                print(result)
                report.write(result + "\n")

    end_time = datetime.now()

    report.write("\n")
    report.write("=" * 50 + "\n")
    report.write(f"Scan End: {end_time}\n")
    report.write(
        f"Duration: {end_time - start_time}\n"
    )
    report.write("=" * 50 + "\n")

print("\nScan Complete!")
print(f"Report saved to: {filename}")
