# Requirements — Tic-Tac-Toe Web UI

## v1 Requirements

### Board & Display
- [ ] **UI-01**: User sees a visual 3×3 grid representing the game board
- [ ] **UI-02**: User sees whose turn it is (X or O) above the board
- [ ] **UI-03**: User sees game outcome message when game ends (X wins, O wins, draw)
- [ ] **UI-04**: Winning cells are visually highlighted when a player wins

### Interaction
- [ ] **PLAY-01**: User can click an empty cell to make a move
- [ ] **PLAY-02**: User sees an error message when attempting an illegal move
- [ ] **PLAY-03**: User can click a "New Game" button to reset and start fresh
- [ ] **PLAY-04**: Board updates immediately after each move

### Game Modes
- [ ] **MODE-01**: User can choose between "Two Player" and "vs Computer" modes
- [ ] **MODE-02**: In two-player mode, X and O alternate on the same screen
- [ ] **MODE-03**: In vs-computer mode, computer plays as O and moves automatically after the user
- [ ] **MODE-04**: Computer opponent blocks winning moves and takes winning moves when available

### Integration
- [ ] **INT-01**: Frontend is served as a static file from FastAPI (same origin, port 8000)
- [ ] **INT-02**: All game state is managed via the existing REST API (no client-side game logic duplication)
- [ ] **INT-03**: CORS configuration is not needed (same origin)

## v2 Requirements (Deferred)
- Move history display
- Score tracking across multiple games
- Difficulty selector for computer opponent (easy/hard)
- Animations for moves and wins
- Mobile-responsive layout

## Out of Scope
- Online multiplayer / WebSockets — overkill for demo scope
- User accounts / authentication — not needed
- Database persistence — keep in-memory
- Build tools / bundlers — single file, no npm
- Minimax AI — simple heuristic is sufficient

## Traceability

| REQ | Phase | Status |
|-----|-------|--------|
| UI-01..04 | — | Pending |
| PLAY-01..04 | — | Pending |
| MODE-01..04 | — | Pending |
| INT-01..03 | — | Pending |

---
*Last updated: 2026-05-03 after initialization*
