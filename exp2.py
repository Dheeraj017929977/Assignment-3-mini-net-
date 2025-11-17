#!/usr/bin/env python3
"""
Experiment 2 – SDN L2 forwarding demo.

Topology:
    h1 ---\
            s1 --- s2 --- h3
    h2 ---/

Requirements:
  • h1, h2, h3 share one L2 subnet.
  • s1 must drop everything arriving on port 2 (the h2 link).
  • s1 must forward traffic arriving on port 1 out port 3 (toward s2).
  • Capture ovs-ofctl output, ping tests (before/after), and flow commands.

This script intentionally avoids a controller binary by letting both
switches run in standalone/learning mode and then pushing rules via
ovs-ofctl.
"""

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.log import setLogLevel, info
import os
import time


def section(fh, title, data):
    """Pretty-print a labeled block into result2.txt."""
    fh.write(f"\n=== {title} ===\n")
    fh.write(data.strip() + "\n")


def main():
    net = Mininet(controller=None, link=TCLink, switch=OVSKernelSwitch)

    info("*** Building switches\n")
    s1 = net.addSwitch("s1", failMode="standalone", protocols="OpenFlow13")
    s2 = net.addSwitch("s2", failMode="standalone", protocols="OpenFlow13")

    info("*** Spawning hosts\n")
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.0.2/24")
    h3 = net.addHost("h3", ip="10.0.0.3/24")

    info("*** Wiring links (controls port numbers)\n")
    net.addLink(h1, s1)  # s1-eth1
    net.addLink(h2, s1)  # s1-eth2
    net.addLink(s1, s2)  # s1-eth3 <-> s2-eth1
    net.addLink(s2, h3)  # s2-eth2

    info("*** Starting Mininet\n")
    net.start()

    with open("result2.txt", "w") as out:
        out.write("Experiment 2: SDN (Layer 2) log\n")

        # Pause to allow running ovs-ofctl commands from another terminal window
        # as specified in the assignment requirements
        info("\n*** Network is running. You can now run the following commands\n")
        info("    from ANOTHER TERMINAL WINDOW:\n")
        info("    $ sudo ovs-ofctl -O OpenFlow13 show s1\n")
        info("    $ sudo ovs-ofctl -O OpenFlow13 dump-flows s1\n")
        info(
            "\n*** Waiting 5 seconds... (or run commands manually from another terminal)\n"
        )
        time.sleep(5)  # Give user time to run commands from another terminal

        # Capture the commands automatically (they will also work from another terminal)
        info("*** Capturing ovs-ofctl show and dump-flows output...\n")
        section(
            out, "ovs-ofctl show s1 (before)", s1.cmd("ovs-ofctl -O OpenFlow13 show s1")
        )
        section(
            out,
            "ovs-ofctl dump-flows s1 (before)",
            s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"),
        )

        section(out, "Ping h1 → h3 (before)", h1.cmd(f"ping -c 1 {h3.IP()}"))
        section(out, "Ping h2 → h3 (before)", h2.cmd(f"ping -c 1 {h3.IP()}"))

        drop_cmd = 'ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=2,actions=drop"'
        fwd_cmd = 'ovs-ofctl -O OpenFlow13 add-flow s1 "in_port=1,actions=output:3"'

        section(out, "Flow command: drop traffic from s1-eth2", drop_cmd)
        section(out, "Flow command: forward s1-eth1 → s1-eth3", fwd_cmd)

        s1.cmd(drop_cmd)
        s1.cmd(fwd_cmd)

        section(
            out,
            "ovs-ofctl dump-flows s1 (after)",
            s1.cmd("ovs-ofctl -O OpenFlow13 dump-flows s1"),
        )

        section(out, "Ping h1 → h3 (after)", h1.cmd(f"ping -c 1 {h3.IP()}"))
        section(out, "Ping h2 → h3 (after)", h2.cmd(f"ping -c 1 {h3.IP()}"))

    info("*** Finished. See result2.txt for details.\n")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    main()
