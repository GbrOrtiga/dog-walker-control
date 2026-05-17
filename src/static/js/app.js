/**
 * 🐾 DOG WALKER CONTROL - Frontend JavaScript
 * Gerencia interações com a API e a interface do usuário
 */

const PRICE_PER_WALK = 25.0;
let config = {};
let allWalks = [];
let selectedDays = [];

// ══════════════════════════════════════════════════════════════════════
// INICIALIZAÇÃO
// ══════════════════════════════════════════════════════════════════════

document.addEventListener("DOMContentLoaded", () => {
    initializeApp();
    setupEventListeners();
});

async function initializeApp() {
    try {
        // Carregar configurações
        const response = await fetch("/api/config");
        const result = await response.json();
        config = result;

        // Carregar dados iniciais
        loadDashboard();
        loadWalks();
    } catch (error) {
        console.error("Erro ao inicializar:", error);
        showToast("Erro ao carregar configurações", "error");
    }
}

// ══════════════════════════════════════════════════════════════════════
// EVENT LISTENERS
// ══════════════════════════════════════════════════════════════════════

function setupEventListeners() {
    // Tabs
    document.querySelectorAll(".tab-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            const tabName = e.target.getAttribute("data-tab");
            switchTab(tabName);
        });
    });

    // Form Register
    document.getElementById("formAddWalk")?.addEventListener("submit", handleAddWalk);

    // Days Selection
    document.querySelectorAll(".day-checkbox input").forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            validateDaysSelection();
            updateEstimatedValue();
        });
    });

    // Walks Per Day
    document.getElementById("walksPerDay")?.addEventListener("change", updateEstimatedValue);

    // Search
    document.getElementById("searchOwner")?.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            searchOwner();
        }
    });
}

// ══════════════════════════════════════════════════════════════════════
// TAB MANAGEMENT
// ══════════════════════════════════════════════════════════════════════

function switchTab(tabName) {
    // Remove active class from all tabs
    document.querySelectorAll(".tab-content").forEach((tab) => {
        tab.classList.remove("active");
    });
    document.querySelectorAll(".tab-btn").forEach((btn) => {
        btn.classList.remove("active");
    });

    // Add active class to selected tab
    document.getElementById(tabName)?.classList.add("active");
    document.querySelector(`[data-tab="${tabName}"]`)?.classList.add("active");

    // Load data for specific tabs
    if (tabName === "schedule") {
        loadSchedule();
    } else if (tabName === "list") {
        loadWalks();
    }
}

// ══════════════════════════════════════════════════════════════════════
// DASHBOARD
// ══════════════════════════════════════════════════════════════════════

async function loadDashboard() {
    try {
        const { data: walks } = await fetchAPI("/api/walks");
        const { total } = await fetchAPI("/api/total");
        const { data: schedule } = await fetchAPI("/api/schedule");

        // Update total revenue
        document.getElementById("totalRevenue").textContent = formatCurrency(total);
        document.getElementById("totalWalks").textContent = `${walks.length} passeios registrados`;

        // Update quick info
        updateQuickInfo(walks);

        // Update week preview
        updateWeekPreview(schedule);

        allWalks = walks;
    } catch (error) {
        console.error("Erro ao carregar dashboard:", error);
    }
}

function updateQuickInfo(walks) {
    const container = document.getElementById("quickInfo");
    if (!walks || walks.length === 0) {
        container.innerHTML = "<li>Nenhum passeio registrado</li>";
        return;
    }

    const owners = new Set(walks.map((w) => w.owner_name)).size;
    const dogs = new Set(walks.map((w) => w.dog_name)).size;
    const totalValue = walks.reduce((sum, w) => sum + w.total, 0);

    container.innerHTML = `
        <li><strong>Donos:</strong> ${owners}</li>
        <li><strong>Cães:</strong> ${dogs}</li>
        <li><strong>Total:</strong> ${formatCurrency(totalValue)}</li>
    `;
}

function updateWeekPreview(schedule) {
    const container = document.getElementById("weekPreview");
    if (!schedule || Object.keys(schedule).length === 0) {
        container.innerHTML = "<p>Nenhum passeio agendado</p>";
        return;
    }

    let html = "";
    Object.entries(schedule).forEach(([day, walks]) => {
        if (walks.length > 0) {
            const dayTotal = walks.reduce((sum, w) => sum + (w.walks_per_day || 1), 0);
            html += `
                <div class="day-card">
                    <h4>${getDayAbbrev(day)}</h4>
                    <div class="day-info">
                        ${dayTotal} passeio(s) – R$ ${(dayTotal * PRICE_PER_WALK).toFixed(2)}
                    </div>
                    ${walks
                        .map(
                            (w) => `
                        <div class="dog-item">
                            <div class="dog-item-name">🐕 ${w.dog_name}</div>
                            <div class="dog-item-owner">${w.owner_name}</div>
                        </div>
                    `
                        )
                        .join("")}
                </div>
            `;
        }
    });

    container.innerHTML = html;
}

