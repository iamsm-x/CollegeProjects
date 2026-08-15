/**
 * app.js — TCOE Campus Navigation Frontend
 * ==========================================
 * Simple Floor-by-Floor Room List Navigation Engine
 *
 * Responsibilities:
 *   1. Render a clean, clickable room list per floor (Outdoor, GF, 1F..7F).
 *   2. Let users tap a room to set it as source / destination.
 *   3. Highlight source, destination, and path rooms in the list.
 *   4. Multi-floor transition alerts & floor selector toolbar.
 *   5. Dijkstra's & A* algorithm comparisons & turn-by-turn navigation steps.
 */

"use strict";

const API_BASE =
  window.location.port === "8000"
    ? ""
    : "http://127.0.0.1:8000";

/* ──────────────────────────────────────────────────────────────
   DOM references
   ────────────────────────────────────────────────────────────── */

const $ = (id) =>
  document.getElementById(id);

const $$ = (sel) =>
  document.querySelectorAll(sel);

const DOM = {
  graphCanvas: $("graph-canvas"),
  graphLoader: $("graph-loader"),
  graphStatus: $("graph-status-msg"),

  sourceSelect: $("source-select"),
  destSelect: $("dest-select"),

  swapBtn: $("swap-btn"),
  findBtn: $("find-btn"),

  overlay: $("overlay"),
  toast: $("toast"),

  algoGroup: $("algo-radio-group"),
  modeGroup: $("mode-btn-group"),

  legendFloors: $("legend-floors"),

  floorTabs: $("floor-tabs"),
  floorTitle: $("floor-title"),
  floorBadge: $("floor-badge"),

  transitionBar: $("floor-transition-bar"),
  ftMsg: $("ft-msg"),
  ftBtn: $("ft-btn"),

  roomList: $("room-list"),

  scTimeVal: $("sc-time-val"),
  scHopsVal: $("sc-hops-val"),

  cmpBlock: $("cmp-block"),

  cdCost: $("cd-cost"),
  caCost: $("ca-cost"),

  cdNodes: $("cd-nodes"),
  caNodes: $("ca-nodes"),

  cdTime: $("cd-time"),
  caTime: $("ca-time"),

  cdLen: $("cd-len"),
  caLen: $("ca-len"),

  effNote: $("efficiency-note"),

  dirBlock: $("dir-block"),
  dirTitle: $("dir-title"),
  dirList: $("dir-list"),

  btnReset: $("btn-reset"),
};


/* ──────────────────────────────────────────────────────────────
   Application state
   ────────────────────────────────────────────────────────────── */

let graphData = null;

let currentFloor = 0;

let selectedAlgo = "both";

let selectedMode = "both";

let currentPathIds = [];


/* ──────────────────────────────────────────────────────────────
   Floor definitions
   ────────────────────────────────────────────────────────────── */

const FLOORS = [
  {
    id: -1,
    name: "Outdoor Campus Areas",
    short: "Outdoor",
    badge: "Grounds"
  },

  {
    id: 0,
    name: "Ground Floor",
    short: "GF",
    badge: "Level 0"
  },

  {
    id: 1,
    name: "First Floor",
    short: "1F",
    badge: "Level 1"
  },

  {
    id: 2,
    name: "Second Floor",
    short: "2F",
    badge: "Level 2"
  },

  {
    id: 3,
    name: "Third Floor",
    short: "3F",
    badge: "Level 3"
  },

  {
    id: 4,
    name: "Fourth Floor",
    short: "4F",
    badge: "Level 4"
  },

  {
    id: 5,
    name: "Fifth Floor",
    short: "5F",
    badge: "Level 5"
  },

  {
    id: 6,
    name: "Sixth Floor",
    short: "6F",
    badge: "Level 6"
  },

  {
    id: 7,
    name: "Seventh Floor",
    short: "7F",
    badge: "Level 7"
  }
];


/* ──────────────────────────────────────────────────────────────
   Floor colours
   ────────────────────────────────────────────────────────────── */

const FLOOR_COLORS = {
  "-1": "#2e9e5b",
  "0": "#3fae6a",
  "1": "#6bbf5b",
  "2": "#8bd17e",
  "3": "#4faa8a",
  "4": "#5cb896",
  "5": "#7bc47a",
  "6": "#48a878",
  "7": "#2f8f5e"
};


