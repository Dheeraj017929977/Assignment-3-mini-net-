#!/usr/bin/env python3
"""
Experiment 1: IP Routing
Creates a Mininet topology with hosts and routers, configures routing,
and tests connectivity with ping commands.
"""

from mininet.net import Mininet
from mininet.node import Node, Host
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import subprocess
import os
import sys


class LinuxRouter(Node):
    """A Node with IP forwarding enabled."""

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()


def createTopology():
    """Create the network topology with hosts and routers."""
    net = Mininet(link=TCLink)

    info("*** Adding hosts\n")
    # Add hosts with their IP addresses
    h1 = net.addHost("h1", ip="10.0.0.1/24")
    h2 = net.addHost("h2", ip="10.0.3.2/24")
    h3 = net.addHost("h3", ip="10.0.2.2/24")

    info("*** Adding routers\n")
    # Add routers
    r1 = net.addHost("r1", cls=LinuxRouter, ip="10.0.0.3/24")
    r2 = net.addHost("r2", cls=LinuxRouter, ip="10.0.1.2/24")

    info("*** Creating links\n")
    # Create links with IP addresses
    # h1 to r1
    net.addLink(
        h1,
        r1,
        intfName1="h1-eth0",
        intfName2="r1-eth0",
        params1={"ip": "10.0.0.1/24"},
        params2={"ip": "10.0.0.3/24"},
    )

    # h2 to r1
    net.addLink(
        h2,
        r1,
        intfName1="h2-eth0",
        intfName2="r1-eth2",
        params1={"ip": "10.0.3.2/24"},
        params2={"ip": "10.0.3.4/24"},
    )

    # r1 to r2
    net.addLink(
        r1,
        r2,
        intfName1="r1-eth1",
        intfName2="r2-eth0",
        params1={"ip": "10.0.1.1/24"},
        params2={"ip": "10.0.1.2/24"},
    )

    # r2 to h3
    net.addLink(
        r2,
        h3,
        intfName1="r2-eth1",
        intfName2="h3-eth0",
        params1={"ip": "10.0.2.1/24"},
        params2={"ip": "10.0.2.2/24"},
    )

    info("*** Starting network\n")
    net.start()

    return net


def configureRoutes(net):
    """Configure routing tables for all hosts."""
    info("*** Configuring routes\n")

    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")
    r1 = net.get("r1")
    r2 = net.get("r2")

    # Configure routes from h1 to h3
    # h1 -> r1 (default gateway)
    h1.cmd("ip route add default via 10.0.0.3")

    # Configure routes from h2 to h3
    # h2 -> r1 (default gateway)
    h2.cmd("ip route add default via 10.0.3.4")

    # Configure routes from h3 to h1 and h2
    # h3 -> r2 (default gateway)
    h3.cmd("ip route add default via 10.0.2.1")

    # Configure routes on r1
    # r1 needs to know how to reach h3 (via r2)
    r1.cmd("ip route add 10.0.2.0/24 via 10.0.1.2")

    # Configure routes on r2
    # r2 needs to know how to reach h1 and h2 (via r1)
    r2.cmd("ip route add 10.0.0.0/24 via 10.0.1.1")
    r2.cmd("ip route add 10.0.3.0/24 via 10.0.1.1")


def runPingTests(net):
    """Run ping tests and save results to result1.txt."""
    info("*** Running ping tests\n")

    h1 = net.get("h1")
    h2 = net.get("h2")
    h3 = net.get("h3")

    results = []
    results.append("=" * 60)
    results.append("Experiment 1: IP Routing - Ping Test Results")
    results.append("=" * 60)
    results.append("")

    # Ping from h1 to h3
    results.append("1. Ping from h1 to h3 (10.0.2.2):")
    results.append("-" * 60)
    ping_result = h1.cmd("ping -c 1 10.0.2.2")
    results.append(ping_result)
    results.append("")

    # Ping from h2 to h3
    results.append("2. Ping from h2 to h3 (10.0.2.2):")
    results.append("-" * 60)
    ping_result = h2.cmd("ping -c 1 10.0.2.2")
    results.append(ping_result)
    results.append("")

    # Ping from h3 to h1
    results.append("3. Ping from h3 to h1 (10.0.0.1):")
    results.append("-" * 60)
    ping_result = h3.cmd("ping -c 1 10.0.0.1")
    results.append(ping_result)
    results.append("")

    # Ping from h3 to h2
    results.append("4. Ping from h3 to h2 (10.0.3.2):")
    results.append("-" * 60)
    ping_result = h3.cmd("ping -c 1 10.0.3.2")
    results.append(ping_result)
    results.append("")

    # Write results to file
    with open("result1.txt", "w") as f:
        f.write("\n".join(results))

    info("*** Ping test results saved to result1.txt\n")


def main():
    """Main function to create topology, configure routes, and test."""
    setLogLevel("info")

    # Create topology
    net = createTopology()

    try:
        # Configure routes
        configureRoutes(net)

        # Run ping tests
        runPingTests(net)

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
