# Frameshock Framework

**A robust, modular penetration testing framework designed for real-world security assessments**

*Built by security professionals, for security professionals*

---

## Why Frameshock?

In the fast-evolving landscape of cybersecurity, penetration testers need tools that are **powerful**, **flexible**, and **scalable**. Frameshock delivers exactly that—a clean, modular framework that lets you focus on what matters: finding vulnerabilities and securing systems.

### The Problem We Solve

Traditional pentesting tools often force you to:
- Work with bloated frameworks loaded with modules you'll never use
- Manually manage multiple targets and sessions
- Switch between different tools for payload generation and exploitation
- Spend more time wrestling with tools than actually testing

**Frameshock changes that.**

---

## What Makes Frameshock Different

### 🎯 **Shodan Integration for Scale**
Automatically discover and target vulnerable systems at scale. Search, identify, and queue targets directly from Shodan's massive database. Perfect for red team exercises and large-scale assessments.

### 🔧 **Pick & Drop Modularity**
True modular architecture. Drop your custom exploits into the `Modules/` directory and they're instantly available. No configuration, no registration—just pure simplicity.

### 🎭 **Multi-Target, Multi-Session Management**
Built-in multithreading handles multiple victims simultaneously. Stable, secure, and designed for operations beyond the LAN.

### 🚀 **Complete Payload Arsenal**
- Generic reverse shells (sh, bash)
- Python-based reverse connections
- Full Meterpreter integration
- Cross-platform payload support

### 💾 **Intelligent Target Management**
SQLite-backed target database with filtering, categorization, and bulk operations. Never lose track of your scope again.

---

## Quick Start

### Prerequisites
```bash
# Requires root privileges for full functionality
sudo su
```

### Installation
```bash
git clone https://github.com/hdbreaker/Frameshock.git
cd Frameshock
chmod +x setup.sh
./setup.sh
```

### Basic Usage
```bash
python frameshock.py
```

### Essential Commands
```
show modules       → List available exploit modules
use shodan         → Search and queue targets via Shodan
set target         → Manually add targets
show targets       → Display current target list
set payload        → Configure reverse shell payload
start handler      → Launch multi-handler for sessions
```

---

## Framework Architecture

### Core Components

**🎯 Target Discovery**
- Shodan API integration for automated reconnaissance
- Manual target specification
- Bulk import capabilities

**🛠️ Modular Exploit System**
- Drop-in module support
- Automatic module detection
- Clean separation of concerns

**🔄 Session Management**
- Multithreaded payload handlers
- Session persistence
- Cross-platform compatibility

**💿 Data Persistence**
- SQLite database for target management
- Search and filter capabilities
- Audit trail maintenance

---

## Available Modules

Frameshock comes with battle-tested modules for common vulnerabilities:

- **QMAIL Shellshock Exploit**
- **SQL Injection with Bing Search**
- **AXIS Camera Credential Harvester**
- **Web Application Bot**
- **AXIS Camera Easy Credentials**

*Building your own modules? Drop them in `/Modules/` and they're ready to use.*

---

## Advanced Features

### Payload Customization
Generate payloads for multiple platforms and scenarios:
- Linux reverse shells (sh/bash)
- Python-based connections
- Windows compatibility
- Meterpreter integration

### Shodan-Powered Reconnaissance
```
use shodan
> wordpress vulnerability
Results found: 15,247
Pages: 152
Input number of pages to process: 5
```

Automatically queue thousands of potential targets based on your search criteria.

### Multi-Session Handling
Handle dozens of compromised systems simultaneously with Frameshock's built-in multi-handler, integrated directly with Metasploit's infrastructure.

---

## Use Cases

### Red Team Operations
- Large-scale target discovery and exploitation
- Automated vulnerability verification
- Multi-target campaign management

### Penetration Testing
- Systematic vulnerability assessment
- Payload testing and verification
- Session management and persistence

### Security Research
- 0-day exploitation testing
- Proof-of-concept development
- Vulnerability impact assessment

---

## Security Notice

⚠️ **Frameshock is designed for authorized security testing only.**

This framework should only be used against systems you own or have explicit permission to test. Unauthorized access to computer systems is illegal and unethical.

---

## Contributing

### Adding Modules
1. Create your exploit in Python
2. Follow the existing module structure
3. Drop it in `/Modules/` directory
4. It's automatically available in the framework

### Module Development Guidelines
- Clean, readable code
- Proper error handling
- Clear documentation
- English comments only

---

## Philosophy

**"Pick and Drop"** — We believe in simplicity. Take what you need, leave what you don't. Build your custom arsenal without the bloat.

**"Do It Yourself"** — Learn, create, and share. Combat script-kiddie culture with professional, educational tools.

**"Share Your Discoveries"** — The security community grows stronger when we collaborate and share knowledge.

---

## Support & Documentation

- **Framework Tutorial**: [Frameshock Unveiled](http://www.securitysignal.org/2015/02/frameshock-al-descubierto.html)
- **Issue Tracking**: Submit bugs and feature requests via GitHub Issues
- **Community**: Join discussions about module development and security research

---

## License & Credits

Frameshock is powered by **hdbreaker (Alejandro Parodi)**

*Built for the security community, by the security community.*

---

**Ready to level up your penetration testing game?**
*Clone, configure, and start discovering vulnerabilities at scale.*
