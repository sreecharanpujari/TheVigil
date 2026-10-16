"""
The Vigil — An experiment in digital impermanence.

A real-time anti-social media ledger where posts decay over time.
Reading heals. Typing kills.

Run:
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000
"""

import threading
import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO

# ═══════════════════════════════════════════════════════════════
#  App & SocketIO setup
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config["SECRET_KEY"] = "vigil-ephemeral"
socketio = SocketIO(app, async_mode="threading")

# ═══════════════════════════════════════════════════════════════
#  Configuration
# ═══════════════════════════════════════════════════════════════

DEFAULT_LIFESPAN = 60.0     # seconds a new post starts with
MAX_LIFESPAN     = 90.0     # ceiling for healing
HEAL_RATE        = 1.5      # +seconds restored per second of gaze
DECAY_RATE       = 1.0      # -seconds lost per second of neglect
NOISE_PENALTY    = 0.5      # -seconds lost per keystroke (all posts)
TICK_HZ          = 20       # internal simulation frequency
EMIT_HZ          = 10       # state broadcast frequency to clients

# ═══════════════════════════════════════════════════════════════
#  Shared State  (guarded by `lock`)
# ═══════════════════════════════════════════════════════════════

lock = threading.Lock()

posts: list[dict] = []          # [{id, text, life, maxLife}, ...]
post_id_seq: int  = 0
stats: dict       = {"decayed": 0, "healed": 0.0}
client_vis: dict  = {}          # sid -> set of visible post IDs

# ═══════════════════════════════════════════════════════════════
#  Routes
# ═══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")

# ═══════════════════════════════════════════════════════════════
#  SocketIO Event Handlers
# ═══════════════════════════════════════════════════════════════

@socketio.on("connect")
def on_connect():
    """Register a new client and send current state."""
    sid = request.sid
    with lock:
        client_vis[sid] = set()
        payload = _build_state()
    socketio.emit("state", payload, to=sid)


@socketio.on("disconnect")
def on_disconnect():
    """Clean up client visibility tracking."""
    with lock:
        client_vis.pop(request.sid, None)


@socketio.on("post")
def on_post(data):
    """Handle a new post submission."""
    global post_id_seq

    text = (data.get("text") or "").strip()
    if not text:
        return
    text = text[:500]

    with lock:
        post_id_seq += 1
        posts.insert(0, {
            "id":      post_id_seq,
            "text":    text,
            "life":    DEFAULT_LIFESPAN,
            "maxLife": DEFAULT_LIFESPAN,
        })


@socketio.on("keys")
def on_keys(data):
    """Handle batched keystroke entropy from a client."""
    count = int(data.get("n", 1))
    count = max(1, min(count, 50))          # cap to prevent abuse

    with lock:
        penalty = NOISE_PENALTY * count
        for p in posts:
            p["life"] = max(p["life"] - penalty, 0)


@socketio.on("vis")
def on_vis(data):
    """Update which posts a specific client can see."""
    ids = data.get("ids", [])
    with lock:
        client_vis[request.sid] = set(ids)

# ═══════════════════════════════════════════════════════════════
#  State Builder
# ═══════════════════════════════════════════════════════════════

def _build_state(dying_ids=None):
    """Serialize current state. Must be called under `lock`."""
    return {
        "posts": [
            {
                "id":      p["id"],
                "text":    p["text"],
                "life":    round(p["life"], 2),
                "maxLife": p["maxLife"],
            }
            for p in posts
        ],
        "dying":   dying_ids or [],
        "active":  len(posts),
        "decayed": stats["decayed"],
        "healed":  int(stats["healed"]),
    }

# ═══════════════════════════════════════════════════════════════
#  Core Game Loop  (background thread)
# ═══════════════════════════════════════════════════════════════

def game_loop():
    """
    Runs continuously at TICK_HZ.

    Each tick:
      - Heal posts that any connected client can see.
      - Decay posts that no client can see.
      - Remove posts whose lifespan reaches zero.
      - Broadcast state to all clients at EMIT_HZ.
    """
    last_tick = time.monotonic()
    last_emit = 0.0
    emit_interval = 1.0 / EMIT_HZ
    tick_interval  = 1.0 / TICK_HZ

    while True:
        socketio.sleep(tick_interval)

        now = time.monotonic()
        dt  = min(now - last_tick, 0.25)    # clamp large gaps (tab-away)
        last_tick = now

        with lock:
            # ── Aggregate visibility across all clients ──
            visible: set = set()
            for v in client_vis.values():
                visible.update(v)

            # ── Update every post ──
            dying: list[int] = []

            for p in posts:
                if p["id"] in visible:
                    # Healing — gaze restores life
                    p["life"] = min(p["life"] + HEAL_RATE * dt, MAX_LIFESPAN)
                    stats["healed"] += HEAL_RATE * dt
                else:
                    # Decay — silence erodes life
                    p["life"] = max(p["life"] - DECAY_RATE * dt, 0)

                if p["life"] <= 0:
                    dying.append(p["id"])

            # ── Reap dead posts ──
            if dying:
                dying_set = set(dying)
                posts[:] = [p for p in posts if p["id"] not in dying_set]
                stats["decayed"] += len(dying)

            # ── Broadcast (throttled) ──
            payload = None
            if now - last_emit >= emit_interval:
                payload = _build_state(dying)
                last_emit = now

        # Emit outside the lock
        if payload is not None:
            socketio.emit("state", payload)

# ═══════════════════════════════════════════════════════════════
#  Entry Point
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "127.0.0.1")

    socketio.start_background_task(game_loop)

    print()
    print("  +==========================================+")
    print("  |        T H E   V I G I L                 |")
    print("  |                                          |")
    print(f"  |   -> http://{host}:{port:<24}|")
    print("  |   Reading heals.  Typing kills.          |")
    print("  +==========================================+")
    print()

    socketio.run(
        app,
        host=host,
        port=port,
        debug=False,
        allow_unsafe_werkzeug=True,
    )
