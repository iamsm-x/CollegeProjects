"""
models.py — Pydantic API Models
================================
Defines request and response schemas for the Campus Navigation API.
FastAPI uses these to auto-validate inputs and auto-generate OpenAPI docs.
"""

from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------
class ShortestPathRequest(BaseModel):
    """
    Body sent by the frontend when requesting a shortest-path computation.
    """
    source: str = Field(
        ...,
        description="Node ID of the starting location (e.g. 'main_gate')",
        examples=["main_gate"],
    )
    destination: str = Field(
        ...,
        description="Node ID of the target location (e.g. 'library')",
        examples=["library"],
    )
    algorithm: Literal["dijkstra", "astar", "both"] = Field(
        default="both",
        description=(
            "Which algorithm(s) to run: "
            "'dijkstra' | 'astar' | 'both' (default — comparison mode)"
        ),
    )
    mode: Literal["both", "stairs", "elevator"] = Field(
        default="both",
        description=(
            "Vertical transport preference: "
            "'both' (any) | 'stairs' (no elevator) | 'elevator' (no stairs)"
        ),
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "source": "main_gate",
                "destination": "library",
                "algorithm": "both",
                "mode": "elevator",
            }
        }
    }


# ---------------------------------------------------------------------------
# Single-algorithm result
# ---------------------------------------------------------------------------
class PathResult(BaseModel):
    """Result produced by one algorithm run."""

    found:               bool
    path:                list[str]        # node IDs in order
    path_names:          list[str]        # human-readable names
    total_time_seconds:  float            # total estimated travel time
    nodes_explored:      int              # how many nodes the algo visited
    compute_time_us:     float            # wall-clock time in microseconds
    directions:          list[str]        # turn-by-turn instructions
    error:               Optional[str] = None  # set when found=False


# ---------------------------------------------------------------------------
# Full response
# ---------------------------------------------------------------------------
class ShortestPathResponse(BaseModel):
    """
    API response for /api/shortest-path.
    Contains results from one or both algorithms, plus request metadata.
    """
    source:           str
    source_name:      str
    destination:      str
    destination_name: str
    algorithm:        str          # echoes the requested algorithm(s)
    mode:             str          # echoes the transport mode
    dijkstra:         Optional[PathResult] = None
    astar:            Optional[PathResult] = None
