# TCET Campus Navigation & Shortest-Path Finder System
## Thakur College of Engineering & Technology

An interactive web application that allows students and visitors to navigate the TCOE campus building (7 floors + outdoor areas) using **Dijkstra's Algorithm** and **A\* (A-Star) Algorithm** for shortest-path finding.

---

## 📁 Project Structure

```
IIS/
├── backend/
│   ├── __init__.py      # Python package marker
│   ├── main.py          # FastAPI app — routes & static file serving
│   ├── graph.py         # Campus graph: all nodes, edges, coordinates
│   ├── algorithms.py    # Dijkstra's & A* implementations (pure Python)
│   └── models.py        # Pydantic request/response models
├── frontend/
│   ├── index.html       # Single-page application (SPA)
│   ├── style.css        # Dark-mode + neon theme
│   └── app.js           # Vis.js graph, API calls, UI logic
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Install dependencies
```bash
cd /path/to/IIS
pip install -r requirements.txt
```

### 2. Start the server
```bash
uvicorn backend.main:app --reload
```

### 3. Open your browser
```
http://localhost:8000
```

### 4. API documentation (auto-generated)
```
http://localhost:8000/docs
```

---

## 🧠 Algorithms

### Dijkstra's Algorithm
- Classic weighted shortest-path (greedy + priority queue)
- **Time Complexity**: O((V + E) log V)
- **Space Complexity**: O(V)
- Guaranteed to find the globally optimal path

### A\* Algorithm
- Heuristic-guided search; more efficient than Dijkstra for spatial graphs
- **Heuristic**: h(n) = |floor(n) − floor(goal)| × 50 seconds
  - Admissible: elevator travel (50 s/floor) is the minimum vertical cost
- **Time Complexity**: O(E log V) in practice
- **Space Complexity**: O(V)
- Explores fewer nodes than Dijkstra due to heuristic guidance

---

## 🏢 Campus Covered

| Area | Details |
|---|---|
| **Outdoor** | Main Gate, Multipurpose Hall, Garden, Sports Ground |
| **Ground Floor** | Canteen, Principal & Dean's Office, Main Office, Mechanical Automation Lab |
| **Floor 1** | Store Room, Seminar Hall 1 |
| **Floor 2** | Seminar Hall 2 & 3 |
| **Floor 3** | Boys Common Room (303) |
| **Floor 4** | College Library, Seminar Hall 4 |
| **Floor 5** | Classrooms 501, 502, 503 |
| **Floor 6** | Classrooms 601, 602, 603, NCC Office |
| **Floor 7** | Room 701 (Lab), Rooms 702 & 703, MTECH/B.VOC HOD Cabin |
| **All Floors** | Stairs, Elevator, Boys & Girls Washrooms |

---

## 🌐 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Frontend SPA |
| `GET` | `/api/graph` | Full Vis.js graph data |
| `GET` | `/api/locations` | Locations grouped by floor |
| `POST` | `/api/shortest-path` | Compute shortest path |

### Example: POST `/api/shortest-path`
```json
{
  "source": "main_gate",
  "destination": "library",
  "algorithm": "both",
  "mode": "elevator"
}
```

**Response includes:**
- Shortest path (node IDs + names)
- Total travel time (seconds)
- Turn-by-turn directions
- Nodes explored & compute time (for both algorithms)

---

## 🎨 UI Features
- **Interactive graph** — click any node to set source/destination
- **Algorithm comparison** — see Dijkstra's vs A* side-by-side
- **Transport mode** — prefer stairs, elevator, or use both
- **Turn-by-turn directions** — step-by-step instructions with emoji
- **Dark mode + neon accents** — modern premium design

---

## 📚 Technology Stack
| Component | Technology |
|---|---|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| Algorithms | Pure Python (heapq min-heap) |
| Frontend | HTML5, Vanilla CSS, Vanilla JavaScript |
| Graph Visualisation | Vis.js Network (CDN) |
| API Style | REST/JSON |
