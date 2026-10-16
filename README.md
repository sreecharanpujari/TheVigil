"""
The Vigil — An experiment in digital impermanence.

Supports multiple deployment targets:
1. Streamlit Community Cloud (via GitHub: `streamlit run app.py`)
2. Local Python execution (`python app.py`)
3. GitHub Pages (direct static hosting via root `index.html`)
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML_PATH = BASE_DIR / "index.html"


def load_html() -> str:
    """Read the self-contained Vigil application HTML."""
    if INDEX_HTML_PATH.exists():
        return INDEX_HTML_PATH.read_text(encoding="utf-8")
    return "<h1>Error: index.html not found.</h1>"


def run_streamlit_app():
    """Renders The Vigil inside Streamlit (Community Cloud or local)."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.set_page_config(
        page_title="The Vigil",
        page_icon="🕯️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Clean styling to remove default Streamlit padding and headers
    st.markdown(
        """
        <style>
        #MainMenu, header, footer {
            visibility: hidden;
            display: none !important;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            z-index: 999999;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    html_code = load_html()
    components.html(html_code, height=950, scrolling=True)


def run_local_server(port: int = 5000):
    """Fallback: Zero-dependency local web server for `python app.py`."""
    import http.server
    import socketserver
    import webbrowser

    os.chdir(BASE_DIR)
    handler = http.server.SimpleHTTPRequestHandler

    print()
    print("  +==========================================+")
    print("  |        T H E   V I G I L                 |")
    print("  |                                          |")
    print(f"  |   -> http://localhost:{port:<19}|")
    print("  |   Reading heals.  Typing kills.          |")
    print("  +==========================================+")
    print()

    webbrowser.open(f"http://localhost:{port}")

    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down The Vigil server.")


# ─────────────────────────────────────────────────────────────
# Execution Entry Point
# ─────────────────────────────────────────────────────────────

# Detect if Streamlit is executing this file (Streamlit sets special module flags)
is_streamlit = (
    "streamlit" in sys.modules
    or any("streamlit" in arg for arg in sys.argv)
    or os.environ.get("STREAMLIT_SERVER_PORT") is not None
)

if is_streamlit:
    run_streamlit_app()
elif __name__ == "__main__":
    # If executed as `python app.py` directly:
    try:
        import streamlit
        from streamlit.web import cli as stcli

        sys.argv = ["streamlit", "run", str(Path(__file__).resolve())]
        sys.exit(stcli.main())
    except ImportError:
        # If streamlit is not installed locally, use Python's built-in web server
        port = int(os.environ.get("PORT", 5000))
        run_local_server(port=port)
