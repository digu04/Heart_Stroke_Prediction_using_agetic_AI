// ============================================
// app.js — SPA Router, API Calls, Animations
// Heart Disease Prediction — Agentic AI
// ============================================

// ---------------------------
// STATE
// ---------------------------
const state = {
    user: null,
    context: null,
    chatHistory: [],
    currentPage: 'register',
};

// ---------------------------
// NAVIGATION
// ---------------------------
function navigateTo(page) {
    // Validation gates
    if (page !== 'register' && !state.user) {
        showAlert('regMessage', 'Please register or login first.', 'warning');
        return;
    }
    if ((page === 'results' || page === 'chat') && !state.context) {
        showAlert('inputMessage', 'Please run a prediction first.', 'warning');
        page = 'input';
    }

    state.currentPage = page;

    // Hide all views
    document.querySelectorAll('.view').forEach(v => {
        v.classList.remove('active');
    });
    // Show target
    const target = document.getElementById('view-' + page);
    if (target) target.classList.add('active');

    // Update nav
    document.querySelectorAll('.nav-item').forEach(n => {
        n.classList.toggle('active', n.dataset.page === page);
    });

    // Close mobile sidebar
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('mobileOverlay').classList.remove('visible');

    // Page-specific actions
    if (page === 'history') loadHistory();
    if (page === 'register') loadExistingUsers();
}

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('mobileOverlay').classList.toggle('visible');
}

// ---------------------------
// LOADING OVERLAY
// ---------------------------
function showLoading(text) {
    document.getElementById('loadingText').textContent = text || 'Processing...';
    document.getElementById('loadingOverlay').classList.add('visible');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('visible');
}

// ---------------------------
// ALERT HELPER
// ---------------------------
function showAlert(containerId, message, type) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const icon = { success: '✅', warning: '⚠️', danger: '❌', info: 'ℹ️' }[type] || 'ℹ️';
    container.innerHTML = `<div class="alert alert-${type}">${icon} ${message}</div>`;
    setTimeout(() => { container.innerHTML = ''; }, 5000);
}

// ---------------------------
// REGISTER / LOGIN
// ---------------------------
function toggleRegMode(mode) {
    const isNew = mode === 'new';
    document.getElementById('newUserForm').style.display = isNew ? 'block' : 'none';
    document.getElementById('existUserForm').style.display = isNew ? 'none' : 'block';
    document.getElementById('togNew').classList.toggle('active', isNew);
    document.getElementById('togExist').classList.toggle('active', !isNew);
    if (!isNew) loadExistingUsers();
}

async function loadExistingUsers() {
    try {
        const res = await fetch('/api/users');
        const data = await res.json();
        const sel = document.getElementById('existEmail');
        if (data.users && data.users.length > 0) {
            sel.innerHTML = data.users.map(u =>
                `<option value="${u.email}">${u.name} (${u.email})</option>`
            ).join('');
        } else {
            sel.innerHTML = '<option value="">No users found</option>';
        }
    } catch (e) {
        console.error('Failed to load users:', e);
    }
}

async function registerUser() {
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const mobile = document.getElementById('regMobile').value.trim();

    if (!name || !email) {
        showAlert('regMessage', 'Name and email are required.', 'warning');
        return;
    }

    try {
        const res = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, mobile })
        });
        const data = await res.json();

        if (data.success) {
            state.user = data.user;
            updateSidebarUser();
            showAlert('regMessage', `Welcome, ${data.user.name}!`, 'success');
            setTimeout(() => navigateTo('input'), 800);
        } else {
            showAlert('regMessage', data.error || 'Registration failed.', 'danger');
        }
    } catch (e) {
        showAlert('regMessage', 'Server error. Is the backend running?', 'danger');
    }
}

async function loginUser() {
    const email = document.getElementById('existEmail').value;
    if (!email) {
        showAlert('regMessage', 'Please select a user.', 'warning');
        return;
    }

    try {
        const res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await res.json();

        if (data.success) {
            state.user = data.user;
            updateSidebarUser();
            showAlert('regMessage', `Welcome back, ${data.user.name}!`, 'success');
            setTimeout(() => navigateTo('input'), 800);
        } else {
            showAlert('regMessage', data.error || 'User not found.', 'danger');
        }
    } catch (e) {
        showAlert('regMessage', 'Server error.', 'danger');
    }
}

function updateSidebarUser() {
    if (!state.user) return;
    document.getElementById('sidebarUserInfo').style.display = 'flex';
    document.getElementById('sidebarUserName').textContent = state.user.name;
    document.getElementById('sidebarUserEmail').textContent = state.user.email;
    document.getElementById('userAvatar').textContent = state.user.name.charAt(0).toUpperCase();
}

// ---------------------------
// TABS (Input page)
// ---------------------------
function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

    document.getElementById('tab' + tab.charAt(0).toUpperCase() + tab.slice(1)).classList.add('active');
    document.getElementById('content-' + tab).classList.add('active');
}

