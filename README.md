# The Vigil

> An experiment in digital impermanence.

**The Vigil** is an autonomous anti-social media ledger based on digital impermanence. Thoughts are living entities that decay over time. Silence and focused gaze sustain them; voices, noise, typing, and tab-switching burn them away.

---

## Core Mechanics

| Mechanic | Implementation & Severity |
|---|---|
| **Accelerated Lifespan** | Every new post starts with a **30.0s** lifespan (decreased from 60s for intense impermanence). Reaching 0s permanently destroys the post. |
| **Acoustic Surveillance** | Uses the **Web Audio API** and real-time RMS frequency analysis. If ambient voices, talking, or loud noises are detected, a voice breach triggers, inflicting **-1.5s immediately to every post**. |
| **Cognitive Attention Lock** | Uses `Page Visibility API` and `window.blur`. If you switch to another app (Discord, WhatsApp, browser tabs), an **Abandonment Breach** engages, burning **-4.0s per second** from all posts until focus returns. |
| **Typing Entropy** | Every character typed into the composer area penalizes **all posts by -0.8s**, triggering a red vignette alert. |
| **Gaze Tracking (Healing)** | Looking steadily at a post (&ge; 60% in viewport) freezes decay and restores **+1.5s per second** up to a 50s ceiling. |
| **Procedural Visual Decay** | &bull; **100%–50%**: Crisp monospace text.<br>&bull; **49%–20%**: Progressive CSS `blur()` and opacity fade.<br>&bull; **19%–0%**: Procedural text corruption replacing characters with unicode glitch glyphs (`█`, `░`, `▒`, `▓`, `~`, `¤`, `∆`). When healed back above 20%, clean text is restored! |
| **Telemetry HUD** | Real-time decibel VU meter, Attention Lock monitor, and Gaze counter. |

---

## How to Deploy to GitHub (Option A: Streamlit Cloud)

1. Open your repository on GitHub.
2. Click **Add file** &rarr; **Upload files**.
3. Upload the updated files:
   - `app.py`
   - `index.html`
   - `requirements.txt`
   - `README.md`
4. Click **Commit changes**.
5. Return to your Streamlit Cloud tab &rarr; click **`< Manage app`** in the bottom-right corner &rarr; click the three vertical dots **(⋮)** &rarr; **Reboot app**.

---

## Run Locally

```bash
python app.py
```
Starts a local server and opens **http://localhost:5000** in your browser.

## Tech Stack

- **Backend**: Python, Streamlit (Streamlit Community Cloud deployment runner)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **APIs**: Web Audio API (Acoustic Analyser), IntersectionObserver (Gaze), Page Visibility API (Focus Lock)
- **Design**: Bespoke dark laboratory terminal (`#070709`, `#38bdf8`, `#ef4444`)

## License

MIT License. Free to use and distribute.
