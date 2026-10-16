# The Vigil

> An experimental, anti-social media platform built on the concept of digital impermanence.

Unlike traditional networks that reward endless scrolling, likes, and permanent noise, **The Vigil** treats digital thoughts as fragile entities that must be actively protected through silent attention.

---

### Core Mechanics & Capabilities

* **Ephemeral Time-Capsules (The Timer):** Every message deposited into the ledger begins with a strict countdown timer (60 seconds). Once a post's timer reaches zero, it is permanently purged from the system and the interface without any backups or archives.
* **Gaze-Powered Sustenance (The Healing Mechanic):** The platform utilizes viewport tracking (`IntersectionObserver`) to detect what the user is actively reading. If a user holds a post on their screen in complete silence, this passive attention acts as a shield. It freezes the decay timer and slowly regenerates the post's lifespan (+1.5s/s).
* **Global Entropy Penalty (The Destruction Mechanic):** Interaction is punished rather than rewarded. Anytime a user begins typing to deposit a new thought, their keystrokes generate "noise." This noise triggers a global penalty, instantly draining the lifespan of every other active post currently on the ledger (-0.5s per keystroke).
* **Procedural Visual Decay (The Glitch Effect):** As a post loses its lifespan, it visually degrades to reflect its dying state:
  * **100% – 50% Lifespan**: High-contrast, pristine text.
  * **49% – 20% Lifespan**: Progressive optical blur and opacity fade.
  * **19% – 0% Lifespan**: Text corruption into unreadable unicode glyphs (`█`, `░`, `▒`, `▓`, `~`). When healed back above 20%, clean text is restored!

---

### The User Experience

* **Zero Vanity Metrics:** There are no likes, follower counts, share buttons, or comment threads. The only metric is the survival integrity (time remaining) of a thought.
* **Minimalist Interface:** Designed with a stark, dark-mode terminal aesthetic (`#0a0a0c`, `#38bdf8`, `#ef4444`). This emphasizes the text itself and the color-coded progress bars (shifting from Blue &rarr; Yellow &rarr; Red) that indicate the health of each capsule.
* **Collective Responsibility:** The mechanics force a cooperative dilemma. Users must decide whether their desire to speak (type a new post) is worth actively destroying the thoughts others have left behind, fostering a highly intentional, quiet, and mindful digital environment.

---

### Deployment (Streamlit Cloud via GitHub)

1. Commit and push these updated files to your GitHub repository:
   - `app.py`
   - `index.html`
   - `requirements.txt`
   - `README.md`
2. In your Streamlit Cloud tab, open **`< Manage app`** in the bottom-right &rarr; click **⋮** &rarr; **Reboot app**.

---

### Run Locally

```bash
python app.py
```
Starts a local server and opens **http://localhost:5000** in your browser.
