# The Vigil

> An experiment in digital impermanence.

**The Vigil** is an anti-social media ledger where posts are living entities that decay over time. Silence keeps them alive. Noise destroys them.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Core Mechanics

| Mechanic | How it works |
|---|---|
| **Time-Bombed Posts** | Every post starts with a 60-second lifespan. A server-side game loop ticks down every post by 1 second per second. Lifespan hits 0 → post is permanently deleted. |
| **Gaze Tracking (Healing)** | `IntersectionObserver` tracks if a post is visible in your viewport. If you're reading it, its timer freezes and restores **+1.5s per second**, up to a 90s ceiling. |
| **Entropy (Destruction)** | Every keystroke in the composer subtracts **0.5s from every living post**. The more you type, the faster everything dies. |
| **Visual Decay** | **100–50%**: pristine. **49–20%**: progressive CSS blur + opacity fade. **Below 20%**: characters randomly replaced with glitch glyphs (`█░▒▓~`). |

## Architecture

```
┌─────────────────────────────────┐
│  Python Server  (app.py)        │
│  Flask + SocketIO               │
│                                 │
│  • Game loop (20 Hz thread)     │
│  • All state lives here         │
│  • Broadcasts at 10 Hz          │
├─────────────────────────────────┤
│         WebSocket (SocketIO)    │
├─────────────────────────────────┤
│  Browser Client                 │
│  (templates/index.html)         │
│                                 │
│  • Thin rendering layer         │
│  • IntersectionObserver → vis   │
│  • Keystroke batching → entropy │
│  • Visual decay effects         │
└─────────────────────────────────┘
```

Multiple browser tabs share the same living feed — the Python server is the single source of truth.

## Quick Start

### Prerequisites

- Python 3.10+

### Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Vigil.git
cd Vigil

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

## Deployment

### Render (Recommended — Free Tier)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → **New** → **Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` — click **Deploy**

Or use the blueprint button:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Railway

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Railway auto-detects the `Dockerfile`
4. Set environment variable: `PORT=5000`, `HOST=0.0.0.0`

### Docker

```bash
docker build -t the-vigil .
docker run -p 5000:5000 the-vigil
```

### Heroku

```bash
heroku create the-vigil
git push heroku main
```

## Project Structure

```
Vigil/
├── app.py                  # Flask + SocketIO server, game loop, all state
├── templates/
│   └── index.html          # Frontend (HTML + CSS + JS client)
├── requirements.txt        # Python dependencies
├── Procfile                # Heroku / Render start command
├── Dockerfile              # Container deployment
├── render.yaml             # Render.com one-click blueprint
├── runtime.txt             # Python version pin
├── .gitignore
├── LICENSE
└── README.md
```

## Configuration

Tweak constants in `app.py`:

| Variable | Default | Description |
|---|---|---|
| `DEFAULT_LIFESPAN` | `60.0` | Seconds a new post starts with |
| `MAX_LIFESPAN` | `90.0` | Healing ceiling |
| `HEAL_RATE` | `1.5` | Seconds restored per second of gaze |
| `DECAY_RATE` | `1.0` | Seconds lost per second of neglect |
| `NOISE_PENALTY` | `0.5` | Seconds lost per keystroke (all posts) |

## Tech Stack

- **Backend**: Python, Flask, Flask-SocketIO
- **Transport**: WebSocket via Socket.IO
- **Frontend**: Vanilla HTML/CSS/JS (no framework)
- **Real-time**: Server-side game loop at 20 Hz, state broadcast at 10 Hz

## License

[MIT](LICENSE)

