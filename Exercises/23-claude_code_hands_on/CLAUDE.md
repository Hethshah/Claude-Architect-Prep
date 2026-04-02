# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**UIGen** — an AI-powered React component generator with live preview. Users describe components in natural language; Claude generates and updates code in real time via a streaming chat interface.

## Commands

```bash
npm run dev          # Start dev server (Next.js + Turbopack)
npm run build        # Production build
npm run lint         # ESLint
npm test             # Run all Vitest tests
npx vitest run src/path/to/file.test.ts  # Run a single test file

npm run setup        # First-time setup: install + prisma generate + migrate
npm run db:reset     # Reset SQLite database (destructive)
```

The dev server wraps Next.js with a `node-compat.cjs` shim (`NODE_OPTIONS='--require ./node-compat.cjs'`). All scripts include this automatically.

Requires `ANTHROPIC_API_KEY` in `.env`. Without it the app falls back to a static mock provider automatically.

## Architecture

### Virtual File System (VFS)
All generated code lives **in memory only** — nothing is written to disk. The VFS is implemented in `src/lib/file-system.ts` and exposed via `src/lib/contexts/file-system-context.tsx`. Claude's tools (`src/lib/tools/file-manager.ts`, `src/lib/tools/str-replace.ts`) operate exclusively on this VFS during generation.

### AI Provider Abstraction
`src/lib/provider.ts` wraps `@ai-sdk/anthropic`. If `ANTHROPIC_API_KEY` is absent, it returns a `MockLanguageModel` with canned responses. Always go through this abstraction rather than instantiating the Anthropic client directly.

### Chat → Generation Flow
1. User message → `POST /api/chat` (`src/app/api/chat/route.ts`)
2. Route calls Claude via Vercel AI SDK (`streamText`), passing tools and the system prompt from `src/lib/prompts/generation.tsx`
3. Claude streams text and invokes tools (`file-manager`, `str-replace`) to create/update files in the VFS
4. Frontend (`src/lib/contexts/chat-context.tsx`) consumes the stream and updates VFS state
5. Preview re-renders live

### Authentication & Persistence
JWT sessions are stored in HTTP-only cookies (`src/lib/auth.ts`). Anonymous users are fully supported — the VFS state is local only. Projects (messages + VFS snapshot as JSON) are persisted to SQLite via Prisma **only when a user is signed in**. See `src/actions/` for server actions and `prisma/schema.prisma` for the `User` / `Project` models.

### Live Preview
`src/components/preview/PreviewFrame` compiles VFS files via `@babel/standalone` at runtime inside a sandboxed iframe. There is no server-side execution of generated code.
