import socket
import argparse
import sys

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 65535
DEFAULT_TIMEOUT = 1
DEFAULT_THREADS = 10

custom_theme = Theme(
    {
        "header": "bold magenta",
        "data": "cyan",
        "success": "green",
        "error": "bold red",
    }
)
console = Console(theme=custom_theme)


def validate_ip(target: str) -> str:
    try:
        socket.gethostbyname(target)
        return target
    except socket.gaierror:
        raise argparse.ArgumentTypeError(f"Invalid IP address or domain name: {target}")


def scan_port(
    target: str, port: int, timeout: float = DEFAULT_TIMEOUT
) -> tuple[int, str | None]:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((target, port))
            return port, None
    except socket.timeout:
        return port, "Timeout"
    except ConnectionRefusedError:
        return port, "Connection Refused"
    except OSError as e:
        return port, str(e)


def scan_target(
    target: str,
    start_port: int = DEFAULT_START_PORT,
    end_port: int = DEFAULT_END_PORT,
    timeout: float = DEFAULT_TIMEOUT,
    threads: int = DEFAULT_THREADS,
) -> list[int]:
    ports = range(start_port, end_port + 1)
    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, target, p, timeout) for p in ports]
        with tqdm(total=len(ports), desc="Scanning ports", unit="port") as progress_bar:
            for future in futures:
                port, error_msg = future.result()
                if error_msg is None:
                    open_ports.append(port)
                progress_bar.update(1)
    return open_ports


def display_results(target: str, open_ports: list[int]):
    console.rule("[header]Scan Results[/header]")
    if open_ports:
        table = Table(
            title=f"Open Ports on {target}", style="data", border_style="green"
        )
        table.add_column("Port", style="bold green", justify="center")
        table.add_column("Status", style="bold yellow", justify="center")
        for port in open_ports:
            table.add_row(str(port), "✅ Open")
        console.print(table)
    else:
        console.print(f"[error]No open ports found on {target}.[/error]")


def main():
    parser = argparse.ArgumentParser(description="A simple port scanner.")
    parser.add_argument(
        "target", help="The IP address or domain name to scan.", type=validate_ip
    )
    parser.add_argument(
        "-s",
        "--start-port",
        type=int,
        default=DEFAULT_START_PORT,
        help="The starting port (default: 1).",
    )
    parser.add_argument(
        "-e",
        "--end-port",
        type=int,
        default=DEFAULT_END_PORT,
        help="The ending port (default: 65535).",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="The timeout in seconds (default: 1).",
    )
    parser.add_argument(
        "-T",
        "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help="The number of threads (default: 10).",
    )
    args = parser.parse_args()
    if not 1 <= args.start_port <= 65535:
        parser.error("Start port must be between 1 and 65535.")
    if not 1 <= args.end_port <= 65535:
        parser.error("End port must be between 1 and 65535.")
    if args.start_port > args.end_port:
        parser.error("Start port cannot be greater than end port.")
    if args.timeout <= 0:
        parser.error("Timeout must be greater than 0.")
    if args.threads <= 0:
        parser.error("Threads must be greater than 0.")
    console.print("\n[success]Scanning...[/success]\n")
    try:
        open_ports = scan_target(
            args.target, args.start_port, args.end_port, args.timeout, args.threads
        )
        console.print("\n")
        display_results(args.target, open_ports)
    except KeyboardInterrupt:
        console.print("\n[error]Scan interrupted by user.[/error]")
        sys.exit(0)


if __name__ == "__main__":
    main()
