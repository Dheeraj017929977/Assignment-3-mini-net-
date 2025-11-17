# Mininet Network Experiments

This repository contains two Mininet experiments for IP Routing and SDN (L2) configurations.

## Installation on Ubuntu

### Step 1: Install Ubuntu

1. **Download Ubuntu:** Get the latest Ubuntu LTS ISO (22.04 recommended) from [ubuntu.com/download](https://ubuntu.com/download)

2. **Install Ubuntu:**
   - **Bare metal installation:**
     - Create a bootable USB using Rufus (Windows) or `dd`/BalenaEtcher (macOS/Linux)
     - Boot from the USB, choose *Install Ubuntu*, and follow the prompts (language, keyboard, disk selection, user creation)
   
   - **Virtual machine installation:**
     - Install VirtualBox or VMware
     - Create a new VM with at least 2 vCPUs, 4 GB RAM, and 20 GB disk space
     - Attach the Ubuntu ISO to the VM, boot it, and complete the installation

3. **Update Ubuntu after installation:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo reboot
   ```

### Step 2: Install Mininet and Dependencies

Open a terminal and run:

```bash
sudo apt update
sudo apt install -y mininet openvswitch-switch python3 python3-pip git
```

**Optional - Install from source (if apt package doesn't work):**
```bash
git clone https://github.com/mininet/mininet
cd mininet
sudo ./util/install.sh -a
```

### Step 3: Verify Installation

Test that Mininet is working correctly:

```bash
sudo mn --test pingall
```

If this command runs without errors, Mininet is installed correctly!

### Step 4: Get This Repository

Clone or download this repository:

```bash
cd ~
git clone <repository-url>
cd Assignment-3-mini-net-
```

## How to Run the Experiments

### Experiment 1: IP Routing

This experiment creates a network topology with hosts and routers, configures routing tables, and tests connectivity.

**To run:**
```bash
sudo python3 exp1.py
```

Or use the shell script:
```bash
sudo bash run_exp1.sh
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

**Note:** The script automatically populates `result1.txt` with ping test results.

---

### Experiment 2: SDN (L2)

This experiment creates a network topology with hosts and OpenFlow switches, uses `ovs-ofctl` to check switch states and configure flow rules, and tests connectivity.

**Assignment Requirements:**
- Show ping results from h1 to h3 and from h2 to h3 in `result2.txt`
- Check port state and flow table of s1 using `ovs-ofctl show s1` and `ovs-ofctl dump-flows s1`
- Use `ovs-ofctl add-flow` to drop all flows from port s1-eth2
- Use `ovs-ofctl add-flow` to forward all flows from port s1-eth1 to s1-eth3
- Show all commands used in `result2.txt`
- Show ping results again after flow rules are applied

**To run:**
```bash
sudo python3 exp2.py
```

Or use the shell script:
```bash
sudo bash run_exp2.sh
```

**What it does (automatically satisfies all assignment requirements):**
1. Creates topology with hosts h1, h2, h3 and switches s1, s2 (OVSKernelSwitch)
2. Executes `ovs-ofctl show s1` to check port state of switch s1 (saved to result2.txt)
3. Executes `ovs-ofctl dump-flows s1` to show flow table (should be empty at this point, saved to result2.txt)
4. Runs initial ping tests (before flow rules):
   - from h1 to h3: `ping -c 1 h3` (saved to result2.txt)
   - from h2 to h3: `ping -c 1 h3` (saved to result2.txt)
5. Configures flow rules on s1 using `ovs-ofctl add-flow` (commands shown in result2.txt):
   - Drops all flows from port s1-eth2: `ovs-ofctl add-flow s1 "in_port=2,actions=drop"`
   - Forwards all flows from port s1-eth1 to s1-eth3: `ovs-ofctl add-flow s1 "in_port=1,actions=output:3"`
6. Shows flow table after rules are added: `ovs-ofctl dump-flows s1` (saved to result2.txt)
7. Runs final ping tests (after flow rules):
   - from h1 to h3 (saved to result2.txt)
   - from h2 to h3 (saved to result2.txt)
8. Saves all results to `result2.txt`, including:
   - `ovs-ofctl show s1` output (before)
   - `ovs-ofctl dump-flows s1` output (before and after)
   - Initial ping test results (from h1 to h3 and from h2 to h3)
   - Flow rule commands used
   - Final ping test results (from h1 to h3 and from h2 to h3)
9. Opens Mininet CLI for manual testing (type `exit` to stop)

**Manual testing:** The script automatically captures all required commands and outputs. However, if you want to run `ovs-ofctl` commands manually from **another terminal window** while the Mininet network is running (as mentioned in the assignment), you can do so. The script includes a pause option - set `HOLD=1` environment variable:
```bash
# Run with manual pause option
HOLD=1 sudo python3 exp2.py

# In another terminal (while exp2.py is paused), you can run:
sudo ovs-ofctl -O OpenFlow13 show s1
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
```

**Note:** The script automatically populates `result2.txt` with all required test results, including all ping results and `ovs-ofctl` output as specified in the assignment.

---

## Important Notes

1. **Run with sudo**: Both scripts require sudo privileges to create network namespaces and configure network interfaces.

2. **Separate runs**: Experiments 1 and 2 are independent and do not share configurations.

3. **Result files**: The result files (`result1.txt` and `result2.txt`) are automatically generated when you run the scripts. You don't need to manually create them.

4. **CLI mode**: After running tests, both scripts open the Mininet CLI. You can:
   - Test additional commands manually
   - Type `exit` to stop the network and clean up

5. **Network cleanup**: If a previous run didn't clean up properly, run:
   ```bash
   sudo mn -c
   ```

## Files

- `exp1.py` - Experiment 1: IP Routing implementation (modular and well-organized with comments)
- `exp2.py` - Experiment 2: SDN (L2) implementation with `ovs-ofctl` (modular and well-organized with comments)
- `run_exp1.sh` - Shell script wrapper for Experiment 1
- `run_exp2.sh` - Shell script wrapper for Experiment 2
- `result1.txt` - Results from Experiment 1 (auto-generated)
- `result2.txt` - Results from Experiment 2 (auto-generated, contains all required outputs)

## Submission Requirements

The following files must be submitted (as specified in the assignment):

1. `exp1.py` - IP Routing experiment implementation
2. `exp2.py` - SDN (L2) experiment implementation
3. `result1.txt` - Ping test results from Experiment 1
4. `result2.txt` - All test results from Experiment 2, including:
   - Ping results from h1 to h3 and from h2 to h3
   - `ovs-ofctl show s1` output
   - `ovs-ofctl dump-flows s1` output (before and after)
   - Flow rule commands used
   - Ping results after flow rules are applied

**Note:** The code is modular and well-organized with comments explaining logical steps (e.g., "add switches", "configure routes", etc.).

## Changelog

- **11/6**: IP addresses in Task 1 diagram were updated (r1 and h2 IP addresses). The current implementation in `exp1.py` uses the updated IP addresses.

## Troubleshooting

- **Permission denied**: Make sure you're running with `sudo`
  ```bash
  sudo python3 exp1.py
  ```

- **Mininet not found / ModuleNotFoundError**: Ensure Mininet is properly installed:
  ```bash
  sudo apt install -y mininet
  sudo mn --test pingall
  ```

- **OVS commands fail**: Ensure Open vSwitch is installed:
  ```bash
  sudo apt install -y openvswitch-switch
  ```

- **Network cleanup**: If a previous run didn't clean up properly:
  ```bash
  sudo mn -c
  ```

- **Cannot find required executable mnexec**: The `pip install mininet` command only installs the Python package, not the full Mininet system. Use `apt install mininet` instead:
  ```bash
  sudo apt install -y mininet
  ```

## Reference

For more information on Mininet and OpenFlow tools, see:
- [Mininet OpenFlow Tutorial](https://github.com/mininet/openflow-tutorial/wiki/Learn-Development-Tools)
