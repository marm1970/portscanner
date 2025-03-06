import argparse
import asyncio
import socket
import sys
import logging

from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from tqdm import tqdm

DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 65535
DEFAULT_TIMEOUT = 1.0
DEFAULT_CONCURRENCY = 1000

logging.basicConfig(
    level=logging.DEBUG,
    filename="port_scanner.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

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


async def scan_port(target: str, port: int, timeout: float) -> tuple[int, bool]:
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(host=target, port=port), timeout=timeout
        )
        writer.close()
        if sys.version_info >= (3, 7):
            await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError) as e:
        logging.debug(f"Port {port}: {e}")
        return port, False


async def scan_target(
    target: str, start_port: int, end_port: int, timeout: float, concurrency: int
) -> list[int]:
    open_ports = []
    semaphore = asyncio.Semaphore(concurrency)

    async def sem_scan(port: int):
        async with semaphore:
            return await scan_port(target, port, timeout)

    ports = range(start_port, end_port + 1)
    tasks = [asyncio.create_task(sem_scan(port)) for port in ports]
    with tqdm(total=len(ports), desc="Scanning ports", unit="port") as progress_bar:
        for future in asyncio.as_completed(tasks):
            port, is_open = await future
            if is_open:
                open_ports.append(port)
            progress_bar.update(1)
    return open_ports


def display_results(target: str, open_ports: list[int]) -> None:
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
    parser = argparse.ArgumentParser(description="Asynchronous Port Scanner")
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
        "-c",
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help="Maximum concurrent connections (default: 1000).",
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
    if args.concurrency <= 0:
        parser.error("Concurrency must be greater than 0.")
    console.print("\n[success]Scanning...[/success]\n")
    try:
        open_ports = asyncio.run(
            scan_target(
                args.target,
                args.start_port,
                args.end_port,
                args.timeout,
                args.concurrency,
            )
        )
        console.print("\n")
        display_results(args.target, open_ports)
    except KeyboardInterrupt:
        console.print("\n[error]Scan interrupted by user.[/error]")
        sys.exit(0)


if __name__ == "__main__":
    main()
