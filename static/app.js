const API_URL = ""; // Relative

// Clock
function updateClock() {
    const now = new Date();
    document.getElementById('clock').innerText = now.toLocaleTimeString();
}
setInterval(updateClock, 1000);

// Fetch Data
async function refreshData() {
    try {
        // Posts
        const resStats = await fetch(`${API_URL}/posts`);
        const posts = await resStats.json();

        // Count
        const pending = posts.filter(p => p.status === 'PENDIENTE').length;
        const published = posts.filter(p => p.status === 'PUBLICADO').length;

        document.getElementById('count-pending').innerText = pending;
        document.getElementById('count-published').innerText = published;

        // Table
        const tbody = document.getElementById('posts-table-body');
        tbody.innerHTML = '';

        // Limit to 20 for performance
        posts.slice(0, 20).forEach(p => {
            const tr = document.createElement('tr');

            // Status Color
            let statusColor = '#fff';
            if (p.status === 'PENDIENTE') statusColor = '#ffff00';
            if (p.status === 'PUBLICADO') statusColor = '#00ff00';
            if (p.status && p.status.includes('ERROR')) statusColor = '#ff0000';

            tr.innerHTML = `
                <td>#${p.id}</td>
                <td>${p.time || '-'}</td>
                <td>${p.prompt ? p.prompt.substring(0, 40) + '...' : ''}</td>
                <td style="color: ${statusColor}">${p.status}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (e) {
        console.error("Fetch error", e);
    }
}

// Logs
async function refreshLogs() {
    try {
        const res = await fetch(`${API_URL}/logs`);
        const data = await res.json();
        const term = document.getElementById('log-terminal');
        term.innerHTML = data.logs.join('<br>');
        term.scrollTop = term.scrollHeight;
    } catch (e) {
        console.error("Log error", e);
    }
}

// Manual Run
document.getElementById('btn-run-now').addEventListener('click', async () => {
    if (confirm('¿Launch immediate execution?')) {
        await fetch(`${API_URL}/run-now`, { method: 'POST' });
        alert('Command sent. Check logs.');
    }
});

// Init
setInterval(refreshData, 5000);
setInterval(refreshLogs, 3000);
refreshData();
refreshLogs();
