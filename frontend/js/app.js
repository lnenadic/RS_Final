const API_URL = "";

const teamColors = {
    "Tim A": "fill-a",
    "Tim B": "fill-b",
    "Tim C": "fill-c"
};

async function castVote(teamName) {
    const statusDiv = document.getElementById('status-message');
    statusDiv.innerHTML = "⏳ Šaljem glas...";
    statusDiv.style.color = "#555";

    try {
        const response = await fetch(`${API_URL}/vote`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ option: teamName })
        });

        const data = await response.json();

        if (response.ok) {
            statusDiv.innerHTML = `
                <span style="color: green; font-weight: bold;">✅ Glas zabilježen!</span><br>
                <small style="color: #666;">Zahtjev obradio server: <b>${data.processed_by}</b></small>
            `;

            fetchResults();
        } else {
            statusDiv.textContent = "❌ Greška: " + (data.detail || "Nepoznato");
            statusDiv.style.color = "red";
        }
    } catch (error) {
        console.error(error);
        statusDiv.innerHTML = "⚠️ Backend nije dostupan.<br><small>Jesi li pokrenuo docker-compose?</small>";
        statusDiv.style.color = "orange";
    }
}

async function fetchResults() {
    try {
        const response = await fetch(`${API_URL}/results`);
        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error("Greška pri dohvatu rezultata:", error);
    }
}

function renderResults(data) {
    const resultsList = document.getElementById('results-list');
    const totalCountSpan = document.getElementById('total-count');

    let totalVotes = Object.values(data).reduce((a, b) => a + b, 0);
    totalCountSpan.textContent = totalVotes;

    let html = "";
    const allTeams = ["Tim A", "Tim B", "Tim C"];

    allTeams.forEach(team => {
        const count = data[team] || 0;
        const percentage = totalVotes === 0 ? 0 : Math.round((count / totalVotes) * 100);
        const colorClass = teamColors[team] || "fill-a";

        html += `
            <div class="result-item">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <strong>${team}</strong>
                    <span>${count} (${percentage}%)</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill ${colorClass}" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    });

    resultsList.innerHTML = html;
}

window.onload = fetchResults;
setInterval(fetchResults, 5000);