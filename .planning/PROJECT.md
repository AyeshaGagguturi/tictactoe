# Tic-Tac-Toe — Web UI

## What This Is

A browser-based frontend for the existing Tic-Tac-Toe REST API. A single HTML page (vanilla HTML/CSS/JS) served by FastAPI that lets players visually play tic-tac-toe instead of using curl or Swagger UI.

## Core Value

**Play tic-tac-toe in the browser** — click cells, see the board update, get instant feedback on wins/draws/errors.

## Context

- **Existing codebase:** A working FastAPI backend with full game logic, REST endpoints, and test coverage
- **Stack:** Python 3.12, FastAPI, Pydantic, uvicorn
- **Storage:** In-memory dict (no database)
- **API endpoints already exist:** create game, make move, get state, reset, delete

## Who It's For

Developers demoing the API (e.g., in an interview) and anyone who wants to quickly play a game without crafting HTTP requests.

## Requirements

### Validated

- ✓ Game creation via API — existing
- ✓ Move validation (turn order, cell taken, game over) — existing
- ✓ Win/draw detection — existing
- ✓ Game reset — existing
- ✓ Health check endpoint — existing

### Active

- [ ] Visual 3×3 game board rendered in the browser
- [ ] Click a cell to make a move (calls POST /games/{id}/moves)
- [ ] Display whose turn it is (X or O)
- [ ] Display game outcome (X wins, O wins, draw)
- [ ] Highlight winning line when game is won
- [ ] Reset button to start a new game
- [ ] Two-player hot-seat mode (two humans, same screen)
- [ ] Computer opponent mode (simple AI that picks moves)
- [ ] Mode selector to choose between two-player and vs computer
- [ ] Served as a static file from FastAPI (same server, port 8000)
- [ ] CORS not needed (same origin)

### Out of Scope

- Online multiplayer / WebSockets — overkill for this scope
- User accounts / auth — not needed
- Persistent storage / database — keep in-memory
- Mobile-specific responsive design — desktop-first is fine
- Build tools / bundlers — single HTML file, no npm

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Single HTML file with inline CSS/JS | No build tools, zero setup, easy to demo | — Pending |
| Serve via FastAPI StaticFiles | Same origin, no CORS, one server to run | — Pending |
| Simple AI (random + block/win) | Good enough for demo, no minimax complexity | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-03 after initialization*
