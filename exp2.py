#!/usr/bin/env python3
"""
Experiment 2: SDN (L2)
Creates a Mininet topology with hosts and OpenFlow switches,
configures flow rules using ovs-ofctl, and tests connectivity.
"""

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, Controller
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import subprocess
import time
import os
import re
import sys


def createTopology():
    """Create the network topology with hosts and switches."""
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)

    info("*** Adding controller\n")
    # Add a controller (required for OVS switches)
    c0 = net.addController("c0")

    info("*** Adding hosts\n")
    # Add hosts
    h1 = net.addHost("h1")
    h2 = net.addHost("h2")
    h3 = net.addHost("h3")

    info("*** Adding switches\n")
    # Add switches (OVSKernelSwitch)
    s1 = net.addSwitch("s1")
    s2 = net.addSwitch("s2")

    info("*** Creating links\n")
    # Create links according to the topology diagram
    # h1 connected to s1 (h1-eth0 to s1-eth1)
    net.addLink(h1, s1, intfName1="h1-eth0", intfName2="s1-eth1")

    # h2 connected to s1 (h2-eth0 to s1-eth2)
    net.addLink(h2, s1, intfName1="h2-eth0", intfName2="s1-eth2")

    # s1 connected to s2 (s1-eth3 to s2-eth1)
    net.addLink(s1, s2, intfName1="s1-eth3", intfName2="s2-eth1")

    # s2 connected to h3 (s2-eth2 to h3-eth0)
    net.addLink(s2, h3, intfName1="s2-eth2", intfName2="h3-eth0")

    info("*** Starting network\n")
    net.start()

    return net


def runInitialPingTests(net):
    """Run ping tests before flow rules and save results to result2.txt."""
    info("*** Running initial ping tests (before flow rules)\n")

    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")

    results = []
    results.append("=" * 60)
    results.append("Experiment 2: SDN (L2) - Results")
    results.append("=" * 60)
    results.append("")

    results.append("PART 1: Initial Ping Tests (Before Flow Rules)")
    results.append("-" * 60)
    results.append("")

    # Ping from h1 to h3
    results.append("1. Ping from h1 to h3:")
    results.append("-" * 60)
    ping_result = h1.cmd("ping -c 1 h3")
    results.append(ping_result)
    results.append("")

    # Ping from h2 to h3
    results.append("2. Ping from h2 to h3:")
    results.append("-" * 60)
    ping_result = h2.cmd("ping -c 1 h3")
    results.append(ping_result)
    results.append("")

    # Write initial results to file
    with open("result2.txt", "w") as f:
        f.write("\n".join(results))

    info("*** Initial ping test results saved to result2.txt\n")

    return results


def showSwitchInfo(net):
    """Show switch port state and flow table using ovs-ofctl."""
    info("*** Checking switch s1 port state and flow table\n")

    s1 = net.get("s1")

    results = []
    results.append("")
    results.append("PART 2: Switch s1 Information")
    results.append("-" * 60)
    results.append("")

    # Show port state
    results.append("1. Port state of s1 (ovs-ofctl show s1):")
    results.append("-" * 60)
    show_result = subprocess.run(
        ["sudo", "ovs-ofctl", "show", "s1"], capture_output=True, text=True
    )
    results.append(show_result.stdout)
    results.append("")

    # Show flow table (should be empty at this point)
    results.append("2. Flow table of s1 (ovs-ofctl dump-flows s1):")
    results.append("-" * 60)
    dump_result = subprocess.run(
        ["sudo", "ovs-ofctl", "dump-flows", "s1"], capture_output=True, text=True
    )
    results.append(dump_result.stdout)
    results.append("")

    # Append to result file
    with open("result2.txt", "a") as f:
        f.write("\n".join(results))

    return results


