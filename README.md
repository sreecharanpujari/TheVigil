# The Vigil

> An experiment in digital impermanence.

**The Vigil** is an anti-social media ledger based on digital impermanence. Posts are not permanent; they are living entities that decay over time. Silence keeps them alive; noise actively destroys them.

---

## Core Mechanics

| Mechanic | How it Works |
|---|---|
| **Time-Bombed Posts** | Every new post starts with a **60.0s** lifespan. A 20Hz game loop ticks down each post by 1s/s. When it reaches 0s, it is permanently deleted from DOM and memory. |
| **Gaze Tracking (Healing)** | `IntersectionObserver` monitors if a post is &ge; 60% in your viewport. When looked at, decay is frozen and its lifespan is restored at **+1.5s per second** (up to 90s). |
| **Entropy (Destruction)** | Keystrokes in the composer area trigger a noise penalty that subtracts **0.5s from EVERY post** on the feed, flashing an entropy alert and red vignette. |
| **Procedural Visual Decay** | &bull; **100%–50%**: Crisp monospace text.<br>&bull; **49%–20%**: Progressive CSS `blur()` and fading opacity.<br>&bull; **19%–1%**: Procedural text corruption replacing letters with unicode glitch glyphs (`█`, `░`, `▒`, `▓`, `~`, `¤`, `∆`). When healed back above 20%, clean text is restored! |
| **Dynamic Health Bar** | Transitions from Cyan/Blue (>50%) &rarr; Amber/Yellow (20%–50%) &rarr; Red Danger (<20%). |

---

## How to Deploy to GitHub

### Option 1: Streamlit Community Cloud (What you had in your screenshot)

1. Commit and push all files in this directory to your GitHub repository:
   ```bash
   git add -A
   git commit -m "Deploy The Vigil"
   git push origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** &rarr; Select your GitHub repository &rarr; Set main file path to: `app.py`.
4. Click **Deploy!**

Your app will immediately build and run full-screen without errors.

---

### Option 2: GitHub Pages (1-Click Free Hosting)

Because this repository contains a self-contained root `index.html`:

1. Push your code to your GitHub repository.
2. In your GitHub repository, click **Settings** (top tab).
3. On the left sidebar, click **Pages**.
4. Under **Build and deployment** &rarr; **Branch**:
   - Select `main` (or `master`)
   - Folder: `/ (root)`
   - Click **Save**.
5. Within 60 seconds, GitHub will give you a live URL:
   `https://<your-username>.github.io/<your-repo-name>/`

---

### Option 3: Run Locally on Your Computer

Simply run:
```bash
python app.py
```
This automatically starts a local server and opens **http://localhost:5000** in your web browser.

Alternatively, if you have Streamlit installed:
```bash
streamlit run app.py
```

---

## Project Structure

```
Vigil/
├── index.html       ← Complete, production-ready SPA (runs anywhere)
├── app.py           ← Streamlit Cloud entrypoint + zero-dependency local runner
├── requirements.txt ← Streamlit dependency for cloud builders
├── render.yaml      ← Render.com deployment blueprint
├── Dockerfile       ← Containerized deployment (Railway / Cloud Run)
├── Procfile         ← Heroku / Render process configuration
├── .gitignore       ← Ignores cache and temporary files
└── README.md        ← Documentation and deployment guide
```

## License

MIT License. Free to use, modify, and distribute.