// ---------------------------
// FORM PREDICTION
// ---------------------------
async function submitFormPrediction() {
    const data = {
        Age: document.getElementById('fAge').value,
        Sex: document.getElementById('fSex').value,
        ChestPainType: document.getElementById('fChestPain').value,
        RestingBP: document.getElementById('fRestingBP').value,
        Cholesterol: document.getElementById('fCholesterol').value,
        FastingBS: document.getElementById('fFastingBS').value,
        RestingECG: document.getElementById('fRestingECG').value,
        MaxHR: document.getElementById('fMaxHR').value,
        ExerciseAngina: document.getElementById('fExerciseAngina').value,
        Oldpeak: document.getElementById('fOldpeak').value,
        ST_Slope: document.getElementById('fSTSlope').value
    };

    // Basic validation
    if (!data.Age || !data.RestingBP || !data.Cholesterol || !data.MaxHR) {
        showAlert('inputMessage', 'Please fill in all required fields.', 'warning');
        return;
    }

    showLoading('Running AI prediction pipeline...');

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: data, user: state.user })
        });
        const result = await res.json();
        hideLoading();

        if (result.success) {
            state.context = result.context;
            renderResults();
            navigateTo('results');
        } else {
            showAlert('inputMessage', result.error || 'Prediction failed.', 'danger');
        }
    } catch (e) {
        hideLoading();
        showAlert('inputMessage', 'Server error during prediction.', 'danger');
    }
}

// ---------------------------
// FREE TEXT PREDICTION
// ---------------------------
async function submitTextPrediction() {
    const text = document.getElementById('freeText').value.trim();
    if (!text) {
        showAlert('inputMessage', 'Please describe your symptoms.', 'warning');
        return;
    }

    showLoading('AI is analyzing your text...');

    try {
        const res = await fetch('/api/predict-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, user: state.user })
        });
        const result = await res.json();
        hideLoading();

        if (result.success) {
            state.context = result.context;
            renderResults();
            navigateTo('results');
        } else {
            showAlert('inputMessage', result.error || 'Text analysis failed.', 'danger');
        }
    } catch (e) {
        hideLoading();
        showAlert('inputMessage', 'Server error.', 'danger');
    }
}

// ---------------------------
// PDF UPLOAD
// ---------------------------
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    document.getElementById('uploadFileName').textContent = '📎 ' + file.name;

    // Upload to backend for extraction
    const formData = new FormData();
    formData.append('file', file);

    showLoading('Extracting text from PDF...');

    fetch('/api/extract-pdf', { method: 'POST', body: formData })
        .then(r => r.json())
        .then(data => {
            hideLoading();
            if (data.success) {
                document.getElementById('extractedText').value = JSON.stringify(data.extracted, null, 2);
                document.getElementById('extractedPreview').style.display = 'block';
                // Store extracted data for prediction
                state._uploadedData = data.extracted;
            } else {
                showAlert('inputMessage', data.error || 'PDF extraction failed.', 'danger');
            }
        })
        .catch(() => {
            hideLoading();
            showAlert('inputMessage', 'Server error during PDF extraction.', 'danger');
        });
}

async function submitUploadPrediction() {
    if (!state._uploadedData) {
        showAlert('inputMessage', 'Please upload a PDF first.', 'warning');
        return;
    }

    showLoading('Running AI prediction pipeline...');

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: state._uploadedData, user: state.user })
        });
        const result = await res.json();
        hideLoading();

        if (result.success) {
            state.context = result.context;
            renderResults();
            navigateTo('results');
        } else {
            showAlert('inputMessage', result.error || 'Prediction failed.', 'danger');
        }
    } catch (e) {
        hideLoading();
        showAlert('inputMessage', 'Server error.', 'danger');
    }
}

// ---------------------------
// RENDER RESULTS
// ---------------------------
function renderResults() {
    const ctx = state.context;
    if (!ctx) return;

    const risk = ctx.risk;
    const prediction = ctx.prediction;

    // Gauge animation
    const circumference = 2 * Math.PI * 85; // ~534
    const offset = circumference - (risk / 100) * circumference;
    const gaugeFill = document.getElementById('gaugeFill');

    let gaugeColor = 'var(--accent-green)';
    if (risk >= 60) gaugeColor = 'var(--accent-red)';
    else if (risk >= 30) gaugeColor = 'var(--accent-amber)';

    gaugeFill.style.stroke = gaugeColor;
    // Trigger animation
    setTimeout(() => {
        gaugeFill.style.strokeDashoffset = offset;
    }, 100);

    // Counter animation for gauge value
    animateCounter('gaugeValue', 0, risk, 1500);

    // Stat cards
    document.getElementById('resPrediction').textContent =
        prediction === 1 ? 'High Risk ⚠️' : 'Low Risk ✅';
    document.getElementById('resPrediction').style.color =
        prediction === 1 ? 'var(--accent-red)' : 'var(--accent-green)';

    let riskLabel = 'Low';
    if (risk >= 60) riskLabel = 'High';
    else if (risk >= 30) riskLabel = 'Moderate';
    document.getElementById('resRisk').textContent = riskLabel;
    document.getElementById('resRisk').style.color = gaugeColor;

    // Reasoning & Lifestyle
    document.getElementById('resReasoning').textContent = ctx.reasoning || 'No interpretation available.';
    document.getElementById('resLifestyle').textContent = ctx.lifestyle || 'No recommendations available.';
}

