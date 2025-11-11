# Documentation

## Summary

Frontend user interface built with React to visualize experiment results using charts and carousels. Uses libraries such as ECharts and Embla Carousel, and tanstack/react-query for API calls and caching to avoid delays when loading large datasets (e.g., ~240 image records).

## Requirements

- Node.js >= 22.14.0 (recommended)
- Package manager: bun
- Access to the backend API (URL and credentials if required)

If you use NVM (Node Version Manager):

```bash
cd frontend
# install and use Node 22.14.0 if not already installed
nvm install 22.14.0
nvm use 22.14.0
```

## Installation

From the `frontend` directory:

```bash
bun install
```

## Useful scripts

Adjust these commands based on `package.json` scripts.

```bash
# start in development mode (hot-reload)
bun run dev

# build for production
bun run build
```

## Project structure

```
└── 📁frontend
    ├── 📁public         # static files (index.html, favicon...)
    └── 📁src
        ├── 📁components # reusable components
        ├── 📁lib        # general utilities
        ├── 📁pages      # main views / pages
        ├── 📁services   # API calls / HTTP clients
        └── 📁types
    ├── .gitignore
    ├── .nvmrc
    ├── .prettierignore
    ├── .prettierrc
    ├── bun.lockb
    ├── components.json
    ├── eslint.config.js
    ├── index.html
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.js
    ├── README.md
    ├── tailwind.config.ts
    ├── tsconfig.app.json
    ├── tsconfig.json
    ├── tsconfig.node.json
    └── vite.config.ts
```

## Environment variables

Create a `.env` file. Vite environment variables typically use the VITE\_ prefix. Example:

```
VITE_API_URL=https://api.example.com
# or for local development:
# VITE_API_URL=http://localhost:8000/api

VITE_ENVIRONMENT=development
# or
# VITE_ENVIRONMENT=production
```

## Development

- Start the dev server:

```bash
bun run dev
```

- Open the app at: http://localhost:5173

## Continuous Integration

The repository is integrated with Vercel and configured to detect changes automatically in the `/frontend` directory for deployments.
