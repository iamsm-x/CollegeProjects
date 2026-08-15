"""
graph.py — Campus Graph Data for Thakur College of Engineering
==============================================================
Defines all nodes (locations) and edges (connections with travel-time weights)
that form the navigation graph of the 7-floor building plus outdoor areas.

Node Types  : room, lab, office, stairs, elevator, washroom, outdoor,
              seminar, canteen, library
Transport   : walk, stairs, elevator
Weights     : estimated travel time in seconds
Coordinates : x,y used by Vis.js for fixed-position rendering
              Floor f → y = (7 - f) * 130  (Floor 7 at top, outdoor below GF)
"""

# ---------------------------------------------------------------------------
# Constants — node types
# ---------------------------------------------------------------------------
TYPE_ROOM     = "room"
TYPE_LAB      = "lab"
TYPE_OFFICE   = "office"
TYPE_STAIRS   = "stairs"
TYPE_ELEVATOR = "elevator"
TYPE_WASHROOM = "washroom"
TYPE_OUTDOOR  = "outdoor"
TYPE_SEMINAR  = "seminar"
TYPE_CANTEEN  = "canteen"
TYPE_LIBRARY  = "library"

# Constants — transport types for edges
TRANSPORT_WALK     = "walk"
TRANSPORT_STAIRS   = "stairs"
TRANSPORT_ELEVATOR = "elevator"

# ---------------------------------------------------------------------------
# Floor colour palette for Vis.js node styling
# ---------------------------------------------------------------------------
FLOOR_BG_COLOR = {
    -1: "#0d2b1a",  # Outdoor  — deep forest green
     0: "#0d1b2b",  # Ground   — deep navy
     1: "#1a0d2b",  # Floor 1  — deep purple
     2: "#2b0d1a",  # Floor 2  — deep rose
     3: "#2b1a0d",  # Floor 3  — deep amber
     4: "#0d2b2b",  # Floor 4  — deep teal
     5: "#1a2b0d",  # Floor 5  — deep lime
     6: "#2b0d0d",  # Floor 6  — deep red
     7: "#0d1a2b",  # Floor 7  — deep blue
}

FLOOR_BORDER_COLOR = {
    -1: "#00ff88",  # Outdoor  — neon green
     0: "#00f5d4",  # Ground   — neon cyan
     1: "#7b2fff",  # Floor 1  — neon purple
     2: "#ff2fa0",  # Floor 2  — neon pink
     3: "#ffaa00",  # Floor 3  — neon amber
     4: "#00d4f5",  # Floor 4  — neon sky
     5: "#aaff00",  # Floor 5  — neon lime
     6: "#ff4444",  # Floor 6  — neon red
     7: "#4488ff",  # Floor 7  — neon blue
}

# ---------------------------------------------------------------------------
# Helper — compute fixed y-coordinate for a given floor
# ---------------------------------------------------------------------------
def _fy(floor: int) -> int:
    """Return Vis.js y-coordinate for a floor. Outdoor (floor -1) goes below GF."""
    if floor == -1:
        return 1090
    return (7 - floor) * 130


