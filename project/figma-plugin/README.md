# Figma development plugin

This plain-JavaScript development plugin reads selected layers, calls the local workflow backend, and applies text or image fills through the main-thread canvas bridge. No build step is required.

1. Start the root demo with `python scripts/dev.py` after following the root setup instructions.
2. In Figma Desktop, choose **Plugins → Development → Import plugin from manifest** and select this folder's `manifest.json`.
3. Run **Creative Workflow Studio** in an isolated scratch design.
4. Choose **Create demo selection** to create two text layers and a 1024 × 1024 fill-capable rectangle.
5. Pair with the local backend, generate or localize copy, create an image placeholder, and apply outputs.

The development allowlist permits only <http://127.0.0.1:4531>. Production domains remain disabled. The exchange is a fixed local demo; no real model provider is contacted. The placeholder is marked `placeholderOnly: true`.

`src/main.js` owns selection and canvas changes. `src/ui.html` owns the iframe controls and API requests. The browser harness exercises workflow and persistence independently of the Figma editor. Native canvas application was not rerun during this refresh; retain that distinction when demonstrating the project.