function animateCounter(elementId, start, end, duration) {
    const el = document.getElementById(elementId);
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = start + (end - start) * eased;
        el.textContent = current.toFixed(1) + '%';
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// ---------------------------
// ACCORDION
// ---------------------------
function toggleAccordion(id) {
    const item = document.getElementById(id);
    const body = item.querySelector('.accordion-body');
    const inner = item.querySelector('.accordion-body-inner');

    if (item.classList.contains('open')) {
        body.style.maxHeight = '0';
        item.classList.remove('open');
    } else {
        body.style.maxHeight = inner.scrollHeight + 20 + 'px';
        item.classList.add('open');
    }
}

// ---------------------------
// CHAT
// ---------------------------
async function sendChat() {
    const input = document.getElementById('chatInput');
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    // Add user message
    appendChatMessage(msg, 'user');

    // Show typing indicator
    const typingEl = document.createElement('div');
    typingEl.className = 'typing-indicator';
    typingEl.id = 'typingIndicator';
    typingEl.innerHTML = '<span></span><span></span><span></span>';
    document.getElementById('chatMessages').appendChild(typingEl);
    scrollChat();

    try {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, context: state.context })
        });
        const data = await res.json();

        // Remove typing indicator
        const ti = document.getElementById('typingIndicator');
        if (ti) ti.remove();

        if (data.reply) {
            appendChatMessage(data.reply, 'ai');
        } else {
            appendChatMessage('Sorry, I could not process your question.', 'ai');
        }
    } catch (e) {
        const ti = document.getElementById('typingIndicator');
        if (ti) ti.remove();
        appendChatMessage('Server error. Please try again.', 'ai');
    }
}

function appendChatMessage(text, sender) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'chat-msg ' + sender;
    div.textContent = text;
    container.appendChild(div);
    scrollChat();
}

function scrollChat() {
    const container = document.getElementById('chatMessages');
    container.scrollTop = container.scrollHeight;
}

// ---------------------------
// HISTORY
// ---------------------------
async function loadHistory() {
    const container = document.getElementById('historyContainer');
    container.innerHTML = '<div class="alert alert-info">Loading history...</div>';

    try {
        const res = await fetch('/api/history');
        const data = await res.json();

        if (!data.history || data.history.length === 0) {
            container.innerHTML = '<div class="alert alert-info">No prediction history found.</div>';
            return;
        }

        let html = '';
        data.history.reverse().forEach((entry, i) => {
            const isHigh = entry.prediction === 1;
            html += `
                <div class="history-entry ${isHigh ? 'high-risk' : ''}">
                    <div class="history-card">
                        <div class="history-ts">🕒 ${entry.timestamp}</div>
                        <div class="history-risk" style="color: ${isHigh ? 'var(--accent-red)' : 'var(--accent-green)'}">
                            ${entry.risk}% Risk
                        </div>
                        <div class="history-pred">
                            <span class="badge ${isHigh ? 'badge-high' : 'badge-low'}">
                                ${isHigh ? 'High Risk ⚠️' : 'Low Risk ✅'}
                            </span>
                        </div>

                        <div class="accordion-item" id="histAcc${i}">
                            <div class="accordion-header" onclick="toggleAccordion('histAcc${i}')">
                                <span>📋 Details</span>
                                <span class="acc-icon">▼</span>
                            </div>
                            <div class="accordion-body">
                                <div class="accordion-body-inner">
<strong>Features:</strong>
${Object.entries(entry.features || {}).map(([k, v]) => `${k}: ${v}`).join('\n')}

<strong>Medical Interpretation:</strong>
${entry.reasoning || 'N/A'}

<strong>Lifestyle Advice:</strong>
${entry.lifestyle || 'N/A'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = '<div class="alert alert-danger">Failed to load history.</div>';
    }
}

async function clearHistory() {
    if (!confirm('Are you sure you want to clear all history?')) return;

    try {
        await fetch('/api/history/clear', { method: 'POST' });
        loadHistory();
    } catch (e) {
        console.error('Failed to clear history:', e);
    }
}

// ---------------------------
// PDF DOWNLOAD
// ---------------------------
function downloadReport() {
    window.open('/api/report/download', '_blank');
}

// ---------------------------
// INIT
// ---------------------------
document.addEventListener('DOMContentLoaded', () => {
    loadExistingUsers();
});