# ---------------------------------------------------------------------------
# NODES
# Format: node_id → {name, floor, type, short, x, y}
#   short : abbreviated label shown inside the Vis.js node circle
# ---------------------------------------------------------------------------
NODES: dict = {

    # ── Outdoor Areas (floor = -1) ──────────────────────────────────────────
    "main_gate": {
        "name": "Main Gate", "floor": -1, "type": TYPE_OUTDOOR,
        "short": "Gate", "x": 0, "y": _fy(-1),
    },
    "multipurpose_hall": {
        "name": "Multipurpose Hall", "floor": -1, "type": TYPE_OUTDOOR,
        "short": "MPH", "x": -220, "y": _fy(-1) - 60,
    },
    "garden": {
        "name": "Garden", "floor": -1, "type": TYPE_OUTDOOR,
        "short": "Garden", "x": 220, "y": _fy(-1) - 60,
    },
    "sports_ground": {
        "name": "Sports Ground", "floor": -1, "type": TYPE_OUTDOOR,
        "short": "Sports", "x": 0, "y": _fy(-1) - 130,
    },

    # ── Building Entrance (floor = 0, treated as outdoor boundary) ──────────
    "building_entrance": {
        "name": "Building Entrance", "floor": 0, "type": TYPE_OUTDOOR,
        "short": "Entry", "x": 0, "y": _fy(0) + 60,
    },

    # ── Ground Floor (floor = 0) ─────────────────────────────────────────────
    "canteen": {
        "name": "Canteen", "floor": 0, "type": TYPE_CANTEEN,
        "short": "Canteen", "x": -240, "y": _fy(0),
    },
    "principal_office": {
        "name": "Principal & Dean's Office", "floor": 0, "type": TYPE_OFFICE,
        "short": "Principal", "x": -90, "y": _fy(0),
    },
    "main_office": {
        "name": "Main Office", "floor": 0, "type": TYPE_OFFICE,
        "short": "Office", "x": 90, "y": _fy(0),
    },
    "mech_auto_lab": {
        "name": "Mechanical Automation Lab", "floor": 0, "type": TYPE_LAB,
        "short": "Mech Lab", "x": 240, "y": _fy(0),
    },
    "boys_wc_0": {
        "name": "Boys Washroom (GF)", "floor": 0, "type": TYPE_WASHROOM,
        "short": "GF", "x": -390, "y": _fy(0),
    },
    "girls_wc_0": {
        "name": "Girls Washroom (GF)", "floor": 0, "type": TYPE_WASHROOM,
        "short": "GF", "x": 390, "y": _fy(0),
    },
    "stairs_0": {
        "name": "Stairs (Ground Floor)", "floor": 0, "type": TYPE_STAIRS,
        "short": "GF", "x": -330, "y": _fy(0),
    },
    "elevator_0": {
        "name": "Elevator (Ground Floor)", "floor": 0, "type": TYPE_ELEVATOR,
        "short": "GF", "x": 330, "y": _fy(0),
    },

    # ── First Floor (floor = 1) ──────────────────────────────────────────────
    "store_room": {
        "name": "Store Room", "floor": 1, "type": TYPE_ROOM,
        "short": "Store", "x": -90, "y": _fy(1),
    },
    "seminar_hall_1": {
        "name": "Seminar Hall 1", "floor": 1, "type": TYPE_SEMINAR,
        "short": "SH-1", "x": 90, "y": _fy(1),
    },
    "boys_wc_1": {
        "name": "Boys Washroom (1F)", "floor": 1, "type": TYPE_WASHROOM,
        "short": "1F", "x": -390, "y": _fy(1),
    },
    "girls_wc_1": {
        "name": "Girls Washroom (1F)", "floor": 1, "type": TYPE_WASHROOM,
        "short": "1F", "x": 390, "y": _fy(1),
    },
    "stairs_1": {
        "name": "Stairs (1st Floor)", "floor": 1, "type": TYPE_STAIRS,
        "short": "1F", "x": -330, "y": _fy(1),
    },
    "elevator_1": {
        "name": "Elevator (1st Floor)", "floor": 1, "type": TYPE_ELEVATOR,
        "short": "1F", "x": 330, "y": _fy(1),
    },

    # ── Second Floor (floor = 2) ─────────────────────────────────────────────
    "seminar_hall_2": {
        "name": "Seminar Hall 2", "floor": 2, "type": TYPE_SEMINAR,
        "short": "SH-2", "x": -90, "y": _fy(2),
    },
    "seminar_hall_3": {
        "name": "Seminar Hall 3", "floor": 2, "type": TYPE_SEMINAR,
        "short": "SH-3", "x": 90, "y": _fy(2),
    },
    "boys_wc_2": {
        "name": "Boys Washroom (2F)", "floor": 2, "type": TYPE_WASHROOM,
        "short": "2F", "x": -390, "y": _fy(2),
    },
    "girls_wc_2": {
        "name": "Girls Washroom (2F)", "floor": 2, "type": TYPE_WASHROOM,
        "short": "2F", "x": 390, "y": _fy(2),
    },
    "stairs_2": {
        "name": "Stairs (2nd Floor)", "floor": 2, "type": TYPE_STAIRS,
        "short": "2F", "x": -330, "y": _fy(2),
    },
    "elevator_2": {
        "name": "Elevator (2nd Floor)", "floor": 2, "type": TYPE_ELEVATOR,
        "short": "2F", "x": 330, "y": _fy(2),
    },

    # ── Third Floor (floor = 3) ──────────────────────────────────────────────
    "boys_common_room_303": {
        "name": "Boys Common Room (303)", "floor": 3, "type": TYPE_ROOM,
        "short": "BCR 303", "x": 0, "y": _fy(3),
    },
    "boys_wc_3": {
        "name": "Boys Washroom (3F)", "floor": 3, "type": TYPE_WASHROOM,
        "short": "3F", "x": -390, "y": _fy(3),
    },
    "girls_wc_3": {
        "name": "Girls Washroom (3F)", "floor": 3, "type": TYPE_WASHROOM,
        "short": "3F", "x": 390, "y": _fy(3),
    },
    "stairs_3": {
        "name": "Stairs (3rd Floor)", "floor": 3, "type": TYPE_STAIRS,
        "short": "3F", "x": -330, "y": _fy(3),
    },
    "elevator_3": {
        "name": "Elevator (3rd Floor)", "floor": 3, "type": TYPE_ELEVATOR,
        "short": "3F", "x": 330, "y": _fy(3),
    },

    # ── Fourth Floor (floor = 4) ─────────────────────────────────────────────
    "library": {
        "name": "College Library", "floor": 4, "type": TYPE_LIBRARY,
        "short": "Library", "x": -90, "y": _fy(4),
    },
    "seminar_hall_4": {
        "name": "Seminar Hall 4", "floor": 4, "type": TYPE_SEMINAR,
        "short": "SH-4", "x": 90, "y": _fy(4),
    },
    "boys_wc_4": {
        "name": "Boys Washroom (4F)", "floor": 4, "type": TYPE_WASHROOM,
        "short": "4F", "x": -390, "y": _fy(4),
    },
    "girls_wc_4": {
        "name": "Girls Washroom (4F)", "floor": 4, "type": TYPE_WASHROOM,
        "short": "4F", "x": 390, "y": _fy(4),
    },
    "stairs_4": {
        "name": "Stairs (4th Floor)", "floor": 4, "type": TYPE_STAIRS,
        "short": "4F", "x": -330, "y": _fy(4),
    },
    "elevator_4": {
        "name": "Elevator (4th Floor)", "floor": 4, "type": TYPE_ELEVATOR,
        "short": "4F", "x": 330, "y": _fy(4),
    },

    # ── Fifth Floor (floor = 5) — Classrooms ────────────────────────────────
    "room_501": {
        "name": "Room 501", "floor": 5, "type": TYPE_ROOM,
        "short": "501", "x": -120, "y": _fy(5),
    },
    "room_502": {
        "name": "Room 502", "floor": 5, "type": TYPE_ROOM,
        "short": "502", "x": 0, "y": _fy(5),
    },
    "room_503": {
        "name": "Room 503", "floor": 5, "type": TYPE_ROOM,
        "short": "503", "x": 120, "y": _fy(5),
    },
    "boys_wc_5": {
        "name": "Boys Washroom (5F)", "floor": 5, "type": TYPE_WASHROOM,
        "short": "5F", "x": -390, "y": _fy(5),
    },
    "girls_wc_5": {
        "name": "Girls Washroom (5F)", "floor": 5, "type": TYPE_WASHROOM,
        "short": "5F", "x": 390, "y": _fy(5),
    },
    "stairs_5": {
        "name": "Stairs (5th Floor)", "floor": 5, "type": TYPE_STAIRS,
        "short": "5F", "x": -330, "y": _fy(5),
    },
    "elevator_5": {
        "name": "Elevator (5th Floor)", "floor": 5, "type": TYPE_ELEVATOR,
        "short": "5F", "x": 330, "y": _fy(5),
    },

    # ── Sixth Floor (floor = 6) — Classrooms + NCC Office ───────────────────
    "room_601": {
        "name": "Room 601", "floor": 6, "type": TYPE_ROOM,
        "short": "601", "x": -160, "y": _fy(6),
    },
    "room_602": {
        "name": "Room 602", "floor": 6, "type": TYPE_ROOM,
        "short": "602", "x": -40, "y": _fy(6),
    },
    "room_603": {
        "name": "Room 603", "floor": 6, "type": TYPE_ROOM,
        "short": "603", "x": 80, "y": _fy(6),
    },
    "ncc_office": {
        "name": "NCC Office", "floor": 6, "type": TYPE_OFFICE,
        "short": "NCC", "x": 200, "y": _fy(6),
    },
    "boys_wc_6": {
        "name": "Boys Washroom (6F)", "floor": 6, "type": TYPE_WASHROOM,
        "short": "6F", "x": -390, "y": _fy(6),
    },
    "girls_wc_6": {
        "name": "Girls Washroom (6F)", "floor": 6, "type": TYPE_WASHROOM,
        "short": "6F", "x": 390, "y": _fy(6),
    },
    "stairs_6": {
        "name": "Stairs (6th Floor)", "floor": 6, "type": TYPE_STAIRS,
        "short": "6F", "x": -330, "y": _fy(6),
    },
    "elevator_6": {
        "name": "Elevator (6th Floor)", "floor": 6, "type": TYPE_ELEVATOR,
        "short": "6F", "x": 330, "y": _fy(6),
    },

    # ── Seventh Floor (floor = 7) — Classrooms + MTECH/BVOC HOD ─────────────
    "room_701": {
        "name": "Room 701 (Lab)", "floor": 7, "type": TYPE_LAB,
        "short": "701 Lab", "x": -160, "y": _fy(7),
    },
    "room_702": {
        "name": "Room 702", "floor": 7, "type": TYPE_ROOM,
        "short": "702", "x": -40, "y": _fy(7),
    },
    "room_703": {
        "name": "Room 703", "floor": 7, "type": TYPE_ROOM,
        "short": "703", "x": 80, "y": _fy(7),
    },
    "mtech_bvoc_hod": {
        "name": "MTECH / B.VOC HOD Cabin", "floor": 7, "type": TYPE_OFFICE,
        "short": "HOD", "x": 200, "y": _fy(7),
    },
    "boys_wc_7": {
        "name": "Boys Washroom (7F)", "floor": 7, "type": TYPE_WASHROOM,
        "short": "7F", "x": -390, "y": _fy(7),
    },
    "girls_wc_7": {
        "name": "Girls Washroom (7F)", "floor": 7, "type": TYPE_WASHROOM,
        "short": "7F", "x": 390, "y": _fy(7),
    },
    "stairs_7": {
        "name": "Stairs (7th Floor)", "floor": 7, "type": TYPE_STAIRS,
        "short": "7F", "x": -330, "y": _fy(7),
    },
    "elevator_7": {
        "name": "Elevator (7th Floor)", "floor": 7, "type": TYPE_ELEVATOR,
        "short": "7F", "x": 330, "y": _fy(7),
    },
}


