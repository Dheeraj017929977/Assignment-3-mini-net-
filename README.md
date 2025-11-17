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
   git clone https://github.com/Dheeraj017929977/Assignment-3-mini-net-.git
   cd Assignment-3-mini-net-
   sudo python3 exp1.py
   sudo python3 exp2.py
   ```

---

## Linux Testing Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/Dheeraj017929977/Assignment-3-mini-net-.git
cd Assignment-3-mini-net-
```

### Step 2: Install Mininet

```bash
# Update package list
sudo apt update

# Install dependencies
sudo apt install -y git python3-pip

# Clone and install Mininet
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -a
cd ..
```

### Step 3: Verify Installation

```bash
sudo mn --test pingall
```

If you see successful pings, Mininet is installed correctly.

### Step 4: Clean Up (Before Each Test)

```bash
sudo mn -c
```

### Step 5: Run Experiments

**Run Experiment 1:**
```bash
sudo python3 exp1.py
```
Results are saved to `result1.txt`. Type `exit` in the Mininet CLI when done.

**Run Experiment 2 (Automated):**
```bash
sudo python3 exp2.py
```

**Run Experiment 2 (Manual Mode - Recommended):**
```bash
MANUAL=1 sudo python3 exp2.py
```
When the script pauses, open a **NEW terminal window** and run:
```bash
sudo ovs-ofctl -O OpenFlow13 show s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"
```
Then return to the first terminal and press ENTER. Results are saved to `result2.txt`.

---

## Prerequisites

- Mininet installed on your system
- Python 3
- Open vSwitch (OVS) tools (for Experiment 2)
- sudo privileges (required to run Mininet)

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

**Manual mode (run commands from another terminal - matches assignment instructions):**
```bash
MANUAL=1 sudo python3 exp2.py   # or use HOLD=1 (same effect)
```
When the script pauses, **open a NEW terminal window** and run these commands:
```bash
# 1. Check port state of s1
sudo ovs-ofctl -O OpenFlow13 show s1

# 2. Check flow table (should be empty initially)
sudo ovs-ofctl -O OpenFlow13 dump-flows s1

# 3. Drop all traffic from port s1-eth2
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"

# 4. Forward traffic from port s1-eth1 to s1-eth3
sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"
```
Then go back to the first terminal and press ENTER to let the script finish. All commands and outputs (including the exact ovs-ofctl commands you used) are automatically documented in `result2.txt`.

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

- **`Cannot find required executable mnexec`**: This means the Python mininet package is installed, but the system binaries are missing. Reinstall Mininet: `cd mininet && sudo ./util/install.sh -a`

- **Permission denied**: Make sure you're running with `sudo`

- **Mininet not found / ModuleNotFoundError**: Ensure Mininet is properly installed on Linux. The `pip install mininet` command only installs the Python package, not the full Mininet system.

- **OVS commands fail**: Ensure Open vSwitch is installed and running: `sudo apt install -y openvswitch-switch openvswitch-common`

- **Network cleanup**: If a previous run didn't clean up properly, you may need to run `sudo mn -c` to clean up Mininet

