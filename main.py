import socket

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

custom_theme = Theme(
    {
        "header": "bold magenta",
        "data": "cyan",
        "success": "green",
        "error": "bold red",
    }
)
console = Console(theme=custom_theme)


def scan_port(target, port, timeout=1):
    try:
        with socket.create_connection((target, port), timeout=timeout):
            return port
    except OSError:
        return None


def scan_target(target, start_port=1, end_port=65535, timeout=1, threads=10):
    ports = range(start_port, end_port + 1)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(
            tqdm(
                executor.map(lambda p: scan_port(target, p, timeout), ports),
                total=len(ports),
                desc="Scanning ports",
                unit="port",
            )
        )
    return [port for port in results if port is not None]


def display_results(target, open_ports):
    if open_ports:
        console.rule("[header]Scan Results[/header]")
        table = Table(
            title=f"Open Ports on {target}", style="data", border_style="green"
        )
        table.add_column("Port", style="bold green", justify="center")
        table.add_column("Status", style="bold yellow", justify="center")
        for port in open_ports:
            table.add_row(str(port), "✅ Open")
        console.print(table)
    else:
        console.rule("[error]Scan Results[/error]")
        console.print(f"[error]No open ports found on {target}.[/error]")


def main():
    console.rule("[header]Port Scanner[/header]")
    target = input("Enter the IP address or domain name to scan: ")
    start_port = int(input("Enter the starting port (default: 1): ") or 1)
    end_port = int(input("Enter the ending port (default: 65535): ") or 65535)
    timeout = float(input("Enter the timeout in seconds (default: 1): ") or 1)
    threads = int(input("Enter the number of threads (default: 10): ") or 10)
    console.print("\n[success]Scanning...[/success]\n")
    open_ports = scan_target(target, start_port, end_port, timeout, threads)
    console.print("\n")
    display_results(target, open_ports)


if __name__ == "__main__":
    main()
