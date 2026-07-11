# Frontend Taste Engineer showcase

This is a full, dependency-free localhost and a standalone static deployment.

## Run locally

```bash
cd plugins/frontend-taste-engineer/review-app
npm run dev
```

Open `http://127.0.0.1:8765/`. The command rebuilds the standalone site before serving it. Python 3 is the only runtime requirement; `python3 serve.py` is equivalent.

## Build and deploy

```bash
npm run build
```

The deployable output is written to `review-app/dist/`. It includes the interface, favicon, and a read-only snapshot of the relevant knowledge and evaluation artifacts, so it does not depend on repository-relative paths in production.

- Netlify: import the repository; the root `netlify.toml` supplies the build command, publish directory, and security headers.
- Any static host: use `python3 plugins/frontend-taste-engineer/review-app/build.py` as the build command and `plugins/frontend-taste-engineer/review-app/dist` as the output directory.
- Local production preview: run `npm run preview` after a build.

The compact technical showcase includes:

- a direct link to the verified GitHub repository;
- an interactive, explicitly conceptual specimen showing how art direction changes with product context;
- the plugin's documented operating loop and install commands;
- the existing local knowledge search and evaluation summary.

The interface has no external frontend dependencies, fonts, analytics, or backend. Artifact loading can fail without blocking the primary content or GitHub action, and the page never modifies stable knowledge. Deployments contain a build-time evidence snapshot; rebuild the site when the canonical plugin artifacts change.

See `DESIGN.md` for the product brief, design thesis, accessibility target, and rendered refinement record.