def configureFlowRules(net):
    """Configure flow rules using ovs-ofctl."""
    info("*** Configuring flow rules on s1\n")

    results = []
    results.append("")
    results.append("PART 3: Flow Rules Configuration")
    results.append("-" * 60)
    results.append("")

    # Get port mapping from ovs-ofctl show output
    show_result = subprocess.run(
        ["sudo", "ovs-ofctl", "show", "s1"], capture_output=True, text=True
    )

    # Parse port numbers from the output
    # Format: " 1(s1-eth1): addr:..." or "PORT 1: s1-eth1"
    port_map = {}
    for line in show_result.stdout.split("\n"):
        if "s1-eth" in line:
            # Try to extract port number and interface name
            # Match patterns like " 1(s1-eth1):" or "PORT 1: s1-eth1"
            match = re.search(r"(\d+)\(s1-eth(\d+)\)", line)
            if match:
                port_num = int(match.group(1))
                iface_num = int(match.group(2))
                port_map[iface_num] = port_num
            else:
                # Alternative pattern: "PORT 1: s1-eth1"
                match = re.search(r"PORT\s+(\d+).*s1-eth(\d+)", line)
                if match:
                    port_num = int(match.group(1))
                    iface_num = int(match.group(2))
                    port_map[iface_num] = port_num

    # Default to sequential port numbers if parsing fails
    # In Mininet, ports are typically numbered sequentially
    if not port_map:
        port_map = {1: 1, 2: 2, 3: 3}
        info("*** Using default port mapping (1->1, 2->2, 3->3)\n")
    else:
        info(f"*** Port mapping: {port_map}\n")

    # Get port numbers
    port_s1_eth1 = port_map.get(1, 1)  # Port for s1-eth1
    port_s1_eth2 = port_map.get(2, 2)  # Port for s1-eth2
    port_s1_eth3 = port_map.get(3, 3)  # Port for s1-eth3

    # Drop all flows from port s1-eth2
    cmd_drop = [
        "sudo",
        "ovs-ofctl",
        "add-flow",
        "s1",
        f"priority=100,in_port={port_s1_eth2},actions=drop",
    ]
    results.append("Command to drop flows from s1-eth2:")
    results.append(" ".join(cmd_drop))
    results.append("")

    drop_result = subprocess.run(cmd_drop, capture_output=True, text=True)
    if drop_result.returncode == 0:
        results.append("Flow rule added successfully: drop all flows from s1-eth2")
    else:
        results.append(f"Error adding drop rule: {drop_result.stderr}")
    results.append("")

    # Forward flows from s1-eth1 to s1-eth3
    cmd_forward = [
        "sudo",
        "ovs-ofctl",
        "add-flow",
        "s1",
        f"priority=100,in_port={port_s1_eth1},actions=output:{port_s1_eth3}",
    ]
    results.append("Command to forward flows from s1-eth1 to s1-eth3:")
    results.append(" ".join(cmd_forward))
    results.append("")

    forward_result = subprocess.run(cmd_forward, capture_output=True, text=True)
    if forward_result.returncode == 0:
        results.append(
            "Flow rule added successfully: forward flows from s1-eth1 to s1-eth3"
        )
    else:
        results.append(f"Error adding forward rule: {forward_result.stderr}")
    results.append("")

    # Also need to add reverse flow for return traffic (from s1-eth3 to s1-eth1)
    cmd_reverse = [
        "sudo",
        "ovs-ofctl",
        "add-flow",
        "s1",
        f"priority=100,in_port={port_s1_eth3},actions=output:{port_s1_eth1}",
    ]
    results.append(
        "Command to forward flows from s1-eth3 to s1-eth1 (for return traffic):"
    )
    results.append(" ".join(cmd_reverse))
    results.append("")

    reverse_result = subprocess.run(cmd_reverse, capture_output=True, text=True)
    if reverse_result.returncode == 0:
        results.append(
            "Flow rule added successfully: forward flows from s1-eth3 to s1-eth1"
        )
    else:
        results.append(f"Error adding reverse rule: {reverse_result.stderr}")
    results.append("")

    # Show updated flow table
    results.append("Updated flow table of s1:")
    results.append("-" * 60)
    dump_result = subprocess.run(
        ["sudo", "ovs-ofctl", "dump-flows", "s1"], capture_output=True, text=True
    )
    results.append(dump_result.stdout)
    results.append("")

    # Append to result file
    with open("result2.txt", "a") as f:
        f.write("\n".join(results))

    info("*** Flow rules configured and saved to result2.txt\n")


def runFinalPingTests(net):
    """Run ping tests after flow rules and save results to result2.txt."""
    info("*** Running final ping tests (after flow rules)\n")

    h1 = net.get("h1")
    h3 = net.get("h3")

    results = []
    results.append("")
    results.append("PART 4: Final Ping Tests (After Flow Rules)")
    results.append("-" * 60)
    results.append("")

    # Ping from h1 to h3 (should work - h1 uses s1-eth1 which is forwarded)
    results.append("1. Ping from h1 to h3:")
    results.append("-" * 60)
    ping_result = h1.cmd("ping -c 1 h3")
    results.append(ping_result)
    results.append("")

    # Note: h2 to h3 should fail because s1-eth2 is dropped
    # But the assignment only asks for h1 to h3 after flow rules

    # Append to result file
    with open("result2.txt", "a") as f:
        f.write("\n".join(results))

    info("*** Final ping test results saved to result2.txt\n")


def main():
    """Main function to create topology, configure flows, and test."""
    setLogLevel("info")

    # Create topology
    net = createTopology()

    try:
        # Wait a bit for network to stabilize
        time.sleep(2)

        # Run initial ping tests (before flow rules)
        runInitialPingTests(net)

        # Show switch information
        showSwitchInfo(net)

        # Configure flow rules
        configureFlowRules(net)

        # Wait a bit for flow rules to take effect
        time.sleep(1)

        # Run final ping tests (after flow rules)
        runFinalPingTests(net)

        # Start CLI for manual testing (only if SKIP_CLI env var is not set)
        if os.environ.get("SKIP_CLI", "").lower() not in ("1", "true", "yes"):
            info("*** Network is ready. You can use CLI for manual testing.\n")
            info('*** Type "exit" to stop the network.\n')
            CLI(net)
        else:
            info("*** Tests completed. Skipping CLI (non-interactive mode).\n")
    finally:
        # Clean up
        info("*** Stopping network\n")
        net.stop()


if __name__ == "__main__":
    main()
