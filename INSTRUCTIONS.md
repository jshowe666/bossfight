# Bossfight Isometric Prototype – Working Notes

This document gives Codex-compatible guidance for working on the current isometric Python/Pygame prototype and for extending it toward boss fights and multiplayer. The project is organized as a lightweight client demo with shared logic and a scaffolded (mostly empty) server layer.

## Quick start

1. Ensure Python 3.11+ is available and install `pygame` (the sole external dependency) in your environment.
2. Run the single-player prototype from the repo root:
   ```bash
   python -m client.main
   ```
3. Controls:
   - Right-click on land to pathfind and move (water tiles are treated as obstacles).
   - Move the mouse to the screen edges to pan the camera.
   - Space centers the camera on the player; Esc or window close quits.
   - Press **Q** to fire a straight-line missile toward the mouse.

## Code layout

- **client/** – Pygame client for the local prototype.
  - `client/main.py` – Entry point. Sets up Pygame, screen, `LocalState`, `Camera`, `Renderer`, and `InputHandler`, then runs the frame loop.
  - `client/game/` – Client gameplay state and input.
    - `local_state.py` – Owns grid data, player position, path following, missile lifecycle, cooldowns, and facing updates.
    - `input_handler.py` – Translates Pygame events into game actions (movement, camera centering, Q casts).
    - `camera.py` – Edge-based camera panning and centering helpers.
  - `client/render/` – Rendering utilities.
    - `renderer.py` – Draws tiles, paths, missiles, player sprites, and health bar.
    - `sprite_loader.py` – Loads directional sprites from `assets/sprites/{player,missiles}/` (expects `up.png`, `down.png`, `left.png`, `right.png`).
  - `client/net/` and `client/scenes/` – Empty scaffolding for future menu flows and networking.
- **shared/** – Logic used by both client and (future) server.
  - `constants.py` – Tile geometry, movement speeds, colors, health bar sizes, etc.
  - `game_logic/` – Isometric conversions, grid generation, and Dijkstra pathfinding that treats water as obstacles and blocks diagonal corner-cutting.
  - `game_models.py` – Data classes for common entities (currently just missiles).
- **server/** – Placeholder multiplayer server skeleton (protocol, TCP manager, world/room state) to fill in when networking is added.
- **assets/** – Expected home for sprite art; add your own PNGs to avoid missing-file errors when running the client.

## Game loop overview

1. `InputHandler.process_events` converts Pygame input into state changes (movement requests, Q casts, camera recentering).
2. `LocalState.update` advances player movement along the current path, steps missiles forward, and updates cooldowns.
3. `Renderer.render` draws the grid, path markers, missiles, and player sprite with a health bar using camera offsets.

## Extending toward boss fights and multiplayer

- **Boss fights:** Add new entities and combat rules to `shared/game_models.py` and `shared/game_logic/`, then render them in `client/render/renderer.py`. Place boss AI/state in `client/game/` until server logic exists.
- **Spells & abilities:** Mirror the Q missile flow (input → state → renderer). Keep cooldowns and direction handling in `LocalState` to simplify networking later.
- **Networking:** The empty `client/net/` and `server/` modules are intended for a future client/server split. Keep shared data and simulation rules in `shared/` so both sides stay deterministic.
- **Scenes/menus:** Build menu and lobby flows under `client/scenes/`, with `client/client_app.py` as a future orchestrator between menus and the game scene.

## Contribution tips

- Favor deterministic logic in `shared/` so it can be reused on the server.
- Keep rendering and input client-only; avoid importing Pygame in shared modules.
- When adding assets, maintain the directional naming scheme (`up/down/left/right.png`) so `sprite_loader` keeps working.
- For new gameplay features, extend `constants.py` with tunable values instead of hardcoding numbers in code.
