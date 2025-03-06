# 🔍 Asynchronous Port Scanner

A high-performance, asynchronous Python port scanner with rich visual output, designed to efficiently identify open ports on a target system.

## 🚀 Installation

Follow these steps to set up the project:

### 1️⃣ Clone the Repository
   ```bash
   git clone https://github.com/marm1970/portscanner.git
   cd portscanner
   ```

### 2️⃣ Create a Virtual Environment
   ```bash
   python -m venv venv
   ```

### 3️⃣ Activate the Virtual Environment
   - **Windows**:
     ```bash
     venv\Scripts\Activate.ps1
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

### 4️⃣ Install Dependencies
   ```bash
   python -m pip install rich tqdm
   ```

## ⚡ Usage

Run the script using the following syntax:

```bash
python main.py <target> [options]
```

### Required Argument:
- `<target>`: The IP address or domain to scan.

### Optional Arguments:
- `-s, --start-port <port>`: Starting port (default: `1`).
- `-e, --end-port <port>`: Ending port (default: `65535`).
- `-t, --timeout <seconds>`: Timeout for each connection attempt (default: `1.0`).
- `-c, --concurrency <num>`: Maximum concurrent connections (default: `1000`).

### Example Usage:

```bash
python main.py example.com -s 20 -e 1000 -t 0.5 -c 500
```

This scans ports `20-1000` on `example.com` with a timeout of `0.5` seconds per port and a concurrency level of `500`.

## 📊 Output

Results are displayed in a structured, visually formatted table using `rich`. Open ports will be highlighted with a ✅ marker for easy identification.

## 🤝 Contributing

Contributions are welcome! Follow these steps to contribute:

1️⃣ **Fork the repository**  
2️⃣ **Create a new branch**  
   ```bash
   git checkout -b feature-name
   ```
3️⃣ **Commit your changes**  
   ```bash
   git commit -m "Describe your changes"
   ```
4️⃣ **Push to your branch**  
   ```bash
   git push origin feature-name
   ```
5️⃣ **Open a pull request** and provide details about your changes.

---

💡 Have suggestions or found a bug? Feel free to open an issue or submit a pull request!
