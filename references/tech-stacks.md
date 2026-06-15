# Recommended Tech Stacks by Project Type

This reference provides curated tech stack recommendations for common project types. Use these as starting points — always adjust based on user preferences, team skills, and project constraints.

## Web Application (Frontend Only)

### Option A: Modern SPA (Recommended for most cases)
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | React 18+ with TypeScript | Largest ecosystem, best AI coding support |
| Styling | Tailwind CSS | Utility-first, AI generates it well |
| Build | Vite | Fast dev server, simple config |
| State | Zustand | Minimal boilerplate, easy to understand |
| Routing | React Router v6 | Standard, well-documented |
| Deploy | Vercel / Netlify | Zero-config deploys |

### Option B: Lightweight
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | Vanilla HTML + CSS + JS | No build step, simplest possible |
| Styling | Tailwind CSS (CDN) | Quick styling without setup |
| Deploy | GitHub Pages / CloudStudio | Free static hosting |

### Option C: Vue Alternative
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | Vue 3 + TypeScript | Approachable, great for small-to-medium apps |
| Styling | Tailwind CSS | Same benefits |
| Build | Vite | First-class Vue support |
| State | Pinia | Official Vue state management |

## CLI Tool / Script

### Python CLI
| Layer | Technology | Reason |
|-------|-----------|--------|
| Language | Python 3.12+ | Rich ecosystem, great for data/scripts |
| CLI Framework | Click or Typer | Type-hint friendly, auto-generated help |
| Config | Pydantic | Data validation, settings management |
| Package | uv or pip | Fast dependency management |

### Node.js CLI
| Layer | Technology | Reason |
|-------|-----------|--------|
| Language | TypeScript | Type safety for larger tools |
| CLI Framework | Commander.js | Simple, widely used |
| Prompts | Inquirer.js | Interactive CLI prompts |
| Package | pnpm | Fast, disk-efficient |

## Full-Stack Application

### Option A: JavaScript Monorepo
| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | React + TypeScript + Vite | Consistent language across stack |
| Backend | Node.js + Express/Fastify | Same language, shared types |
| Database | PostgreSQL + Prisma ORM | Type-safe DB access, great migrations |
| Auth | NextAuth.js / Lucia | Flexible auth solutions |
| Deploy | Docker Compose | Full control, consistent environments |

### Option B: Python Backend + React Frontend
| Layer | Technology | Reason |
|-------|-----------|--------|
| Frontend | React + TypeScript + Vite | Best frontend DX |
| Backend | FastAPI (Python) | Auto-generated API docs, async |
| Database | SQLite (dev) / PostgreSQL (prod) | Easy local dev, scalable prod |
| Auth | JWT + OAuth2 | Standard, well-supported |

### Option C: All-in-One
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | Next.js 14+ (App Router) | Full-stack React, SSR, API routes |
| Database | SQLite via Drizzle ORM | Zero-config local DB |
| Auth | NextAuth.js | Built-in auth for Next.js |
| Deploy | Vercel | Seamless Next.js deployment |

## Static Site / Documentation
| Layer | Technology | Reason |
|-------|-----------|--------|
| Generator | VitePress / Docusaurus | Fast, markdown-based |
| Styling | Default theme + custom CSS | Minimal effort |
| Deploy | GitHub Pages / Vercel | Free hosting |

## Mobile App
| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | React Native + Expo | Cross-platform, familiar React |
| Navigation | Expo Router | File-based routing |
| State | Zustand | Same as web React |

## Decision Factors

When choosing between options, consider:

1. **User familiarity**: If the user mentions a preference, use it
2. **Project complexity**: Simple projects = simpler stacks
3. **Time to MVP**: Monorepo / all-in-one stacks ship fastest
4. **AI coding support**: React + TypeScript has the best AI coding assistance due to training data abundance
5. **Deployment target**: If the user has a preferred platform, align the stack

## Stack Selection Prompt

When presenting the tech stack choice to the user, frame it as:

"We recommend [Option X] because [reason]. Alternative options are [Y] if you prefer [trade-off]. Which would you like to go with?"
