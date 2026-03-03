# STATE.md - Nchantrs

## Current State: Active Development

### Project
- **Name**: Nchantrs
- **Type**: Telegram bot framework
- **Branch**: morg-ws
- **Location**: /home/solubrew/.morg/workspace/projects/nchantrs

### Architecture

#### Core Components
- **NchantdStore**: Data storage layer (extends MicroStash -> SQuiRL)
- **GlainMixin**: Optional glain integration for agent memory
- **Models**: Nchantd model classes

#### Integration Chain
```
NchantdStore -> MicroStash -> SQuiRL
      |
      +-> GlainMixin (optional)
```

### Dependencies
- micromole
- squirl (via micromole)
- glain (optional)

### Features
| Feature | Status |
|---------|--------|
| NchantdStore | ✅ Stable |
| Glain tables | ✅ Implemented |
| Optional glain | ✅ Implemented |
| GlainMixin | ✅ Implemented |

### GitVein
- URL: file:///mnt/overse/SBST01/vein/GitVein/nchantrs.git
- Branch: morg-ws

### Last Updated
2026-03-03
