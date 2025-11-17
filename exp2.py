#!/usr/bin/env python3
"""
Experiment 2 – SDN (Layer 2) forwarding with Open vSwitch.

Topology
--------
    h1 ---\
            s1 --- s2 --- h3
    h2 ---/

Requirements
------------
* h1, h2, h3 share one /24 subnet.
* s1 must drop all traffic arriving on s1-eth2 (the h2 link).
* s1 must forward all traffic arriving on s1-eth1 out of s1-eth3 (toward s2).
* Show ovs-ofctl port/flow information and record ping results before/after.
"""

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import os


def section(file_handle, title, content):
    """Write a titled block into result2.txt."""
    file_handle.write(f"\n=== {title} ===\n")
    file_handle.write(content.strip() + "\n")


def build_network():
    """Create the topology with standalone OVS switches."""
    net = Mininet(controller=None, link=TCLink, switch=OVSKernelSwitch)

    info("*** Adding switches (standalone, OpenFlow13)\n")
    s1 = net.addSwitch("s1", failMode="standalone", protocols="OpenFlow13")
    s2 = net.addSwitch("s2", failMode="standalone", protocols="OpenFlow13")

    info("*** Adding hosts\n")
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")
    h3 = net.addHost("h3", ip="10.0.0.3/24")

    info("*** Creating links (defines port numbering)\n")
    net.addLink(h1, s1)  # s1-eth1
    net.addLink(h2, s1)  # s1-eth2
    net.addLink(s1, s2)  # s1-eth3 <-> s2-eth1
    net.addLink(s2, h3)  # s2-eth2

    info("*** Starting Mininet\n")
    net.start()
    return net, (h1, h2, h3), (s1, s2)


def run_experiment():
    net, (h1, h2, h3), (s1, _s2) = build_network()

    # Flow rule commands that will be documented and executed
    show_cmd = "sudo ovs-ofctl -O OpenFlow13 show s1"
    dump_flows_cmd = "sudo ovs-ofctl -O OpenFlow13 dump-flows s1"
    drop_cmd = 'sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"'
    fwd_cmd = 'sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"'

    with open("result2.txt", "w") as out:
        out.write("Experiment 2: SDN (Layer 2) results\n")
        out.write("=" * 70 + "\n\n")

        # Instructions for manual testing from another terminal
        out.write("INSTRUCTIONS: Manual Testing from Another Terminal Window\n")
        out.write("-" * 70 + "\n")
        out.write(
            "While exp2.py is running, open a NEW terminal window and execute:\n\n"
        )
        out.write(f"1. Check port state of s1:\n")
        out.write(f"   {show_cmd}\n\n")
        out.write(f"2. Check flow table (should be empty initially):\n")
        out.write(f"   {dump_flows_cmd}\n\n")
        out.write(f"3. Drop all flows from port s1-eth2:\n")
        out.write(f"   {drop_cmd}\n\n")
        out.write(f"4. Forward flows from port s1-eth1 to s1-eth3:\n")
        out.write(f"   {fwd_cmd}\n\n")
        out.write("=" * 70 + "\n\n")

        # Baseline ovs-ofctl info
        info("*** Capturing baseline state of s1\n")
        section(
            out, "ovs-ofctl show s1 (before)", s1.cmd("ovs-ofctl -O OpenFlow13 show s1")
        )
        section(
            out,
            "ovs-ofctl dump-flows s1 (before) - should be empty",
            s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"),
        )

        # Baseline pings
        info("*** Running baseline ping tests\n")
        section(
            out, "Ping h1 -> h3 (before flow rules)", h1.cmd(f"ping -c 1 {h3.IP()}")
        )
        section(
            out, "Ping h2 -> h3 (before flow rules)", h2.cmd(f"ping -c 1 {h3.IP()}")
        )

        # Document the commands that will be used
        out.write("\n" + "=" * 70 + "\n")
        out.write("FLOW RULE COMMANDS USED\n")
        out.write("=" * 70 + "\n\n")
        out.write("These commands were executed (manually or automatically):\n\n")
        out.write(f"Command 1 - Drop traffic from s1-eth2 (port 2):\n")
        out.write(f"  {drop_cmd}\n\n")
        out.write(
            f"Command 2 - Forward traffic from s1-eth1 (port 1) to s1-eth3 (port 3):\n"
        )
        out.write(f"  {fwd_cmd}\n\n")
        out.write("=" * 70 + "\n\n")

        # Optional pause for manual execution
        # Supports both MANUAL=1 and HOLD=1 for compatibility
        manual_mode = os.environ.get("MANUAL", os.environ.get("HOLD", "")).lower() in (
            "1",
            "true",
            "yes",
        )

        if manual_mode:
            info("\n" + "=" * 70 + "\n")
            info("*** MANUAL MODE: Run commands from another terminal window\n")
            info("=" * 70 + "\n")
            info(
                "The network is now running. Open a NEW terminal window and execute:\n\n"
            )
            info(f"  {show_cmd}\n")
            info(f"  {dump_flows_cmd}\n")
            info(f"  {drop_cmd}\n")
            info(f"  {fwd_cmd}\n\n")
            info(
                "After running these commands, come back to this terminal and press ENTER.\n"
            )
            info("=" * 70 + "\n\n")
            input(
                "Press ENTER after you have run the ovs-ofctl commands in another terminal...\n"
            )
        else:
            info("*** Installing flow rules automatically\n")
            # Install flow rules automatically
            s1.cmd(drop_cmd.replace("sudo ", ""))
            s1.cmd(fwd_cmd.replace("sudo ", ""))

        # Show flows after programming
        section(
            out,
            "ovs-ofctl dump-flows s1 (after)",
            s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"),
        )

        # Connectivity after rules
        section(out, "Ping h1 -> h3 (after)", h1.cmd(f"ping -c 1 {h3.IP()}"))
        section(out, "Ping h2 -> h3 (after)", h2.cmd(f"ping -c 1 {h3.IP()}"))

    info("*** Experiment complete. See result2.txt for details.\n")

    if os.environ.get("SKIP_CLI", "").lower() not in ("1", "true", "yes"):
        info("*** Mininet CLI available for manual checks. Type 'exit' to stop.\n")
        CLI(net)

    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run_experiment()
