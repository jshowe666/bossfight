#!/usr/bin/env bash

# Create top-level files
touch README.md
touch pyproject.toml
touch requirements.txt
touch .gitignore

# Config
mkdir -p config
touch config/server_config.yaml
touch config/client_config.yaml

# Assets
mkdir -p assets/sprites/player/idle
mkdir -p assets/sprites/player/walk
mkdir -p assets/sprites/player/cast
mkdir -p assets/sprites/missiles
mkdir -p assets/sprites/environment
mkdir -p assets/sprites/ui
mkdir -p assets/audio/sfx
mkdir -p assets/audio/music
mkdir -p assets/fonts

# Shared
mkdir -p shared/game_logic
mkdir -p shared/utils

touch shared/__init__.py
touch shared/constants.py
touch shared/enums.py
touch shared/messages.py
touch shared/game_models.py

touch shared/game_logic/__init__.py
touch shared/game_logic/systems.py
touch shared/game_logic/map_loader.py
touch shared/game_logic/balance.py
# New: dedicated modules for isometric math, pathfinding, and map generation
touch shared/game_logic/isometric.py
touch shared/game_logic/pathfinding.py
touch shared/game_logic/map_generation.py

touch shared/utils/__init__.py
touch shared/utils/serialization.py
touch shared/utils/math_utils.py
touch shared/utils/timing.py

# Server
mkdir -p server/net
mkdir -p server/state
mkdir -p server/logs

touch server/__init__.py
touch server/main.py
touch server/server_app.py
touch server/game_server.py

touch server/net/__init__.py
touch server/net/protocol.py
touch server/net/tcp_server.py
touch server/net/connection_manager.py

touch server/state/__init__.py
touch server/state/world_state.py
touch server/state/room_manager.py

touch server/logs/.gitkeep

# Client
mkdir -p client/net
mkdir -p client/game
mkdir -p client/render
mkdir -p client/scenes

touch client/__init__.py
touch client/main.py
touch client/client_app.py

touch client/net/__init__.py
touch client/net/client_protocol.py
touch client/net/connection.py

touch client/game/__init__.py
touch client/game/camera.py
touch client/game/input_handler.py
touch client/game/local_state.py
touch client/game/spell_bindings.py

touch client/render/__init__.py
touch client/render/sprite_loader.py
touch client/render/renderer.py
touch client/render/ui.py

touch client/scenes/__init__.py
touch client/scenes/base_scene.py
touch client/scenes/main_menu.py
touch client/scenes/game_scene.py

# Scripts
mkdir -p scripts
touch scripts/run_server_local.sh
touch scripts/run_client_local.sh
touch scripts/deploy_server_ec2.sh
touch scripts/setup_venv.sh
chmod +x scripts/*.sh

# Tests
mkdir -p tests
touch tests/__init__.py
touch tests/test_messages.py
touch tests/test_game_logic.py
touch tests/test_net_protocol.py

echo "Project structure initialized (with isometric + pathfinding modules)."
