// --- Configuration & State ---
const API_URL = "";
let config = {};
let stats = {};
let selectedNode = null;

// Node Definitions (Static layout for now)
const nodesDef = [
    { id: "timer", label: "PLANIFICADOR", type: "trigger", x: 80, y: 250, icon: "⏱️" },
    { id: "sheet", label: "G. SHEETS", type: "data", x: 350, y: 250, icon: "📊" },
    { id: "ai", label: "INTEL. ARTIFICIAL", type: "process", x: 620, y: 250, icon: "🧠" },
    { id: "fb", label: "FACEBOOK", type: "output", x: 900, y: 150, icon: "📘" },
    { id: "ig", label: "INSTAGRAM", type: "output", x: 900, y: 350, icon: "📸" },
];

const connections = [
    { from: "timer", to: "sheet", id: "conn_timer_sheet" },
    { from: "sheet", to: "ai", id: "conn_sheet_ai" },
    { from: "ai", to: "fb", id: "conn_ai_fb" },
    { from: "ai", to: "ig", id: "conn_ai_ig" }
];

// --- Initialization ---
function init() {
    console.log("Nodes initialization started");
    initGraph();
    startLoops();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}

// --- Graph Rendering ---
function initGraph() {
    const container = document.getElementById('nodes-layer');
    if (!container) {
        console.error("Critical: 'nodes-layer' not found in DOM");
        return;
    }
    container.innerHTML = ''; // Clear prev

    nodesDef.forEach(n => {
        const el = document.createElement('div');
        el.className = 'node';
        el.id = `node-${n.id}`;
        el.style.left = `${n.x}px`;
        el.style.top = `${n.y}px`;

        // Centrar en móviles si es necesario, pero aquí usamos coords fijas

        let ports = '';
        if (n.type !== 'trigger') ports += '<div class="port port-in"></div>';
        if (n.type !== 'output') ports += '<div class="port port-out"></div>';

        el.innerHTML = `
            <div class="node-header"><span class="node-icon">${n.icon}</span> ${n.label}</div>
            <div class="node-body" id="body-${n.id}">Cargando...</div>
            ${ports}
        `;

        el.addEventListener('click', (e) => {
            e.stopPropagation();
            openPanel(n);
        });

        container.appendChild(el);
    });

    drawCables();
    console.log("Graph initialized");
}

function drawCables() {
    const svg = document.getElementById('cables-layer');
    if (!svg) return;
    svg.innerHTML = '';

    connections.forEach(c => {
        const fromNode = nodesDef.find(n => n.id === c.from);
        const toNode = nodesDef.find(n => n.id === c.to);

        const x1 = fromNode.x + 180;
        const y1 = fromNode.y + 45;
        const x2 = toNode.x;
        const y2 = toNode.y + 45;

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const cp1x = x1 + (x2 - x1) / 2;
        const cp2x = x2 - (x2 - x1) / 2;

        const d = `M ${x1} ${y1} C ${cp1x} ${y1}, ${cp2x} ${y2}, ${x2} ${y2}`;

        path.setAttribute("d", d);
        path.setAttribute("class", "cable active");
        path.id = `cable-${c.from}-${c.to}`;

        svg.appendChild(path);
    });

    updateVisualState();
}

// --- Logic ---
async function fetchConfig() {
    try {
        const res = await fetch(`${API_URL}/config`);
        config = await res.json();
        updateVisualState();
    } catch (e) {
        console.warn("Config fetch failed", e);
    }
}

async function fetchStats() {
    try {
        const res = await fetch(`${API_URL}/stats`);
        stats = await res.json();

        document.getElementById('stats-pending').innerText = stats.pending ?? '-';
        if (document.getElementById('body-sheet')) {
            document.getElementById('body-sheet').innerText = `Pendientes: ${stats.pending}\nTotal: ${stats.total}`;
        }
        if (document.getElementById('body-timer')) {
            document.getElementById('body-timer').innerText = "Diario: 10:00 AM";
        }

        if (stats.seconds_remaining) startCountdown(stats.seconds_remaining);
    } catch (e) {
        console.warn("Stats fetch failed", e);
    }
}

