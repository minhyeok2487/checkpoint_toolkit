# CheckPoint Toolkit v3.4 (Stable)

**CheckPoint Firewall Management Tool for Hyundai AutoEver Security Team**

A Windows GUI application for bulk registration and management of objects and policies using the CheckPoint Management API.

---

## 📋 Table of Contents

1. [Key Features](#key-features)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Getting Started](#getting-started)
5. [Detailed Feature Guide](#detailed-feature-guide)
   - [Bulk Import](#1-bulk-import)
   - [Bulk Policy](#2-bulk-policy)
   - [Zone Policy](#3-zone-policy)
6. [CSV File Formats](#csv-file-formats)
7. [Troubleshooting](#troubleshooting)
8. [Version History](#version-history)

---

## Key Features

### 📦 Bulk Import
- Mass object registration via CSV files
- Supported object types: Host, Network, Range, Group
- Real-time progress monitoring
- Test mode support (validation without actual registration)

### 📋 Bulk Policy
- Mass Access Rule creation via CSV files
- Multiple source/destination/service support (semicolon-separated)
- Automatic section creation
- Automatic creation of missing objects (as groups)

### 🔐 Zone Policy
- Automated zone-based policy generation (Hyundai AutoEver specific)
- DMZ/INT type support
- Environment-specific generation (prd/dev/stg)
- Automatic Inbound/Outbound rule configuration
- Automatic Inline Layer creation

---

## System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **CheckPoint Version**: R80.10 or higher (Management API support required)
- **Network**: Access to CheckPoint Management Server
- **Python**: 3.8 or higher (for source execution)

---

## Installation

### Method 1: Executable File (Recommended)

1. Copy `checkpoint_toolkit.exe` to your desired folder
2. Double-click to run

### Method 2: Python Source Execution

```bash
# 1. Install required packages
pip install customtkinter requests

# 2. Run
python main.py
```

### Method 3: Build from Source

```bash
# Run build.bat or
pyinstaller --onefile --windowed --name checkpoint_toolkit main.py
```

---

## Getting Started

### 1. Launch Application

When you run the program, you'll see the following interface:

```
┌─────────────────────────────────────────────────────────┐
│  CheckPoint Toolkit v3.4         [☀️/🌙] [🇰🇷/🇺🇸]      │
├─────────────────────────────────────────────────────────┤
│  Server: [________________] Port: [443]                  │
│  Username: [____________] Password: [********]           │
│  Domain: [____________] (Optional)                       │
│                                    [🔗 Connect] [🔓 Disc]│
├─────────────────────────────────────────────────────────┤
│ ┌──────────┐ ┌──────────────────────┐ ┌───────────────┐ │
│ │ 📦 Bulk   │ │                      │ │  Log Panel    │ │
│ │ 📋 Policy │ │     Work Area        │ │               │ │
│ │ 🔐 Zone   │ │                      │ │               │ │
│ └──────────┘ └──────────────────────┘ └───────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2. Connect to Server

1. Enter **Server Address** (e.g., `192.168.1.100` or `mgmt.example.com`)
2. Enter **Port** (default: `443`)
3. Enter **Username** (CheckPoint administrator account)
4. Enter **Password**
5. Enter **Domain** (only for MDS environment, leave empty for single SMS)
6. Click **[🔗 Connect]** button

> 💡 Connection settings are automatically saved for next session.

### 3. Change Theme and Language

- **☀️/🌙 Button**: Toggle Light/Dark theme
- **🇰🇷/🇺🇸 Button**: Toggle Korean/English language

---

## Detailed Feature Guide

### 1. Bulk Import

Register Host, Network, Range, and Group objects in bulk via CSV files.

#### How to Use

1. Click **[📦 Bulk Import]** in the left menu
2. Click **[Load CSV]** button to select CSV file
3. Review and edit data in the table
4. Configure options:
   - ☑️ **Test Mode**: Validate only without actual registration
   - ☑️ **Auto Publish**: Automatically publish after completion
5. Click **[▶ Run]** button

#### CSV Format

```csv
type,name,ip,subnet,range_start,range_end,members,color,comments
host,web-server-01,192.168.1.10,,,,,blue,Web Server 1
host,web-server-02,192.168.1.11,,,,,blue,Web Server 2
network,internal-net,,192.168.0.0,255.255.0.0,,,green,Internal Network
range,dhcp-pool,,,192.168.100.1,192.168.100.254,,yellow,DHCP Pool
group,web-servers,,,,,web-server-01;web-server-02,red,Web Server Group
```

| Column | Required | Description |
|--------|:--------:|-------------|
| type | ✅ | One of `host`, `network`, `range`, `group` |
| name | ✅ | Object name (must be unique) |
| ip | △ | IP address (required for host, network address for network) |
| subnet | △ | Subnet mask (network only) |
| range_start | △ | Range start IP (range only) |
| range_end | △ | Range end IP (range only) |
| members | △ | Group members (semicolon-separated, group only) |
| color | - | Color (blue, green, red, yellow, etc.) |
| comments | - | Description |

---

### 2. Bulk Policy

Create Access Rules in bulk via CSV files.

#### Prerequisites (Important!)

⚠️ **Check before creating rules:**

1. **Register Objects First**: Source/destination objects must be **registered first in Bulk Import tab**!
   - Or use "Auto Object" option to create empty groups automatically.
   
2. **Service Names Must Match Exactly**: Services must **exactly match existing names** in CheckPoint!
   - Built-in: `http`, `https`, `ssh`, `telnet`, `ftp`, `Any`, etc.
   - Custom services: **Create in SmartConsole first**, then use the **exact same name**
   - **Services are NOT auto-created!**
   - Case-sensitive (e.g., `MSSQL` ≠ `mssql`)

#### How to Use

1. Click **[📋 Bulk Policy]** in the left menu
2. Enter **Package Name** (e.g., `Standard`)
3. Enter **Layer Name** (leave empty for auto-detection)
4. Click **[Verify]** button to confirm package exists
5. Click **[Load CSV]** button to select CSV file
6. Configure options:
   - ☑️ **Auto Object**: Create missing objects as empty groups
   - ☑️ **Test Mode**: Validate only without actual creation
   - ☑️ **Auto Publish**: Automatically publish after completion
7. Click **[▶ Generate]** button
8. Enter **Insert Position** (rule number or empty for bottom)

#### CSV Format

```csv
name,source,destination,service,action,track,comments
allow-web,web-servers,app-servers,http;https,Accept,Log,Allow web traffic
allow-db,app-servers,db-servers,MSSQL,Accept,Log,Allow DB access
deny-all,Any,db-servers,Any,Drop,Log,Block remaining
```

| Column | Required | Description |
|--------|:--------:|-------------|
| name | ✅ | Rule name |
| source | ✅ | Source object (semicolon for multiple) |
| destination | ✅ | Destination object (semicolon for multiple) |
| service | ✅ | Service (semicolon for multiple) |
| action | ✅ | One of `Accept`, `Drop`, `Reject` |
| track | - | `Log`, `None`, `Detailed Log`, `Extended Log` |
| comments | - | Rule description |

#### Multiple Values Example

```csv
name,source,destination,service,action,track,comments
multi-rule,src1;src2;src3,dst1;dst2,http;https;ssh,Accept,Log,Multiple src/dst/svc
```

---

### 3. Zone Policy

Automatically generate zone-based policies (Hyundai AutoEver specific).

#### How to Use

1. Click **[🔐 Zone Policy]** in the left menu
2. Enter **Package Name** (e.g., `Standard`)
3. Click **[Verify]** button to confirm package exists
4. Configure Zone settings:
   - **Base Name**: System name (e.g., `CCS`, `APP`, `WEB`)
   - **Zone Type**: Select `DMZ` or `INT`
   - **Environment**: Select `prd`, `dev`, `stg` (multiple selection allowed)
5. Click **[Preview]** button to review policies to be created
6. Click **[▶ Generate]** button
7. Enter **Inbound Position** (Cleanup Rule number)
8. Choose whether to **Publish** after Inbound creation
9. Enter **Outbound Position**
10. Choose whether to **Publish** after Outbound creation

#### Generated Structure

**Example: Base Name = `CCS`, Type = `DMZ`, Environment = `prd`, `dev`**

```
Generated Security Zones:
├── internet_DMZ (Source Zone)
├── gs_dc_dmz (Source Zone)
├── ccs_dmz_prd (Target Zone)
└── ccs_dmz_dev (Target Zone)

CCS_Inbound Section:
├── internet_DMZ → ccs_dmz_prd (Inline Layer: internet_to_ccs_dmz_prd)
├── internet_DMZ → ccs_dmz_dev (Inline Layer: internet_to_ccs_dmz_dev)
├── gs_dc_dmz → ccs_dmz_prd (Inline Layer: gs_dc_dmz_to_ccs_dmz_prd)
├── gs_dc_dmz → ccs_dmz_dev (Inline Layer: gs_dc_dmz_to_ccs_dmz_dev)
├── Any(Neg) → ccs_dmz_prd (Inline Layer: any_to_ccs_dmz_prd)
└── Any(Neg) → ccs_dmz_dev (Inline Layer: any_to_ccs_dmz_dev)

CCS_Outbound Section:
├── ccs_dmz_prd → internet_DMZ (Inline Layer: ccs_dmz_prd_to_internet)
├── ccs_dmz_dev → internet_DMZ (Inline Layer: ccs_dmz_dev_to_internet)
├── ccs_dmz_prd → gs_dc_dmz (Inline Layer: ccs_dmz_prd_to_gs_dc_dmz)
├── ccs_dmz_dev → gs_dc_dmz (Inline Layer: ccs_dmz_dev_to_gs_dc_dmz)
├── ccs_dmz_prd → Any(Neg) (Inline Layer: ccs_dmz_prd_to_any)
└── ccs_dmz_dev → Any(Neg) (Inline Layer: ccs_dmz_dev_to_any)
```

#### Source Zones by Type

| Type | Source Zone 1 | Source Zone 2 |
|:----:|---------------|---------------|
| DMZ | internet_DMZ | gs_dc_dmz |
| INT | internet_INT | gs_dc_int |

---

## CSV File Formats

### File Encoding

- **UTF-8** encoding recommended
- When saving from Excel: Select "CSV UTF-8 (Comma delimited)"

### Download Templates

Click the **[Template]** button in each feature to generate sample CSV files.

### Creating CSV from Excel

1. Create data in Excel
2. **File → Save As**
3. File type: **CSV UTF-8 (Comma delimited) (*.csv)**
4. Save

---

## Troubleshooting

### Connection Errors

| Error Message | Cause | Solution |
|---------------|-------|----------|
| Connection refused | Server inaccessible | Check network, verify firewall port |
| Authentication failed | Auth failure | Verify username/password |
| SSL Error | Certificate error | Ignored (self-signed certificates allowed) |
| Domain not found | Domain error | Verify domain name (MDS environment) |

### Object Registration Errors

| Error Message | Cause | Solution |
|---------------|-------|----------|
| Object already exists | Duplicate name | Use different name or delete existing |
| Invalid IP address | IP format error | Check IP address format |
| Invalid subnet mask | Subnet error | Check subnet mask format |

### Policy Creation Errors

| Error Message | Cause | Solution |
|---------------|-------|----------|
| Package not found | Package missing | Verify package name |
| Layer not found | Layer missing | Verify layer name |
| Service not found | Service missing | Register service in CheckPoint |
| Object not found | Object missing | Use auto object creation option |

### Publish Errors

| Error Message | Cause | Solution |
|---------------|-------|----------|
| Publish failed | Publish failure | Check conflicts, manually publish in SmartConsole |
| Session locked | Session locked | Close other sessions and retry |

---

## Version History

### v3.4 (2026-01-23) - Stable
- 🎉 **Zone Policy generation logic stabilized**
- 🔧 Using section name-based `position.below` (same as shell script)
- 🔧 Rule positioning by section name instead of section UID
- 🔧 Unified Track type to Log
- 🔧 Application Site default category auto-set (`Custom_Application_Site`)
- 📋 CSV files compatible with mgmt_cli batch mode

### v3.3 (2026-01-22)
- ✨ Added Bulk Policy generation (CSV-based)
- ✨ Separated Zone Policy tab
- 🔧 Increased log panel font size (10pt → 12pt)
- 🔧 Increased log panel width (320 → 400)

### v3.2 (2026-01-22)
- ✨ Added Dark/Light theme toggle
- ✨ Added Korean/English language toggle
- 🔧 Theme setting persistence

### v3.1 (2026-01-22)
- ✨ Added sidebar navigation
- ✨ Modular refactoring (7 separate files)
- 🔧 Layout optimization

### v3.0 (2026-01-22)
- ✨ Modern UI based on CustomTkinter
- ✨ Hyundai AutoEver brand colors applied

### v2.x (2026-01-22)
- CSV editing feature
- Zone Policy generation feature
- Bug fixes

### v1.0 (2026-01-22)
- Initial version
- Bulk object registration feature

---

## mgmt_cli Batch Mode Compatibility

Object CSV files from this tool are compatible with CheckPoint `mgmt_cli` batch mode.

### Usage

```bash
# Login
mgmt_cli login user admin password *** > session.txt

# Add Hosts
mgmt_cli -s session.txt add host --batch hosts.csv

# Add Networks
mgmt_cli -s session.txt add network --batch networks.csv

# Add Service-TCP
mgmt_cli -s session.txt add service-tcp --batch services.csv

# Add Access Rules
mgmt_cli -s session.txt add access-rule --batch policy.csv

# Publish
mgmt_cli -s session.txt publish

# Logout
mgmt_cli -s session.txt logout
```

### Policy CSV Format (for mgmt_cli)

| Column | Description | Example | Notes |
|:------:|-------------|---------|-------|
| layer | Policy package layer | test Network | Package name + " Network" |
| position | Rule position | top, bottom | Or above/below + section name |
| name | Rule name | web-to-db | Must be unique |
| source | Source | web-server, Any | Multiple: source.1, source.2 |
| destination | Destination | db-server, Any | Multiple: destination.1, destination.2 |
| service | Service | https, Any | Multiple: service.1, service.2 |
| action | Action | Accept, Drop | |
| track.type | Logging | Log, None | |
| comments | Description | Web traffic | Optional |

### Multiple Values (mgmt_cli)

```csv
layer,position,name,source.1,source.2,destination,service.1,service.2,action,track.type
test Network,bottom,multi-rule,host-1,host-2,db-server,https,ssh,Accept,Log
```

> ⚠️ **Note**: GUI tool uses semicolon (`;`) separator, mgmt_cli uses index (`.1`, `.2`) method

---

## Support

Hyundai AutoEver Security Team

---

## License

This software was developed for internal use at Hyundai AutoEver.