// ══════════════════════════════════════════════════════════════════════
// REGISTER WALK FORM
// ══════════════════════════════════════════════════════════════════════

async function handleAddWalk(e) {
    e.preventDefault();

    // Get form values
    const dogName = document.getElementById("dogName").value.trim();
    const ownerName = document.getElementById("ownerName").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const walksPerDay = parseInt(document.getElementById("walksPerDay").value);

    // Get selected days
    const daysCheckboxes = document.querySelectorAll(".day-checkbox input:checked");
    const daysOfWeek = Array.from(daysCheckboxes).map((cb) => cb.value);

    // Validate
    if (!dogName || !ownerName || daysOfWeek.length === 0) {
        showToast("Preencha todos os campos obrigatórios", "warning");
        return;
    }

    if (daysOfWeek.length > 5) {
        showToast("Máximo de 5 dias da semana", "warning");
        return;
    }

    try {
        const response = await fetch("/api/walks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                dog_name: dogName,
                owner_name: ownerName,
                phone: phone,
                walks_per_day: walksPerDay,
                days_of_week: daysOfWeek,
            }),
        });

        const result = await response.json();

        if (result.success) {
            showToast(`✅ ${dogName} registrado com sucesso!`, "success");
            document.getElementById("formAddWalk").reset();
            selectedDays = [];
            updateCheckboxDisplay();
            updateEstimatedValue();
            loadDashboard();
        } else {
            showToast(`Erro: ${result.error}`, "error");
        }
    } catch (error) {
        console.error("Erro ao registrar passeio:", error);
        showToast("Erro ao registrar passeio", "error");
    }
}

function validateDaysSelection() {
    const checkboxes = document.querySelectorAll(".day-checkbox input");
    const checkedCount = document.querySelectorAll(".day-checkbox input:checked").length;
    const maxDays = 5;

    // Disable unchecked boxes if max reached
    checkboxes.forEach((cb) => {
        if (!cb.checked && checkedCount >= maxDays) {
            cb.disabled = true;
        } else {
            cb.disabled = false;
        }
    });

    // Update help text
    document.getElementById("daysHelp").textContent = `Dias selecionados: ${checkedCount}/${maxDays}`;
}

function updateEstimatedValue() {
    const walksPerDay = parseInt(document.getElementById("walksPerDay").value) || 1;
    const selectedDaysCount = document.querySelectorAll(".day-checkbox input:checked").length;
    const total = walksPerDay * selectedDaysCount * PRICE_PER_WALK;

    document.getElementById("estimatedValue").textContent = `Valor estimado: ${formatCurrency(total)}`;
}

function updateCheckboxDisplay() {
    // Update visual state of checkboxes
    validateDaysSelection();
}

// ══════════════════════════════════════════════════════════════════════
// LIST WALKS
// ══════════════════════════════════════════════════════════════════════

async function loadWalks() {
    try {
        const { data: walks } = await fetchAPI("/api/walks");

        if (!walks || walks.length === 0) {
            document.getElementById("walksListContainer").innerHTML =
                "<p>Nenhum passeio registrado</p>";
            return;
        }

        let html = `
            <table>
                <thead>
                    <tr>
                        <th>🐕 Cachorro</th>
                        <th>👤 Dono</th>
                        <th>📱 Telefone</th>
                        <th>📅 Dias</th>
                        <th>🔢 Pass/dia</th>
                        <th>💰 Total</th>
                        <th>⚙️ Ação</th>
                    </tr>
                </thead>
                <tbody>
        `;

        walks.forEach((walk) => {
            const daysAbrev = walk.days_of_week.map(getDayAbbrev).join(" / ");
            const phone = walk.phone || "-";

            html += `
                <tr>
                    <td>${walk.dog_name}</td>
                    <td>${walk.owner_name}</td>
                    <td>${phone}</td>
                    <td>${daysAbrev}</td>
                    <td>${walk.walks_per_day}</td>
                    <td>${formatCurrency(walk.total)}</td>
                    <td>
                        <div class="action-btns">
                            <button class="btn btn-danger" onclick="removeWalk('${walk.dog_name}')">
                                🗑️ Remover
                            </button>
                        </div>
                    </td>
                </tr>
            `;
        });

        html += `
                </tbody>
            </table>
        `;

        document.getElementById("walksListContainer").innerHTML = html;
    } catch (error) {
        console.error("Erro ao carregar passeios:", error);
        showToast("Erro ao carregar passeios", "error");
    }
}

