"""Agent awareness module for nchantrs.

This module provides agent-aware functionality for nchantrs, enabling
integration with various AI agents and their workflows.
"""

import os
from typing import Optional


def get_current_agent() -> str:
    """Get the current agent name from environment or hostname."""
    agent = os.getenv("AGENT_NAME", os.getenv("USER", "default"))
    return agent


def get_agent_workspace() -> str:
    """Get the current agent workspace path."""
    agent = get_current_agent()
    return os.getenv("AGENT_WORKSPACE", f"/home/solubrew/.{agent}/workspace")


def is_agent_available(agent_name: Optional[str] = None) -> bool:
    """Check if a specific agent is available."""
    agent = agent_name or get_current_agent()
    workspace = f"/home/solubrew/.{agent}/workspace"
    return os.path.exists(workspace)


__all__ = ["get_current_agent", "get_agent_workspace", "is_agent_available"]
