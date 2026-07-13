# Frontend Taste Engineer — Marketing Website

Marketing and interactive demo site for the [Frontend Taste Engineer](https://github.com/arnavsri993/frontend-taste-engineer) Codex plugin.

## Stack

- Next.js (App Router)
- TypeScript
- Tailwind CSS v4
- Lucide icons

## Development

```bash
cd website
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Production build

```bash
npm run build
npm start
```

## Deploy to Vercel

1. Import the repository in Vercel
2. Set the root directory to `website`
3. Deploy — no environment variables required

Alternatively, from the `website` directory:

```bash
npx vercel
```

## Design

See [DESIGN.md](./DESIGN.md) for product summary, design thesis, palette, typography, and accessibility strategy.

## Notes

- The Taste Lab demo is an **illustrative workflow preview** — it does not run the actual plugin.
- Plugin version is read from `plugins/frontend-taste-engineer/.codex-plugin/plugin.json` at build time.
- No analytics or telemetry are included in this site.
