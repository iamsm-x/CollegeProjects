"""
main.py — FastAPI Application Entry Point
==========================================
Thakur College of Engineering — Campus Navigation & Shortest-Path System

Endpoints
---------
GET  /                      — Serve the frontend SPA (index.html)
GET  /api/graph             — Full Vis.js graph data (nodes + edges)
GET  /api/locations         — Locations grouped by floor (for dropdowns)
POST /api/shortest-path     — Run Dijkstra's / A* and return result

Static files (CSS, JS) are served from the /frontend directory at /static/*.
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

try:
    from .graph import NODES, get_graph_for_visualization
    from .algorithms import dijkstra, astar
    from .models import ShortestPathRequest, ShortestPathResponse, PathResult
except ImportError:
    from graph import NODES, get_graph_for_visualization
    from algorithms import dijkstra, astar
    from models import ShortestPathRequest, ShortestPathResponse, PathResult

# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="TCOE Campus Navigation API",
    description=(
        "Shortest-path navigator for Thakur College of Engineering. "
        "Uses Dijkstra's and A* algorithms on a weighted campus graph."
    ),
    version="1.0.0",
    contact={"name": "TCOE Navigation Project"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory containing index.html, style.css, app.js
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# Mount /static → frontend directory (serves CSS & JS)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the main single-page application."""
    index = FRONTEND_DIR / "index.html"

    if not index.exists():
        raise HTTPException(
            status_code=404,
            detail="Frontend not found. Run from project root."
        )

    content = index.read_text(encoding="utf-8")
    return HTMLResponse(content=content)


@app.get("/style.css", include_in_schema=False)
async def serve_css():
    """Fallback handler for /style.css."""
    css = FRONTEND_DIR / "style.css"
    if css.exists():
        return FileResponse(str(css), media_type="text/css")
    raise HTTPException(status_code=404)


@app.get("/app.js", include_in_schema=False)
async def serve_js():
    """Fallback handler for /app.js."""
    js = FRONTEND_DIR / "app.js"
    if js.exists():
        return FileResponse(str(js), media_type="application/javascript")
    raise HTTPException(status_code=404)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return 204 No Content for favicon requests."""
    return JSONResponse(content={}, status_code=204)


@app.get(
    "/api/graph",
    summary="Get full campus graph",
    description="Returns all nodes and edges formatted for Vis.js visualisation.",
    tags=["Graph"],
)
async def get_graph():
    """Return the complete campus graph (nodes + edges) for the frontend."""
    return get_graph_for_visualization()


@app.get(
    "/api/locations",
    summary="List all navigable locations",
    description=(
        "Returns every campus location grouped by floor. "
        "Infrastructure nodes (stairs, elevator, washroom) are excluded."
    ),
    tags=["Locations"],
)
async def get_locations():
    """Return locations grouped by floor for dropdown menus."""
    SKIP_TYPES = {"washroom", "stairs", "elevator"}
    floors: dict = {}

    for node_id, data in NODES.items():
        if data["type"] in SKIP_TYPES:
            continue

        fl  = data["floor"]
        key = "outdoor" if fl == -1 else f"floor_{fl}"
        lbl = (
            "Outdoor Areas" if fl == -1
            else " Ground Floor" if fl == 0
            else f"Floor {fl}"
        )

        if key not in floors:
            floors[key] = {"floor": fl, "label": lbl, "locations": []}

        floors[key]["locations"].append({
            "id":   node_id,
            "name": data["name"],
            "type": data["type"],
        })

    # Sort lowest floor first (outdoor last for UX clarity)
    sorted_floors = sorted(floors.values(), key=lambda x: x["floor"])
    return {"floors": sorted_floors}


@app.post(
    "/api/shortest-path",
    response_model=ShortestPathResponse,
    summary="Find shortest path between two campus locations",
    description=(
        "Runs Dijkstra's and/or A* on the campus graph and returns "
        "the shortest path, travel time, step-by-step directions, "
        "and algorithm performance metrics."
    ),
    tags=["Navigation"],
)
async def find_shortest_path(request: ShortestPathRequest):
    """Core navigation endpoint — runs the selected algorithm(s)."""

    # ── Validate nodes ───────────────────────────────────────────────────────
    if request.source not in NODES:
        raise HTTPException(400, detail=f"Unknown source node: '{request.source}'")
    if request.destination not in NODES:
        raise HTTPException(400, detail=f"Unknown destination node: '{request.destination}'")
    if request.source == request.destination:
        raise HTTPException(400, detail="Source and destination must be different.")

    # ── Build response skeleton ──────────────────────────────────────────────
    response = ShortestPathResponse(
        source=request.source,
        source_name=NODES[request.source]["name"],
        destination=request.destination,
        destination_name=NODES[request.destination]["name"],
        algorithm=request.algorithm,
        mode=request.mode,
    )

    # ── Run algorithm(s) ─────────────────────────────────────────────────────
    if request.algorithm in ("dijkstra", "both"):
        result = dijkstra(request.source, request.destination, request.mode)
        response.dijkstra = PathResult(**result)

    if request.algorithm in ("astar", "both"):
        result = astar(request.source, request.destination, request.mode)
        response.astar = PathResult(**result)

    return response


# ---------------------------------------------------------------------------
# Dev entry-point  (python -m backend.main)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    import os
    import uvicorn
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    os.environ["PYTHONPATH"] = project_root + (os.pathsep + os.environ["PYTHONPATH"] if "PYTHONPATH" in os.environ else "")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
