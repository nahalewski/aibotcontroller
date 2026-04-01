# GamePilot AI

GamePilot AI is a cross-platform desktop system that allows an AI model to observe a PC game in real-time, decide actions, and control the game through a virtual input layer.

## Project Structure

- `app/`: Electron + React + TypeScript frontend.
- `runtime/`: Python backend (FastAPI + WebSockets).
- `config/`: Game profiles and local settings.

## Getting Started

### 1. Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **macOS**: Accessibility and Screen Recording permissions are required.
- **Windows**: [ViGEmBus](https://github.com/ViGEm/ViGEmBus) (for virtual controller support).

### 2. Backend Setup (Runtime)

```bash
cd runtime
pip install -r requirements.txt
# If on macOS, also install Quartz framework
pip install pyobjc-framework-Quartz pyobjc-framework-CoreGraphics
# If on Windows, install dxcam and vgamepad
# pip install dxcam vgamepad
python main.py
```

### 3. Frontend Setup (App)

```bash
cd app
npm install
npm run dev
```

## Features

- **Real-time Capture**: Observation of game windows at 10-20 FPS.
- **AI Policy**: Pluggable AI models (OpenAI-compatible) for decision making.
- **Virtual Input**: Low-level keyboard and mouse injection.
- **Technical Dashboard**: Live frame preview, telemetry, and logic logs.

## Safety & Controls

- **Emergency Stop**: Global button to kill the control loop.
- **Input Release**: Automatic release of all keys on shutdown.
- **Cooldowns**: Built-in rate limiting for AI actions.