/* ──────────────────────────────────────────────────────────────
   Toast notification
   ────────────────────────────────────────────────────────────── */

let toastTimer = null;


function showToast(msg, type = "info") {
  DOM.toast.textContent = msg;

  DOM.toast.className =
    `toast ${type} show`;

  clearTimeout(toastTimer);

  toastTimer = setTimeout(() => {
    DOM.toast.className = "toast";
  }, 3000);
}


function showOverlay() {
  DOM.overlay.style.display = "flex";
}


function hideOverlay() {
  DOM.overlay.style.display = "none";
}


function formatTime(seconds) {
  if (seconds < 0) {
    return "N/A";
  }

  if (seconds < 60) {
    return `${seconds}s`;
  }

  const minutes =
    Math.floor(seconds / 60);

  const remainingSeconds =
    Math.round(seconds % 60);

  return remainingSeconds > 0
    ? `${minutes}m ${remainingSeconds}s`
    : `${minutes}m`;
}


/* ──────────────────────────────────────────────────────────────
   Build Legend
   ────────────────────────────────────────────────────────────── */

function buildLegend() {
  DOM.legendFloors.innerHTML =
    FLOORS.map(floor => `
      <div
        class="lf-item"
        style="cursor:pointer;"
        onclick="switchFloor(${floor.id})"
      >
        <span
          class="lf-dot"
          style="
            background:${FLOOR_COLORS[floor.id]};
            box-shadow:0 0 5px ${FLOOR_COLORS[floor.id]}55;
          "
        ></span>

        ${floor.short} — ${floor.name}
      </div>
    `).join("");
}


/* ──────────────────────────────────────────────────────────────
   Build floor tabs
   ────────────────────────────────────────────────────────────── */

function buildFloorTabs() {
  DOM.floorTabs.innerHTML =
    FLOORS.map(floor => `
      <button
        class="floor-tab ${
          floor.id === currentFloor
            ? "active"
            : ""
        }"
        id="ftab-${floor.id}"
        data-floor="${floor.id}"
      >
        <span>${floor.short}</span>

        <span
          class="tab-badge"
          id="tbadge-${floor.id}"
        >
          0
        </span>
      </button>
    `).join("");


  DOM.floorTabs.addEventListener(
    "click",
    event => {

      const button =
        event.target.closest(
          ".floor-tab"
        );

      if (!button) {
        return;
      }

      const floorId =
        parseInt(
          button.dataset.floor,
          10
        );

      switchFloor(floorId);
    }
  );
}


/* ──────────────────────────────────────────────────────────────
   Update floor badges
   ────────────────────────────────────────────────────────────── */

function updateFloorTabBadges() {
  if (!graphData) {
    return;
  }

  const pathSet =
    new Set(currentPathIds);


  FLOORS.forEach(floor => {

    const nodesOnFloor =
      graphData.nodes.filter(
        node =>
          node.floor === floor.id
      );


    const countElement =
      $(`tbadge-${floor.id}`);


    const tabElement =
      $(`ftab-${floor.id}`);


    if (countElement) {
      countElement.textContent =
        nodesOnFloor.length;
    }


    if (tabElement) {

      const hasPathNode =
        nodesOnFloor.some(
          node =>
            pathSet.has(node.id)
        );


      if (
        hasPathNode &&
        currentPathIds.length > 0
      ) {
        tabElement.classList.add(
          "has-path"
        );
      } else {
        tabElement.classList.remove(
          "has-path"
        );
      }
    }
  });
}


/* ──────────────────────────────────────────────────────────────
   Floor switcher
   ────────────────────────────────────────────────────────────── */

function switchFloor(floorNum) {

  currentFloor = floorNum;


  const floorMeta =
    FLOORS.find(
      floor =>
        floor.id === floorNum
    ) || FLOORS[1];


  DOM.floorTitle.textContent =
    `${floorMeta.name} Rooms`;


  DOM.floorBadge.textContent =
    floorMeta.badge;


  DOM.floorBadge.style.color =
    FLOOR_COLORS[floorNum] ||
    "#2e9e5b";


  $$(".floor-tab").forEach(
    tab =>
      tab.classList.remove(
        "active"
      )
  );


  const activeTab =
    $(`ftab-${floorNum}`);


  if (activeTab) {
    activeTab.classList.add(
      "active"
    );
  }


  renderRoomList();
}


