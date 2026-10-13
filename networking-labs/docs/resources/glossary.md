# Networking Glossary for DevOps

Key networking terms explained in DevOps context.

## A

**ARP (Address Resolution Protocol)**
: Maps IP addresses to MAC addresses on a local network. When your container wants to talk to another container on the same network, ARP finds the physical address.

**AS (Autonomous System)**
: A collection of networks under a single administrative domain. Cloud providers, enterprises, and ISPs each have their own AS numbers. Used in BGP routing.

**ASN (Autonomous System Number)**
: Unique identifier for an AS. Example: AS7224 (Amazon), AS8075 (Microsoft).

## B

**BGP (Border Gateway Protocol)**
: The routing protocol that runs the internet. In data centers, eBGP is used for spine-leaf connectivity. Critical for multi-cloud and hybrid architectures.

**Bridge (Docker)**
: Default Docker network driver. Creates a virtual switch connecting containers. Like plugging containers into the same switch.

**Broadcast Domain**
: Network segment where all devices receive each other's broadcast traffic. VLANs separate broadcast domains.

## C

**CIDR (Classless Inter-Domain Routing)**
: Modern IP addressing notation. `10.0.0.0/24` means 256 addresses (10.0.0.0-10.0.0.255). `/24` = 256 IPs, `/16` = 65,536 IPs.

**CNI (Container Network Interface)**
: Standard for container networking in Kubernetes. Plugins like Calico, Cilium, and Flannel implement CNI.

## D

**DHCP (Dynamic Host Configuration Protocol)**
: Automatically assigns IP addresses. Your containers often get IPs from Docker's DHCP-like functionality.

**DNS (Domain Name System)**
: Translates names to IP addresses. `kubernetes.io` → `147.75.40.148`. Docker provides internal DNS for container name resolution.

## E

**eBGP (External BGP)**
: BGP between different autonomous systems. In spine-leaf, each switch is often its own AS, so eBGP connects them.

**ECMP (Equal-Cost Multi-Path)**
: Load balances traffic across multiple equal paths. Critical for spine-leaf performance.

**Encapsulation**
: Wrapping packets in additional headers. VXLAN encapsulates L2 frames in L3 packets for transport across networks.

**EVPN (Ethernet VPN)**
: Control plane for VXLAN in data centers. Distributes MAC/IP information via BGP. Modern DC fabrics use EVPN-VXLAN.

## F

**Fabric**
: Network infrastructure as a unified system. "Data center fabric" refers to the complete spine-leaf network.

**Firewall**
: Filters traffic based on rules. Kubernetes NetworkPolicies are essentially firewall rules for pods.

**FRRouting (FRR)**
: Open-source routing suite for Linux. Supports BGP, OSPF, IS-IS. Used in many virtual network devices.

## G

**Gateway**
: Router connecting different networks. Your default gateway routes traffic to the internet.

## H

**Host Network (Docker)**
: Container uses host's network stack directly. No network isolation but better performance.

## I

**iBGP (Internal BGP)**
: BGP within the same AS. Used for route distribution within a single organization.

**ICMP (Internet Control Message Protocol)**
: Protocol for network diagnostics. `ping` and `traceroute` use ICMP.

**Interface**
: Network connection point. `eth0`, `ens192`, `ethernet-1/1` are interface names.

## J

**Jitter**
: Variation in packet delay. Important for real-time applications (voice, video).

## L

**L2 (Layer 2)**
: Data link layer. MAC addresses, switches, VLANs. "L2 network" means devices are in the same broadcast domain.

**L3 (Layer 3)**
: Network layer. IP addresses, routers, routing. "L3 network" means traffic is routed.

**Latency**
: Time for a packet to travel from source to destination. Measured in milliseconds.

**Leaf (Spine-Leaf)**
: Access layer switches in spine-leaf architecture. Servers/pods connect to leafs. Leafs connect to spines.

**Loopback**
: Virtual interface (`lo`) always up. IP `127.0.0.1`. Used for router IDs in routing protocols.

## M

**MAC Address**
: Hardware address of a network interface. Format: `00:1A:2B:3C:4D:5E`. Unique per interface.

**MTU (Maximum Transmission Unit)**
: Largest packet size for a network path. Default: 1500 bytes. VXLAN needs larger MTU (1550+) to avoid fragmentation.

**Multicast**
: One-to-many communication. Efficient for sending same data to multiple receivers.

## N

