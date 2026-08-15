

# 🏫 TCET Campus Navigator

**Interactive shortest-path finder for Thakur College of Engineering & Technology**

Find the fastest route between any two points on campus — powered by **Dijkstra's** and **A\*** search over a real 7-floor building graph.



---

## ✨ Features

- 🗺️ **Room-by-room navigation** — browse every floor (Outdoor → Ground → 7F) and tap any room to set it as your source or destination
- ⚙️ **Dual algorithms** — run Dijkstra's, A*, or compare both side-by-side (path cost, nodes explored, compute time)
- 🚶 **Transport preference** — route via stairs only, elevator only, or whichever is faster
- 🧭 **Turn-by-turn directions** — plain-English steps with distances and floor changes
- 🌗 **Light / dark theme toggle** — switch modes from the navbar; your choice is remembered on your next visit
- 🔁 **Multi-floor transition alerts** — jump straight to the floor your route continues on
- ⚡ **FastAPI backend** — typed, validated, auto-documented REST API

---

## 📁 Project Structure

```
IIS/
├── backend/
│   ├── __init__.py      # Python package marker
│   ├── main.py          # FastAPI app — routes & static file serving
│   ├── graph.py         # Campus graph: all nodes, edges, travel-time weights
│   ├── algorithms.py    # Dijkstra's & A* implementations (pure Python)
│   └── models.py        # Pydantic request/response schemas
├── frontend/
│   ├── index.html       # Single-page application (SPA)
│   ├── style.css        # Light theme + dark mode, green accent palette
│   ├── app.js           # UI logic, theme toggle, API calls
│   ├── blueprints/      # Floor plan reference images
│   └── textures/        # Branding assets (logo, facade, signage)
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies
```bash
cd IIS
pip install -r requirements.txt
```

### 2. Start the server
```bash
uvicorn backend.main:app --reload
```

### 3. Open the app
```
http://localhost:8000
```

### 4. Explore the API docs (auto-generated Swagger UI)
```
http://localhost:8000/docs
```

---

## 🧠 Algorithms

### Dijkstra's Algorithm
- Classic weighted shortest-path search using a priority queue (min-heap)
- **Time complexity**: `O((V + E) log V)`
- **Space complexity**: `O(V)`
- Always finds the globally optimal path

### A\* Algorithm
- Heuristic-guided search — explores fewer nodes than Dijkstra on this campus graph
- **Heuristic**: `h(n) = |floor(n) − floor(goal)| × 30 seconds`
  - Admissible because the fastest possible way to change one floor (elevator, including wait) never costs less than 30 s
- **Time complexity**: `O(E log V)` in practice
- **Space complexity**: `O(V)`
- `algorithm: "both"` runs both and reports which explored fewer nodes and computed faster

---

## 🏢 Campus Coverage

| Area | Notable Locations |
|---|---|
| **Outdoor** | Main Gate, Multipurpose Hall, Garden, Sports Ground |
| **Ground Floor** | Canteen, Principal & Dean's Office, Main Office, Mechanical Automation Lab |
| **Floor 1** | Store Room, Seminar Hall 1 |
| **Floor 2** | Seminar Hall 2 & 3 |
| **Floor 3** | Boys Common Room (303) |
| **Floor 4** | College Library, Seminar Hall 4 |
| **Floor 5** | Classrooms 501, 502, 503 |
| **Floor 6** | Classrooms 601, 602, 603, NCC Office |
| **Floor 7** | Room 701 (Lab), Rooms 702 & 703, M.Tech/B.Voc HOD Cabin |
| **Every floor** | Stairs, elevator, boys' & girls' washrooms |

**Vertical travel times:** ~35 s per floor via stairs, ~30 s per floor via elevator (including wait).

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the frontend SPA |
| `GET` | `/api/graph` | Full campus graph (nodes + edges) |
| `GET` | `/api/locations` | Navigable locations grouped by floor |
| `POST` | `/api/shortest-path` | Compute the shortest path between two locations |

### Example — `POST /api/shortest-path`

**Request**
```json
{
  "source": "main_gate",
  "destination": "library",
  "algorithm": "both",
  "mode": "elevator"
}
```

**Response** includes, per algorithm:
- Ordered path (node IDs + human-readable names)
- Total travel time, in seconds
- Turn-by-turn directions
- Nodes explored & compute time (µs) — for comparing algorithm efficiency

---

## 📚 Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Validation | Pydantic v2 |
| Algorithms | Pure Python (`heapq` priority queue) |
| Frontend | HTML5, vanilla CSS, vanilla JavaScript — no build step |
| API style | REST / JSON, auto-documented via OpenAPI (Swagger) |

---

<div align="center">

Built for **Thakur College of Engineering & Technology** · Dijkstra's + A\* pathfinding demo

</div>
