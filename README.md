# Multi-Threaded Port Scanner

A fast, multi-threaded Python port scanner with rich visual output to identify open ports on a target.

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/marm1970/portscanner.git
   cd portscanner
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\Activate.ps1
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   python -m pip install rich tqdm
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Follow the prompts to:
   - Enter the target IP address or domain.
   - Specify the port range to scan.
   - Set timeout and thread count (optional).

3. View the results in a clean, visualized table showing open ports.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request and provide details about your changes.

---

Feel free to suggest improvements, report bugs, or share feedback!
