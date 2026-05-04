# Roadmap — Tic-Tac-Toe Web UI

## Milestone 1: Web UI

### Phase 1: Board & Two-Player Mode
**Goal:** A playable two-player tic-tac-toe game in the browser served from FastAPI.

**Requirements:** UI-01, UI-02, UI-03, UI-04, PLAY-01, PLAY-02, PLAY-03, PLAY-04, MODE-01, MODE-02, INT-01, INT-02, INT-03

**Success Criteria:**
1. User can open `http://localhost:8000` and see a 3×3 board
2. Two players can take turns clicking cells, with moves validated by the API
3. Game displays winner/draw and highlights winning line
4. "New Game" button resets the board
5. Mode selector is visible (two-player is default and functional)

**Plans:** 2 plans

Plans:
- [ ] 01-01-PLAN.md — FastAPI static file serving
- [ ] 01-02-PLAN.md — Frontend game UI (board, gameplay, mode selector)

**UI hint**: yes

### Phase 2:Computer Opponent
**Goal:** Add a computer opponent that plays as O with basic strategy.

**Requirements:** MODE-03, MODE-04

**Success Criteria:**
1. User selects "vs Computer" mode and plays as X
2. Computer automatically responds with a move after user's turn
3. Computer blocks user's winning moves when possible
4. Computer takes winning moves when available

**UI hint**: yes

---

## Coverage

| REQ | Phase |
|-----|-------|
| UI-01 | 1 |
| UI-02 | 1 |
| UI-03 | 1 |
| UI-04 | 1 |
| PLAY-01 | 1 |
| PLAY-02 | 1 |
| PLAY-03 | 1 |
| PLAY-04 | 1 |
| MODE-01 | 1 |
| MODE-02 | 1 |
| MODE-03 | 2 |
| MODE-04 | 2 |
| INT-01 | 1 |
| INT-02 | 1 |
| INT-03 | 1 |

**15 requirements → 2 phases → 100% coverage ✓**

---
*Last updated: 2026-05-03 after initialization*