**NAT (Network Address Translation)**
: Maps private IPs to public IPs. Docker uses NAT for containers to reach the internet.

**Network Namespace**
: Linux isolation mechanism for networking. Each container has its own network namespace with separate interfaces, routes, and iptables.

**NIC (Network Interface Card)**
: Physical network hardware. Virtual NICs (vNIC) are software implementations.

## O

**OSI Model**
: 7-layer networking reference model. DevOps most commonly works with L2 (Ethernet), L3 (IP), L4 (TCP/UDP), L7 (HTTP).

**OSPF (Open Shortest Path First)**
: Interior routing protocol. Common in enterprise networks. Less common in cloud-native environments (BGP preferred).

**Overlay Network**
: Virtual network built on top of physical network. VXLAN, Docker overlay networks, and Kubernetes pod networks are overlays.

## P

**Packet**
: Unit of data transmission. Contains headers (addressing info) and payload (data).

**Peering**
: Direct connection between networks. BGP peering establishes neighbor relationships.

**Port (Network)**
: Endpoint for communication. HTTP: 80, HTTPS: 443, SSH: 22. Containers expose ports for services.

**Prefix**
: IP network address in CIDR notation. `10.0.0.0/24` is a /24 prefix.

## R

**Route**
: Path for traffic to reach a destination. Contains: destination, next-hop, interface.

**Route Table**
: Collection of routes. Traffic lookup happens here to determine where to send packets.

**Router**
: Device that forwards packets between networks. Makes decisions based on routing table.

## S

**Spine (Spine-Leaf)**
: Aggregation layer switches. Every leaf connects to every spine. Provides ECMP and redundancy.

**Subnet**
: Subdivision of a network. `10.0.1.0/24` and `10.0.2.0/24` are subnets of `10.0.0.0/16`.

**Switch**
: L2 device connecting devices in same broadcast domain. Forwards based on MAC addresses.

## T

**TCP (Transmission Control Protocol)**
: Reliable, connection-oriented protocol. Most HTTP traffic uses TCP.

**TTL (Time to Live)**
: Packet hop limit. Decremented at each router. Prevents infinite loops. Traceroute exploits TTL.

## U

**UDP (User Datagram Protocol)**
: Fast, connectionless protocol. No delivery guarantee. DNS, DHCP, and VXLAN use UDP.

**Underlay**
: Physical network infrastructure. The overlay runs on top of the underlay.

## V

**VLAN (Virtual LAN)**
: Logical network segmentation at L2. VLAN 100 and VLAN 200 are isolated even on same switch.

**VNI (VXLAN Network Identifier)**
: VXLAN equivalent of VLAN ID. 24-bit field allows 16 million segments vs VLAN's 4096.

**VPC (Virtual Private Cloud)**
: Isolated cloud network. AWS VPC, Azure VNet, GCP VPC are the same concept.

**VRF (Virtual Routing and Forwarding)**
: Multiple routing tables on one device. Network equivalent of virtualization.

**VTEP (VXLAN Tunnel Endpoint)**
: Device that encapsulates/decapsulates VXLAN. Leafs are VTEPs in EVPN-VXLAN.

**VXLAN (Virtual Extensible LAN)**
: Overlay technology for data centers. Encapsulates L2 in L3 (UDP port 4789).

## W

**WAN (Wide Area Network)**
: Network spanning large geographic area. Connects data centers, branch offices, cloud.

## X

**XDP (eXpress Data Path)**
: High-performance Linux packet processing. Used by Cilium for fast networking.

---

## Quick Reference: OSI Layers

| Layer | Name | Protocols | Devices | DevOps Relevance |
|-------|------|-----------|---------|------------------|
| 7 | Application | HTTP, DNS, SSH | - | Service endpoints |
| 4 | Transport | TCP, UDP | - | Port numbers, load balancing |
| 3 | Network | IP, ICMP, BGP | Router | IP addressing, routing |
| 2 | Data Link | Ethernet, VLAN | Switch | MAC addresses, VLANs |
| 1 | Physical | - | NIC, Cable | Hardware connectivity |

## Quick Reference: Common Ports

| Port | Service | Protocol |
|------|---------|----------|
| 22 | SSH | TCP |
| 53 | DNS | UDP/TCP |
| 80 | HTTP | TCP |
| 443 | HTTPS | TCP |
| 179 | BGP | TCP |
| 4789 | VXLAN | UDP |
| 6443 | Kubernetes API | TCP |
