# Mininet Network Experiments

This repository contains two Mininet experiments for IP Routing and SDN (L2) configurations.

## Quick Start

### Preferred: Native Linux / Ubuntu VM

1. Install Ubuntu (20.04/22.04) in VirtualBox/VMware or use a native Linux system.
2. Install Mininet once:
   ```bash
   sudo apt update
   sudo apt install -y git python3-pip
   git clone https://github.com/mininet/mininet
   cd mininet
   sudo ./util/install.sh -a
   ```
3. Clone this repo and run the experiments:
   ```bash
   git clone <repo-url>
   cd Assignment-3-mini-net-
   sudo python3 exp1.py
   sudo python3 exp2.py
   ```

### macOS-only note

If you try to run Mininet directly on macOS you'll hit `ModuleNotFoundError: mininet`, `mnexec not found`, etc. The `pip install mininet` command only installs the Python helpers, not the kernel features. Use Docker or a Linux VM instead:

```bash
# 1. Install Docker Desktop (if not already installed)
# Download from: https://www.docker.com/products/docker-desktop

# 2. Run this command from the assignment directory:
docker run -it --rm --privileged \
  -v $(pwd):/workspace \
  -w /workspace \
  iwaseyusuke/mininet \
  bash

# 3. Inside the container, run:
sudo python3 exp1.py
# or
sudo python3 exp2.py
```

See the [Installation](#installation-macos) section below for more options.

## Prerequisites

- Mininet installed on your system
- Python 3
- Open vSwitch (OVS) tools (for Experiment 2)
- sudo privileges (required to run Mininet)

## Installation (macOS)

**Important:** Mininet is primarily designed for Linux. On macOS, you have several options:

### Option 1: Docker (Recommended for macOS)

This is the easiest way to run Mininet on macOS:

1. **Install Docker Desktop for Mac** from [docker.com](https://www.docker.com/products/docker-desktop)

2. **Pull the Mininet Docker image:**
   ```bash
   docker pull iwaseyusuke/mininet
   ```

3. **Run the experiments in Docker:**
   ```bash
   # Mount your assignment directory and run in the container
   docker run -it --rm --privileged \
     -v $(pwd):/workspace \
     -w /workspace \
     iwaseyusuke/mininet \
     bash
   ```

4. **Inside the Docker container, run:**
   ```bash
   sudo python3 exp1.py
   # or
   sudo python3 exp2.py
   ```

### Option 2: Linux VM (Most Reliable)

1. Install VirtualBox or VMware
2. Download and install Ubuntu 20.04 or 22.04
3. Install Mininet in the VM:
   ```bash
   git clone https://github.com/mininet/mininet
   cd mininet
   sudo ./util/install.sh -a
   ```
4. Copy your assignment files to the VM and run the scripts

### Option 3: Homebrew (Not Available)

Mininet is not available via Homebrew. Use Docker (Option 1) or a Linux VM (Option 2) instead.

### Option 4: Install from Source (Advanced)

If you want to install Mininet from source on macOS:

```bash
# Install dependencies
brew install python3 git

# Clone and install Mininet
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -a
```

**Note:** This may require additional system configuration and may not work perfectly on all macOS versions.

### Verify Installation

After installation, verify Mininet works:
```bash
sudo mn --test pingall
```

If this works, you're ready to run the experiments!

## How to Run

### Experiment 1: IP Routing

This experiment creates a network topology with hosts and routers, configures routing tables, and tests connectivity.

**To run:**
```bash
sudo python3 exp1.py
```

**What it does:**
1. Creates topology with hosts h1, h2, h3 and routers r1, r2
2. Configures IP addresses according to the assignment diagram
3. Sets up routing tables for all hosts
4. Runs ping tests:
   - from h1 to h3 (10.0.2.2)
   - from h2 to h3 (10.0.2.2)
   - from h3 to h1 (10.0.0.1)
   - from h3 to h2 (10.0.3.2)
5. Saves all ping results to `result1.txt`
6. Opens Mininet CLI for manual testing (type `exit` to stop)

**Note:** The script will automatically populate `result1.txt` with ping test results.

---

### Experiment 2: SDN (L2)

This experiment builds the L2 topology (two OVS switches, three hosts), captures baseline OVS state, programs the specified OpenFlow rules, and records connectivity results.

**To run (default automated mode):**
```bash
sudo python3 exp2.py
```

**Optional manual step (matches the assignment instructions):**
```bash
HOLD=1 sudo python3 exp2.py   # script pauses after the topology boots
```
When the prompt appears you can open another terminal and run:
```bash
sudo ovs-ofctl -O OpenFlow13 show s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"
```
Then press ENTER in the first terminal to let the script finish. The outputs (including the exact commands) are still written to `result2.txt`.

**What gets recorded automatically:**
- Baseline ovs-ofctl show/dump outputs (before flows)
- Pings from h1→h3 and h2→h3 before installing flows
- The exact add-flow commands
- Flow table contents after inserting the rules
- Pings from h1→h3 and h2→h3 after the rules are active
- Any CLI commands you run manually (if you stay in the Mininet CLI)

---

## Important Notes

1. **Run with sudo**: Both scripts require sudo privileges to create network namespaces and configure network interfaces.

2. **Separate runs**: Experiments 1 and 2 do not share configurations. Each experiment is independent.

3. **Result files**: The result files (`result1.txt` and `result2.txt`) are automatically generated when you run the scripts. You don't need to manually create them.

4. **CLI mode**: After running tests, both scripts open the Mininet CLI. You can:
   - Test additional commands manually
   - Type `exit` to stop the network and clean up

5. **Manual testing**: If you want to run `ovs-ofctl` commands manually for Experiment 2, you can do so from another terminal window while the Mininet network is running.

## Files

- `exp1.py` - Experiment 1: IP Routing implementation
- `exp2.py` - Experiment 2: SDN (L2) implementation
- `result1.txt` - Results from Experiment 1 (auto-generated)
- `result2.txt` - Results from Experiment 2 (auto-generated)

## Troubleshooting

- **`Cannot find required executable mnexec`**: This means the Python mininet package is installed, but the system binaries are missing. On macOS, use Docker (see Quick Start above) or a Linux VM. The `pip install mininet` command only installs the Python package, not the full Mininet system.

- **Permission denied**: Make sure you're running with `sudo`

- **Mininet not found / ModuleNotFoundError**: On macOS, use Docker or a Linux VM. Mininet requires Linux kernel features that aren't available on macOS.

- **OVS commands fail**: Ensure Open vSwitch is installed and running (included in Docker image)

- **Network cleanup**: If a previous run didn't clean up properly, you may need to run `sudo mn -c` to clean up Mininet

