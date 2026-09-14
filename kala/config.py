"""Central configuration. Secrets come from the environment ONLY.

Never accept API keys through the UI. In Cursor set them as Cloud Agent
secrets; locally use a .env file / exported environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


def _load_dotenv() -> None:
    """Minimal .env loader (no dependency). Does not override real env vars.

    Set KALA_DISABLE_DOTENV=1 to skip loading .env — used to run a PUBLIC demo
    with the local narrator so a paid key is never exposed on an open URL.
    """
    if os.environ.get("KALA_DISABLE_DOTENV") == "1":
        return
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not os.path.exists(path):
        return
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    agents_model: str
    vision_model: str
    app_env: str

    @property
    def live_agents(self) -> bool:
        return bool(self.openai_api_key)


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.environ.get("OPENAI_API_KEY", "").strip(),
        agents_model=os.environ.get("KALA_AGENTS_MODEL", "gpt-4o-mini").strip(),
        vision_model=os.environ.get("KALA_VISION_MODEL", "gpt-4o-mini").strip(),
        app_env=os.environ.get("KALA_ENV", "production").strip(),
    )