/* ──────────────────────────────────────────────────────────────
   Load locations
   ────────────────────────────────────────────────────────────── */

async function loadLocations() {

  try {

    const response =
      await fetch(
        `${API_BASE}/api/locations`
      );


    const data =
      await response.json();


    const buildOptions =
      select => {

        while (
          select.options.length > 1
        ) {
          select.remove(1);
        }


        data.floors.forEach(
          floor => {

            const group =
              document.createElement(
                "optgroup"
              );


            group.label =
              floor.label;


            floor.locations.forEach(
              location => {

                const option =
                  new Option(
                    location.name,
                    location.id
                  );


                group.appendChild(
                  option
                );
              }
            );


            select.appendChild(
              group
            );
          }
        );
      };


    buildOptions(
      DOM.sourceSelect
    );


    buildOptions(
      DOM.destSelect
    );

  } catch (error) {

    console.error(
      "Failed to load locations:",
      error
    );


    showToast(
      "Could not load location list.",
      "error"
    );
  }
}


/* ──────────────────────────────────────────────────────────────
   Load graph
   ────────────────────────────────────────────────────────────── */

async function loadGraph() {

  try {

    const response =
      await fetch(
        `${API_BASE}/api/graph`
      );


    graphData =
      await response.json();


    DOM.graphLoader.style.display =
      "none";


    updateFloorTabBadges();

    renderRoomList();

  } catch (error) {

    console.error(
      "Failed to load graph:",
      error
    );


    DOM.graphLoader.innerHTML =
      "<p style='color:#e05a5a'>Failed to load campus rooms. Server running?</p>";


    showToast(
      "Server connection failed.",
      "error"
    );
  }
}


/* ──────────────────────────────────────────────────────────────
   Room list
   ────────────────────────────────────────────────────────────── */

function renderRoomList() {

  if (!graphData) {
    return;
  }


  const nodesOnFloor =
    graphData.nodes.filter(
      node =>
        node.floor === currentFloor
    );


  const pathSet =
    new Set(currentPathIds);


  const sourceId =
    DOM.sourceSelect.value;


  const destinationId =
    DOM.destSelect.value;


  if (nodesOnFloor.length === 0) {

    DOM.roomList.innerHTML = `
      <div class="empty-state">
        <p>No rooms on this floor.</p>
      </div>
    `;


    checkFloorTransitions();

    return;
  }


  DOM.roomList.innerHTML =
    nodesOnFloor.map(node => {

      const isSource =
        node.id === sourceId;


      const isDestination =
        node.id === destinationId;


      const isOnPath =
        pathSet.has(node.id);


      let classes =
        "room-card";


      if (isSource) {
        classes +=
          " is-source";
      }


      if (isDestination) {
        classes +=
          " is-dest";
      }


      if (isOnPath) {
        classes +=
          " is-on-path";
      }


      let tag = "";


      if (isSource) {

        tag =
          '<span class="rc-tag">START</span>';

      } else if (isDestination) {

        tag =
          '<span class="rc-tag">FINISH</span>';

      } else if (isOnPath) {

        tag =
          '<span class="rc-tag">ON ROUTE</span>';
      }


      return `
        <div
          class="${classes}"
          data-id="${node.id}"
          data-name="${node.full_name}"
        >

          <div class="rc-text">

            <div class="rc-name">
              ${node.full_name}
            </div>

            <div class="rc-type">
              ${node.type}
            </div>

          </div>

          ${tag}

        </div>
      `;

    }).join("");


  $$(".room-card").forEach(
    element => {

      element.addEventListener(
        "click",
        () => {

          const nodeId =
            element.dataset.id;


          const nodeName =
            element.dataset.name;


          if (
            !DOM.sourceSelect.value
          ) {

            DOM.sourceSelect.value =
              nodeId;


            showToast(
              `Source set: ${nodeName}`,
              "success"
            );

          } else if (
            !DOM.destSelect.value
          ) {

            DOM.destSelect.value =
              nodeId;


            showToast(
              `Destination set: ${nodeName}`,
              "success"
            );

          } else {

            DOM.sourceSelect.value =
              nodeId;


            DOM.destSelect.value =
              "";


            showToast(
              `New source: ${nodeName}`,
              "info"
            );
          }


          renderRoomList();
        }
      );


      element.addEventListener(
        "mouseenter",
        () => {

          DOM.graphStatus.textContent =
            `${element.dataset.name} · Click to select as start or destination`;
        }
      );


      element.addEventListener(
        "mouseleave",
        () => {

          DOM.graphStatus.textContent =
            "Click any room below to select it as your starting point or destination";
        }
      );
    }
  );


  checkFloorTransitions();
}


