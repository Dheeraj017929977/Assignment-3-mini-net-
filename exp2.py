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

    # Optional pause so the student can run ovs-ofctl manually (per instructions)
    if os.environ.get("HOLD") == "1":
        input(
            "\n[Experiment 2] Network is ready. In another terminal run:\n"
            "  sudo ovs-ofctl -O OpenFlow13 show s1\n"
            "  sudo ovs-ofctl -O OpenFlow13 dump-flows s1\n"
            '  sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"\n'
            '  sudo ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"\n'
            "Press ENTER here when finished to let the script continue.\n"
        )

    with open("result2.txt", "w") as out:
        out.write("Experiment 2: SDN (Layer 2) results\n")

        # Baseline ovs-ofctl info
        section(
            out, "ovs-ofctl show s1 (before)", s1.cmd("ovs-ofctl -O OpenFlow13 show s1")
        )
        section(
            out,
            "ovs-ofctl dump-flows s1 (before)",
            s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"),
        )

        # Baseline pings
        section(out, "Ping h1 -> h3 (before)", h1.cmd(f"ping -c 1 {h3.IP()}"))
        section(out, "Ping h2 -> h3 (before)", h2.cmd(f"ping -c 1 {h3.IP()}"))

        # Required flow rules
        drop_cmd = 'ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"'
        fwd_cmd = 'ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"'

        section(out, "Flow command (drop traffic from s1-eth2)", drop_cmd)
        section(out, "Flow command (forward s1-eth1 -> s1-eth3)", fwd_cmd)

        s1.cmd(drop_cmd)
        s1.cmd(fwd_cmd)

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
