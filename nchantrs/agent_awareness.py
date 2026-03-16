"""Agent awareness module for nchantrs.

This module provides agent-aware functionality for nchantrs, enabling
integration with various AI agents and their workflows.

## Overview

The nchantrs application is designed to work with multiple AI agents including:
- morg (primary agent)
- arthr (secondary agent)  
- gwen (auxiliary agent)

## Usage

```python
from nchantrs.agent_awareness import get_current_agent, get_agent_workspace

agent = get_current_agent()
workspace = get_agent_workspace()
```

## Agent Configuration

Each agent has:
- A workspace directory: /home/solubrew/.<agent>/workspace
- Access to shared resources
- Independent session management

## Integration Points

- Glain: Long-term knowledge and context management
- AXN: Task and workflow management
- MindOT: Decision engine for complex trade-offs
- Experience: Continuous learning from past tasks
"""

import logging
import os
from typing import Optional

logger: logging.Logger = logging.getLogger(__name__)


# Agent configuration constants
AGENT_WORKSPACE_TEMPLATE = "/home/solubrew/.{agent}/workspace"
DEFAULT_AGENT = "morg"


def get_current_agent() -> str:
    """Get the current agent name from environment or hostname.
    
    Returns:
        str: The current agent name (e.g., 'morg', 'arthr', 'gwen')
    
    Examples:
        >>> get_current_agent()
        'morg'
    """
    agent = os.getenv("AGENT_NAME", os.getenv("USER", DEFAULT_AGENT))
    logger.debug(f"Current agent determined: {agent}")
    return agent


def get_agent_workspace() -> str:
    """Get the current agent workspace path.
    
    Returns:
        str: Path to the current agent's workspace directory
    
    Examples:
        >>> get_agent_workspace()
        '/home/solubrew/.morg/workspace'
    """
    agent = get_current_agent()
    return os.getenv("AGENT_WORKSPACE", AGENT_WORKSPACE_TEMPLATE.format(agent=agent))


def is_agent_available(agent_name: Optional[str] = None) -> bool:
    """Check if a specific agent is available.
    
    Args:
        agent_name: Name of the agent to check. If None, checks current agent.
    
    Returns:
        bool: True if the agent's workspace exists
    
    Examples:
        >>> is_agent_available('morg')
        True
        >>> is_agent_available('nonexistent')
        False
    """
    agent = agent_name or get_current_agent()
    workspace = f"/home/solubrew/.{agent}/workspace"
    return os.path.exists(workspace)


def get_all_agents() -> list:
    """Get list of all known agents.
    
    Returns:
        list: List of agent names
    """
    return ["morg", "arthr", "gwen"]


def get_agent_config(agent_name: str) -> dict:
    """Get configuration for a specific agent.
    
    Args:
        agent_name: Name of the agent
    
    Returns:
        dict: Agent configuration including workspace, data paths, etc.
    """
    return {
        "name": agent_name,
        "workspace": f"/home/solubrew/.{agent_name}/workspace",
        "data": f"/home/solubrew/.{agent_name}",
        "sessions": f"/home/solubrew/.{agent_name}/sessions",
    }


__all__ = [
    "get_current_agent", 
    "get_agent_workspace", 
    "is_agent_available",
    "get_all_agents",
    "get_agent_config",
    "AGENT_WORKSPACE_TEMPLATE",
    "DEFAULT_AGENT",
]