/* ──────────────────────────────────────────────────────────────
   Check whether an edge belongs to path
   ────────────────────────────────────────────────────────────── */

function isEdgeInPath(u, v) {

  if (
    currentPathIds.length < 2
  ) {
    return false;
  }


  for (
    let i = 0;
    i < currentPathIds.length - 1;
    i++
  ) {

    const a =
      currentPathIds[i];


    const b =
      currentPathIds[i + 1];


    if (
      (a === u && b === v) ||
      (a === v && b === u)
    ) {
      return true;
    }
  }


  return false;
}


/* ──────────────────────────────────────────────────────────────
   Multi-floor transition
   ────────────────────────────────────────────────────────────── */

function checkFloorTransitions() {

  if (
    currentPathIds.length === 0 ||
    !graphData
  ) {

    DOM.transitionBar.style.display =
      "none";

    return;
  }


  const pathNodes =
    currentPathIds
      .map(
        id =>
          graphData.nodes.find(
            node =>
              node.id === id
          )
      )
      .filter(Boolean);


  const floorsInPath =
    Array.from(
      new Set(
        pathNodes.map(
          node =>
            node.floor
        )
      )
    );


  if (
    floorsInPath.length <= 1
  ) {

    DOM.transitionBar.style.display =
      "none";

    return;
  }


  const nextNodeOnOtherFloor =
    pathNodes.find(
      node =>
        node.floor !== currentFloor
    );


  if (
    nextNodeOnOtherFloor
  ) {

    const targetFloor =
      FLOORS.find(
        floor =>
          floor.id ===
          nextNodeOnOtherFloor.floor
      );


    DOM.transitionBar.style.display =
      "flex";


    DOM.ftMsg.innerHTML =
      `Multi-floor route. Route continues on <strong>${
        targetFloor
          ? targetFloor.name
          : "Floor " +
            nextNodeOnOtherFloor.floor
      }</strong>`;


    DOM.ftBtn.onclick =
      () =>
        switchFloor(
          nextNodeOnOtherFloor.floor
        );

  } else {

    DOM.transitionBar.style.display =
      "none";
  }
}


/* ──────────────────────────────────────────────────────────────
   Highlight path
   ────────────────────────────────────────────────────────────── */

function highlightPath(
  pathNodeIds
) {

  currentPathIds =
    pathNodeIds;


  updateFloorTabBadges();


  if (
    pathNodeIds.length > 0 &&
    graphData
  ) {

    const startNode =
      graphData.nodes.find(
        node =>
          node.id ===
          pathNodeIds[0]
      );


    if (startNode) {

      switchFloor(
        startNode.floor
      );

    } else {

      renderRoomList();
    }
  }
}


/* ──────────────────────────────────────────────────────────────
   Reset
   ────────────────────────────────────────────────────────────── */

function resetGraph() {

  currentPathIds = [];


  updateFloorTabBadges();


  renderRoomList();


  DOM.scTimeVal.textContent =
    "—";


  DOM.scHopsVal.textContent =
    "—";


  DOM.cmpBlock.style.display =
    "none";


  DOM.dirList.innerHTML = `
    <div class="empty-state">
      <p>
        Select a <strong>source</strong> and
        <strong>destination</strong>, then click
        <strong>Find Shortest Path</strong>
        to see route.
      </p>
    </div>
  `;


  DOM.dirTitle.textContent =
    "Navigation Directions";


  showToast(
    "Path cleared",
    "info"
  );
}


/* ──────────────────────────────────────────────────────────────
   Directions
   ────────────────────────────────────────────────────────────── */