# ---------------------------------------------------------------------------
# EDGES
# Each edge is bidirectional. Weight = estimated travel time in seconds.
# transport: TRANSPORT_WALK | TRANSPORT_STAIRS | TRANSPORT_ELEVATOR
# ---------------------------------------------------------------------------
EDGES: list[dict] = [

    # ── Outdoor connections (all walking) ───────────────────────────────────
    {"source": "main_gate",         "target": "building_entrance",  "weight": 70, "transport": TRANSPORT_WALK},
    {"source": "main_gate",         "target": "multipurpose_hall",  "weight": 55, "transport": TRANSPORT_WALK},
    {"source": "main_gate",         "target": "garden",             "weight": 35, "transport": TRANSPORT_WALK},
    {"source": "main_gate",         "target": "sports_ground",      "weight": 90, "transport": TRANSPORT_WALK},
    {"source": "multipurpose_hall", "target": "garden",             "weight": 25, "transport": TRANSPORT_WALK},
    {"source": "garden",            "target": "sports_ground",      "weight": 35, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "multipurpose_hall",  "weight": 35, "transport": TRANSPORT_WALK},

    # ── Ground floor internal walking connections ────────────────────────────
    {"source": "building_entrance", "target": "canteen",            "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "principal_office",   "weight": 15, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "main_office",        "weight": 20, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "mech_auto_lab",      "weight": 20, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "boys_wc_0",          "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "girls_wc_0",         "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "stairs_0",           "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "building_entrance", "target": "elevator_0",         "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "canteen",           "target": "principal_office",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "principal_office",  "target": "main_office",        "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "main_office",       "target": "mech_auto_lab",      "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_0",          "target": "elevator_0",         "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "mech_auto_lab",     "target": "stairs_0",           "weight": 10, "transport": TRANSPORT_WALK},

    # ── Vertical — Stairs (60 s per floor, bidirectional) ───────────────────
    {"source": "stairs_0", "target": "stairs_1", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_1", "target": "stairs_2", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_2", "target": "stairs_3", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_3", "target": "stairs_4", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_4", "target": "stairs_5", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_5", "target": "stairs_6", "weight": 35, "transport": TRANSPORT_STAIRS},
    {"source": "stairs_6", "target": "stairs_7", "weight": 35, "transport": TRANSPORT_STAIRS},

    # ── Vertical — Elevator (50 s per floor incl. wait, bidirectional) ───────
    {"source": "elevator_0", "target": "elevator_1", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_1", "target": "elevator_2", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_2", "target": "elevator_3", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_3", "target": "elevator_4", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_4", "target": "elevator_5", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_5", "target": "elevator_6", "weight": 30, "transport": TRANSPORT_ELEVATOR},
    {"source": "elevator_6", "target": "elevator_7", "weight": 30, "transport": TRANSPORT_ELEVATOR},

    # ── First Floor internal ─────────────────────────────────────────────────
    {"source": "stairs_1",       "target": "elevator_1",    "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_1",       "target": "store_room",    "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_1",       "target": "seminar_hall_1","weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_1",       "target": "boys_wc_1",     "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_1",       "target": "girls_wc_1",    "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_1",     "target": "seminar_hall_1","weight": 15, "transport": TRANSPORT_WALK},
    {"source": "store_room",     "target": "seminar_hall_1","weight": 10, "transport": TRANSPORT_WALK},

    # ── Second Floor internal ────────────────────────────────────────────────
    {"source": "stairs_2",       "target": "elevator_2",    "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_2",       "target": "seminar_hall_2","weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_2",       "target": "seminar_hall_3","weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_2",       "target": "boys_wc_2",     "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_2",       "target": "girls_wc_2",    "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_2",     "target": "seminar_hall_2","weight": 10, "transport": TRANSPORT_WALK},
    {"source": "seminar_hall_2", "target": "seminar_hall_3","weight": 10, "transport": TRANSPORT_WALK},

    # ── Third Floor internal ─────────────────────────────────────────────────
    {"source": "stairs_3",            "target": "elevator_3",            "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_3",            "target": "boys_common_room_303",  "weight": 15, "transport": TRANSPORT_WALK},
    {"source": "stairs_3",            "target": "boys_wc_3",             "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_3",            "target": "girls_wc_3",            "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_3",          "target": "boys_common_room_303",  "weight": 10, "transport": TRANSPORT_WALK},

    # ── Fourth Floor internal ────────────────────────────────────────────────
    {"source": "stairs_4",       "target": "elevator_4",    "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_4",       "target": "library",       "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_4",       "target": "seminar_hall_4","weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_4",       "target": "boys_wc_4",     "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_4",       "target": "girls_wc_4",    "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_4",     "target": "library",       "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "library",        "target": "seminar_hall_4","weight": 15, "transport": TRANSPORT_WALK},

    # ── Fifth Floor internal ─────────────────────────────────────────────────
    {"source": "stairs_5",   "target": "elevator_5", "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_5",   "target": "room_501",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_5",   "target": "room_502",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_5",   "target": "room_503",   "weight": 15, "transport": TRANSPORT_WALK},
    {"source": "stairs_5",   "target": "boys_wc_5",  "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_5",   "target": "girls_wc_5", "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_5", "target": "room_501",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_501",   "target": "room_502",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_502",   "target": "room_503",   "weight": 10, "transport": TRANSPORT_WALK},

    # ── Sixth Floor internal ─────────────────────────────────────────────────
    {"source": "stairs_6",   "target": "elevator_6", "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "room_601",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "room_602",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "room_603",   "weight": 15, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "ncc_office", "weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "boys_wc_6",  "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_6",   "target": "girls_wc_6", "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_6", "target": "room_601",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_601",   "target": "room_602",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_602",   "target": "room_603",   "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_603",   "target": "ncc_office", "weight": 10, "transport": TRANSPORT_WALK},

    # ── Seventh Floor internal ───────────────────────────────────────────────
    {"source": "stairs_7",   "target": "elevator_7",    "weight": 5, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "room_701",      "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "room_702",      "weight": 15, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "room_703",      "weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "mtech_bvoc_hod","weight": 20, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "boys_wc_7",     "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "stairs_7",   "target": "girls_wc_7",    "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "elevator_7", "target": "room_701",      "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_701",   "target": "room_702",      "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_702",   "target": "room_703",      "weight": 10, "transport": TRANSPORT_WALK},
    {"source": "room_703",   "target": "mtech_bvoc_hod","weight": 10, "transport": TRANSPORT_WALK},
]


# ---------------------------------------------------------------------------
# build_adjacency_list()
# Converts EDGES into an adjacency-list representation used by algorithms.
# ---------------------------------------------------------------------------
def build_adjacency_list(mode: str = "both") -> dict:
    """
    Build an undirected weighted adjacency list from EDGES.

    Parameters
    ----------
    mode : str
        "both"     — include stairs and elevator edges
        "stairs"   — exclude elevator edges  (stairs only for vertical travel)
        "elevator" — exclude stairs edges    (elevator only for vertical travel)

    Returns
    -------
    dict : {node_id: [(neighbour_id, weight, transport), ...]}
    """
    adj: dict = {node_id: [] for node_id in NODES}

    for edge in EDGES:
        t = edge["transport"]
        # Apply mode filter
        if mode == "stairs"   and t == TRANSPORT_ELEVATOR:
            continue
        if mode == "elevator" and t == TRANSPORT_STAIRS:
            continue

        s, d, w = edge["source"], edge["target"], edge["weight"]
        adj[s].append((d, w, t))
        adj[d].append((s, w, t))

    return adj


# ---------------------------------------------------------------------------
# get_graph_for_visualization()
# Returns Vis.js-compatible JSON for the frontend.
# ---------------------------------------------------------------------------
def get_graph_for_visualization() -> dict:
    """Return the full graph as Vis.js nodes + edges payload."""
    vis_nodes = []
    for nid, data in NODES.items():
        fl = data["floor"]
        floor_label = (
            "Outdoor" if fl == -1
            else "Ground Floor" if fl == 0
            else f"Floor {fl}"
        )
        vis_nodes.append({
            "id":          nid,
            "label":       data["short"],
            "title":       f"{data['name']} ({floor_label})",  # tooltip
            "floor":       fl,
            "floor_label": floor_label,
            "type":        data["type"],
            "full_name":   data["name"],
            "x":           data["x"],
            "y":           data["y"],
            "fixed":       {"x": True, "y": True},
            "color": {
                "background":  FLOOR_BG_COLOR.get(fl, "#1a1a2e"),
                "border":      FLOOR_BORDER_COLOR.get(fl, "#00f5d4"),
                "highlight": {
                    "background": "#2a2a4e",
                    "border":     "#ffffff",
                },
                "hover": {
                    "background": "#1e1e3e",
                    "border":     FLOOR_BORDER_COLOR.get(fl, "#00f5d4"),
                },
            },
            "font": {"color": "#e0e0e0", "size": 11},
            "borderWidth": 2,
            "shape": "box",
            "margin": 6,
        })

    vis_edges = []
    for i, edge in enumerate(EDGES):
        t = edge["transport"]
        color_map = {
            TRANSPORT_WALK:     "#555577",
            TRANSPORT_STAIRS:   "#00aa55",
            TRANSPORT_ELEVATOR: "#4488ff",
        }
        vis_edges.append({
            "id":        i,
            "from":      edge["source"],
            "to":        edge["target"],
            "weight":    edge["weight"],
            "transport": t,
            "label":     f"{edge['weight']}s",
            "title":     f"{t.capitalize()} — {edge['weight']}s",
            "color": {
                "color":     color_map.get(t, "#555577"),
                "highlight": "#00f5d4",
                "hover":     "#00f5d4",
            },
            "font":   {"color": "#888888", "size": 9, "align": "middle"},
            "width":  1 if t == TRANSPORT_WALK else 2,
            "dashes": t == TRANSPORT_ELEVATOR,
        })

    return {"nodes": vis_nodes, "edges": vis_edges}