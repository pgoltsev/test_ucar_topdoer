#!/usr/bin/env sh
uv run alembic upgrade head
uv run fastapi dev src/test_ucar/main.py --host 0.0.0.0