function renderDirections(
  directions,
  srcName,
  dstName,
  algo
) {

  DOM.dirTitle.textContent =
    `Directions (${
      algo === "astar"
        ? "A*"
        : "Dijkstra's"
    })`;


  const steps = [

    {
      text:
        `Start at ${srcName}`,

      cls:
        "start-step"
    },


    ...directions.map(
      direction => {

        let cls =
          "walk-step";


        if (
          direction.includes(
            "stairs"
          )
        ) {
          cls =
            "stairs-step";
        }


        if (
          direction.includes(
            "elevator"
          )
        ) {
          cls =
            "elevator-step";
        }


        return {
          text: direction,
          cls
        };
      }
    ),


    {
      text:
        `Arrive at ${dstName}`,

      cls:
        "dest-step"
    }

  ];


  DOM.dirList.innerHTML =
    steps.map(
      (step, index) => `
        <div
          class="dir-step ${step.cls}"
        >

          <span class="step-num">
            ${index + 1}
          </span>

          <span>
            ${step.text}
          </span>

        </div>
      `
    ).join("");
}


/* ──────────────────────────────────────────────────────────────
   Algorithm comparison
   ────────────────────────────────────────────────────────────── */

function renderComparison(
  dijkstraResult,
  astarResult
) {

  DOM.cmpBlock.style.display =
    "block";


  const fillResult =
    (result, prefix) => {

      if (!result) {

        $(`c${prefix}-cost`)
          .textContent = "N/A";

        $(`c${prefix}-nodes`)
          .textContent = "N/A";

        $(`c${prefix}-time`)
          .textContent = "N/A";

        $(`c${prefix}-len`)
          .textContent = "N/A";

        return;
      }


      $(`c${prefix}-cost`)
        .textContent =
        result.found
          ? `${result.total_time_seconds}s`
          : "No path";


      $(`c${prefix}-nodes`)
        .textContent =
        result.found
          ? result.nodes_explored
          : "—";


      $(`c${prefix}-time`)
        .textContent =
        result.found
          ? `${result.compute_time_us.toFixed(1)}µs`
          : "—";


      $(`c${prefix}-len`)
        .textContent =
        result.found
          ? `${result.path.length} nodes`
          : "—";
    };


  fillResult(
    dijkstraResult,
    "d"
  );


  fillResult(
    astarResult,
    "a"
  );


  if (
    dijkstraResult?.found &&
    astarResult?.found
  ) {

    const saved =
      dijkstraResult.nodes_explored -
      astarResult.nodes_explored;


    const pct =
      dijkstraResult.nodes_explored > 0
        ? Math.round(
            (
              saved /
              dijkstraResult.nodes_explored
            ) * 100
          )
        : 0;


    if (saved > 0) {

      DOM.effNote.textContent =
        `A* explored ${saved} fewer nodes (${pct}% more efficient)`;

    } else if (saved === 0) {

      DOM.effNote.textContent =
        "Both algorithms explored the same optimal path";

    } else {

      DOM.effNote.textContent =
        "Both algorithms explored optimal paths";
    }

  } else {

    DOM.effNote.textContent =
      "";
  }
}


/* ──────────────────────────────────────────────────────────────
   Find shortest path
   ────────────────────────────────────────────────────────────── */

async function findPath() {

  const source =
    DOM.sourceSelect.value;


  const destination =
    DOM.destSelect.value;


  if (!source) {

    showToast(
      "Please select a starting location.",
      "error"
    );

    return;
  }


  if (!destination) {

    showToast(
      "Please select a destination.",
      "error"
    );

    return;
  }


  if (
    source === destination
  ) {

    showToast(
      "Source and destination must be different.",
      "error"
    );

    return;
  }


  showOverlay();


  try {

    const response =
      await fetch(
        `${API_BASE}/api/shortest-path`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({
            source,
            destination,
            algorithm:
              selectedAlgo,
            mode:
              selectedMode
          })
        }
      );


    if (!response.ok) {

      const error =
        await response.json();


      throw new Error(
        error.detail ||
        "Server error"
      );
    }


    const data =
      await response.json();


    const primary =
      data.dijkstra ||
      data.astar;


    if (
      !primary?.found
    ) {

      const errorMessage =
        primary?.error ||
        "No path found.";


      showToast(
        errorMessage,
        "error"
      );


      hideOverlay();


      DOM.dirList.innerHTML = `
        <div class="empty-state">
          <p style="color:#ff8888">
            ${errorMessage}
          </p>
        </div>
      `;


      return;
    }


    DOM.scTimeVal.textContent =
      formatTime(
        primary.total_time_seconds
      );


    DOM.scHopsVal.textContent =
      primary.path.length;


    highlightPath(
      primary.path
    );


    const directionResult =
      data.astar ||
      data.dijkstra;


    renderDirections(
      directionResult.directions,
      data.source_name,
      data.destination_name,
      selectedAlgo === "astar"
        ? "astar"
        : "dijkstra"
    );


    if (
      selectedAlgo === "both"
    ) {

      renderComparison(
        data.dijkstra,
        data.astar
      );

    } else {

      DOM.cmpBlock.style.display =
        "none";
    }


    showToast(
      `Route Calculated! ${formatTime(
        primary.total_time_seconds
      )} · ${primary.path.length} stops`,
      "success"
    );

  } catch (error) {

    console.error(
      "findPath error:",
      error
    );


    showToast(
      error.message,
      "error"
    );

  } finally {

    hideOverlay();
  }
}