async function removeWalk(dogName) {
    if (!confirm(`Deseja remover o passeio de "${dogName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/walks/${encodeURIComponent(dogName)}`, {
            method: "DELETE",
        });

        const result = await response.json();

        if (result.success) {
            showToast(`✅ Passeio removido!`, "success");
            loadWalks();
            loadDashboard();
        } else {
            showToast(`Erro: ${result.error}`, "error");
        }
    } catch (error) {
        console.error("Erro ao remover:", error);
        showToast("Erro ao remover passeio", "error");
    }
}

// ══════════════════════════════════════════════════════════════════════
// SCHEDULE
// ══════════════════════════════════════════════════════════════════════

async function loadSchedule() {
    try {
        const { data: schedule } = await fetchAPI("/api/schedule");

        if (!schedule) {
            document.getElementById("scheduleContainer").innerHTML =
                "<p>Erro ao carregar agenda</p>";
            return;
        }

        let html = "";
        let hasAny = false;

        Object.entries(schedule).forEach(([day, walks]) => {
            if (walks.length > 0) {
                hasAny = true;
                const dayTotal = walks.reduce((sum, w) => sum + (w.walks_per_day || 1), 0);
                const dayValue = dayTotal * PRICE_PER_WALK;

                html += `
                    <div class="schedule-day">
                        <h3>📅  ${day}</h3>
                        <div class="day-stats">
                            <span>${dayTotal} passeio(s)</span>
                            <span>${formatCurrency(dayValue)}</span>
                        </div>
                        <ul class="dog-list">
                            ${walks
                                .map(
                                    (w) => `
                                <li>
                                    🐕 <strong>${w.dog_name}</strong>
                                    <br>
                                    <small>👤 ${w.owner_name} | 📱 ${
                                        w.phone || "sem telefone"
                                    }</small>
                                </li>
                            `
                                )
                                .join("")}
                        </ul>
                    </div>
                `;
            }
        });

        if (!hasAny) {
            html = "<p>Nenhum passeio agendado nesta semana</p>";
        }

        document.getElementById("scheduleContainer").innerHTML = html;
    } catch (error) {
        console.error("Erro ao carregar agenda:", error);
        showToast("Erro ao carregar agenda", "error");
    }
}

// ══════════════════════════════════════════════════════════════════════
// SEARCH
// ══════════════════════════════════════════════════════════════════════

async function searchOwner() {
    const ownerName = document.getElementById("searchOwner").value.trim();

    if (!ownerName) {
        showToast("Digite o nome do dono", "warning");
        return;
    }

    try {
        const response = await fetch(`/api/owner/${encodeURIComponent(ownerName)}`);
        const result = await response.json();

        if (result.success && result.data.length > 0) {
            displaySearchResults(result.data, ownerName);
        } else {
            document.getElementById("searchResults").innerHTML =
                `<p>Nenhum resultado encontrado para "${ownerName}"</p>`;
        }
    } catch (error) {
        console.error("Erro ao buscar:", error);
        showToast("Erro ao buscar", "error");
    }
}

function displaySearchResults(results, ownerName) {
    let html = `<h3>Resultados para "${ownerName}" (${results.length} cão(s)):</h3>`;
    let totalValue = 0;

    results.forEach((result) => {
        const daysAbrev = result.days_of_week.map(getDayAbbrev).join(" / ");
        const phone = result.phone || "não informado";
        totalValue += result.total;

        html += `
            <div class="result-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>🐕 ${result.dog_name}</h4>
                        <p><small>📅 ${daysAbrev} | 🔢 ${result.walks_per_day} passeio(s)/dia | 📱 ${phone}</small></p>
                    </div>
                    <div style="text-align: right;">
                        <p style="font-weight: bold; color: var(--primary); font-size: 1.2rem;">
                            ${formatCurrency(result.total)}
                        </p>
                    </div>
                </div>
            </div>
        `;
    });

    html += `
        <div style="background: var(--bg-light); padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 4px solid var(--success);">
            <h4>💰 Total para ${ownerName}:</h4>
            <p style="font-size: 1.3rem; font-weight: bold; color: var(--success);">${formatCurrency(totalValue)}</p>
        </div>
    `;

    document.getElementById("searchResults").innerHTML = html;
}

// ══════════════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ══════════════════════════════════════════════════════════════════════

async function fetchAPI(endpoint) {
    const response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    return await response.json();
}

function formatCurrency(value) {
    return new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
    }).format(value);
}

function getDayAbbrev(fullDay) {
    const abbrevMap = {
        "Segunda-feira": "Seg",
        "Terça-feira": "Ter",
        "Quarta-feira": "Qua",
        "Quinta-feira": "Qui",
        "Sexta-feira": "Sex",
        Sábado: "Sáb",
        Domingo: "Dom",
    };
    return abbrevMap[fullDay] || fullDay;
}

function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
}
