# Mininet Network Experiments

This repository contains two Mininet experiments for IP Routing and SDN (L2) configurations.

## Quick Start

**If you're getting `ModuleNotFoundError: No module named 'mininet'` or `Cannot find required executable mnexec`:**

The `pip install mininet` command only installs the Python package, but Mininet also requires system binaries (like `mnexec`) that need Linux kernel features. On macOS, the easiest solution is to use **Docker**:

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

This experiment creates a network topology with hosts and OpenFlow switches, configures flow rules using `ovs-ofctl`, and tests connectivity.

**To run:**
```bash
sudo python3 exp2.py
```

**What it does:**
1. Creates topology with hosts h1, h2, h3 and switches s1, s2 (OVSKernelSwitch)
2. Runs initial ping tests (before flow rules):
   - from h1 to h3
   - from h2 to h3
3. Shows switch s1 port state and flow table using `ovs-ofctl show s1` and `ovs-ofctl dump-flows s1`
4. Configures flow rules on s1:
   - Drops all flows from port s1-eth2
   - Forwards all flows from port s1-eth1 to s1-eth3
5. Runs final ping tests (after flow rules):
   - from h1 to h3
6. Saves all results to `result2.txt`
7. Opens Mininet CLI for manual testing (type `exit` to stop)

**Note:** The script will automatically populate `result2.txt` with all test results, including:
- Initial ping test results
- Switch port state and flow table information
- Flow rule commands used
- Final ping test results

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