function updateVisualState() {
    const nodeStatus = {
        timer: config.timer_enabled,
        sheet: config.sheet_enabled,
        ai: config.ai_enabled,
        fb: config.fb_enabled,
        ig: config.ig_enabled
    };

    nodesDef.forEach(n => {
        const el = document.getElementById(`node-${n.id}`);
        if (!el) return;
        const isActive = nodeStatus[n.id] !== false;

        if (isActive) {
            el.classList.add('active-node');
            el.classList.remove('disabled-node');
        } else {
            el.classList.remove('active-node');
            el.classList.add('disabled-node');
        }
    });

    connections.forEach(c => {
        const path = document.getElementById(`cable-${c.from}-${c.to}`);
        if (!path) return;
        const fromActive = nodeStatus[c.from] !== false;
        const toActive = nodeStatus[c.to] !== false;

        if (fromActive && toActive) {
            path.classList.add('active');
        } else {
            path.classList.remove('active');
        }
    });
}

function toggleNode(nodeId) {
    const key = `${nodeId}_enabled`;
    const newVal = config[key] === false ? true : false;

    config[key] = newVal;
    updateVisualState();

    fetch(`${API_URL}/config`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ [key]: newVal })
    });

    if (selectedNode && selectedNode.id === nodeId) openPanel(selectedNode);
}

// --- Panel ---
const panel = document.getElementById('details-panel');
if (panel) {
    document.getElementById('btn-close-panel').onclick = () => {
        panel.classList.remove('panel-open');
        selectedNode = null;
    };
}

function openPanel(node) {
    selectedNode = node;
    const panelTitle = document.getElementById('panel-title');
    const panelContent = document.getElementById('panel-content');
    const panelBtn = document.getElementById('btn-panel-action');

    panelTitle.innerText = node.label;
    panel.classList.add('panel-open');

    const isEnabled = config[`${node.id}_enabled`] !== false;
    const statusText = isEnabled ? "ACTIVO" : "DESACTIVADO";
    const color = isEnabled ? "#00ff66" : "#ff3333";

    panelContent.innerHTML = `
        <div class="detail-row">
            <span class="detail-label">ESTADO</span>
            <span class="detail-val" style="color:${color}">${statusText}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">TIPO</span>
            <span class="detail-val">${node.type.toUpperCase()}</span>
        </div>
        ${node.id === 'sheet' && stats.next_post ? `
        <div class="next-post-container">
            <span class="detail-label">PRÓXIMA PUBLICACIÓN</span>
            <div class="post-preview-card">
                <div class="post-preview-time">⏰ ${stats.next_post.time || '10:00 AM'}</div>
                <div class="post-preview-caption">${stats.next_post.caption || 'Sin texto'}</div>
                <div class="post-preview-prompt"><b>IA Prompt:</b> ${stats.next_post.prompt || 'Auto-generado'}</div>
            </div>
        </div>
        ` : (node.id === 'ai' && stats.last_image ? `
        <div class="next-post-container">
            <span class="detail-label">ÚLTIMA IMAGEN GENERADA</span>
            <div class="image-preview-card">
                <img src="${stats.last_image}" alt="IA Generation" id="preview-ai-img">
            </div>
        </div>
        ` : `
        <div class="detail-row">
            <span class="detail-label">INFO</span>
            <span class="detail-val">${getNodeInfo(node.id)}</span>
        </div>
        `)}
    `;

    panelBtn.innerText = isEnabled ? "DESACTIVAR NODO" : "ACTIVAR NODO";
    panelBtn.className = isEnabled ? "neon-btn danger" : "neon-btn";
    panelBtn.onclick = () => toggleNode(node.id);
}

function getNodeInfo(id) {
    if (id === 'sheet') return `Columnas: ID, PROMPT, ESTADO...`;
    if (id === 'timer') return "Ejecución diaria programada.";
    if (id === 'ai') return "Generación de imagen con Imagen 4.0";
    return "Servicio de red social.";
}

// --- Countdown ---
let countdownSecs = 0;
function startCountdown(sec) {
    countdownSecs = sec;
}

setInterval(() => {
    if (countdownSecs > 0) {
        countdownSecs--;
        const h = Math.floor(countdownSecs / 3600).toString().padStart(2, '0');
        const m = Math.floor((countdownSecs % 3600) / 60).toString().padStart(2, '0');
        const s = Math.floor(countdownSecs % 60).toString().padStart(2, '0');
        const el = document.getElementById('countdown');
        if (el) el.innerText = `${h}:${m}:${s}`;
    }
}, 1000);

function startLoops() {
    fetchConfig();
    fetchStats();
    setInterval(fetchStats, 10000);
}

// Controls
document.getElementById('btn-run-all').onclick = async () => {
    if (confirm("¿Lanzar ejecución manual ahora?")) {
        await fetch(`${API_URL}/run-now`, { method: 'POST' });
        alert("¡Ejecución enviada!");
    }
};
document.getElementById('btn-refresh').onclick = fetchStats;