/* ──────────────────────────────────────────────────────────────
   UI event listeners
   ────────────────────────────────────────────────────────────── */

DOM.swapBtn.addEventListener(
  "click",
  () => {

    const temporary =
      DOM.sourceSelect.value;


    DOM.sourceSelect.value =
      DOM.destSelect.value;


    DOM.destSelect.value =
      temporary;


    showToast(
      "Source and destination swapped",
      "info"
    );


    renderRoomList();
  }
);


DOM.findBtn.addEventListener(
  "click",
  findPath
);


document.addEventListener(
  "keydown",
  event => {

    if (
      event.key === "Enter" &&
      DOM.overlay.style.display !== "flex"
    ) {

      findPath();
    }
  }
);


DOM.algoGroup.addEventListener(
  "click",
  event => {

    const label =
      event.target.closest(
        ".radio-opt"
      );


    if (!label) {
      return;
    }


    $$(".radio-opt").forEach(
      item =>
        item.classList.remove(
          "selected"
        )
    );


    label.classList.add(
      "selected"
    );


    label.querySelector(
      "input"
    ).checked = true;


    selectedAlgo =
      label.dataset.value;
  }
);


DOM.modeGroup.addEventListener(
  "click",
  event => {

    const button =
      event.target.closest(
        ".mode-btn"
      );


    if (!button) {
      return;
    }


    $$(".mode-btn").forEach(
      item =>
        item.classList.remove(
          "active"
        )
    );


    button.classList.add(
      "active"
    );


    selectedMode =
      button.dataset.mode;


    showToast(
      `Transport mode: ${selectedMode}`,
      "info"
    );
  }
);


DOM.btnReset.addEventListener(
  "click",
  resetGraph
);


/* ──────────────────────────────────────────────────────────────
   Theme toggle
   ────────────────────────────────────────────────────────────── */

const themeToggleBtn =
  $("theme-toggle");


function applyTheme(theme) {

  document.body.setAttribute(
    "data-theme",
    theme
  );


  themeToggleBtn.setAttribute(
    "aria-pressed",
    theme === "dark"
      ? "true"
      : "false"
  );


  themeToggleBtn.title =
    theme === "dark"
      ? "Switch to light mode"
      : "Switch to dark mode";


  localStorage.setItem(
    "tcoe-theme",
    theme
  );
}


function initTheme() {

  const saved =
    localStorage.getItem(
      "tcoe-theme"
    );


  const preferDark =
    window.matchMedia &&
    window.matchMedia(
      "(prefers-color-scheme: dark)"
    ).matches;


  applyTheme(
    saved ||
    (
      preferDark
        ? "dark"
        : "light"
    )
  );
}


themeToggleBtn.addEventListener(
  "click",
  () => {

    const next =
      document.body.getAttribute(
        "data-theme"
      ) === "dark"
        ? "light"
        : "dark";


    applyTheme(next);
  }
);


/* ──────────────────────────────────────────────────────────────
   Initialise
   ────────────────────────────────────────────────────────────── */

(async function init() {

  initTheme();

  buildLegend();

  buildFloorTabs();

  await Promise.all([
    loadGraph(),
    loadLocations()
  ]);

})();