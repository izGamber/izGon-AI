/**
 * izGon AI - Frontend JavaScript
 * Real-time komunikacija sa Brain Engine-om
 */

// ===== SOCKET.IO SETUP =====
const socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5
});

// ===== SOCKET EVENTS =====
socket.on('connect', () => {
    console.log('✅ Konekcija uspostavljena');
    updateAllStats();
});

socket.on('disconnect', () => {
    console.log('❌ Konekcija prekinuta');
    showNotification('Konekcija prekinuta', 'warning');
});

socket.on('memory_added', (data) => {
    console.log('📝 Nova memorija:', data);
    updateAllStats();
    showNotification('Memorija čuvana!', 'success');
    playSound('success');
});

socket.on('snapshot_created', (data) => {
    console.log('📸 Snapshot kreiran:', data);
    updateAllStats();
    showNotification(`Snapshot kreiran (${data.memory_count} memorija)`, 'success');
});

socket.on('brain_update', (data) => {
    console.log('🧠 Brain update:', data);
    updateBrainStatus(data);
});

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Aplikacija učitana');
    
    // Učitaj theme preference
    loadTheme();
    
    // Inicijalizuj sve
    updateAllStats();
    refreshActivity();
    initializeEventListeners();
    
    // Real-time ažuriranja svakih 30 sekundi
    setInterval(updateAllStats, 30000);
});

// ===== THEME SYSTEM =====
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
}

function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

// ===== API CALLS =====
async function apiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showNotification(`Greška: ${error.message}`, 'error');
        return null;
    }
}

// ===== STATS FUNCTIONS =====
async function updateAllStats() {
    updateMemoryStats();
    updateBrainStats();
}

async function updateMemoryStats() {
    const data = await apiCall('/api/brain/stats');
    if (!data) return;
    
    document.getElementById('totalMemories').textContent = data.total_memories || 0;
    document.getElementById('totalSnapshots').textContent = data.snapshot_count || 0;
    
    // Ažuriraj brain status
    const statusEl = document.getElementById('brainStatus');
    if (statusEl) {
        statusEl.textContent = data.brain_health === 'optimal' ? '✅ Optimalno' : '⚠️ Potrebno učenje';
        statusEl.style.color = data.brain_health === 'optimal' ? '#10b981' : '#f59e0b';
    }
}

async function updateBrainStats() {
    const data = await apiCall('/api/brain/stats');
    if (!data) return;
    
    // Ažuriraj chart memorija po tipu
    if (data.memory_types && typeof Chart !== 'undefined') {
        updateMemoryChart(data.memory_types);
    }
}

function updateBrainStatus(data) {
    const statusEl = document.getElementById('brainStatus');
    if (statusEl && data.status) {
        statusEl.textContent = data.status.toUpperCase();
        statusEl.style.color = '#10b981';
    }
}

// ===== ACTIVITY FUNCTIONS =====
async function refreshActivity() {
    const data = await apiCall('/api/activities');
    if (!data) return;
    
    const list = document.getElementById('activityList');
    if (!list) return;
    
    if (data.length === 0) {
        list.innerHTML = '<p class="loading">Nema aktivnosti</p>';
        return;
    }
    
    list.innerHTML = data.map(activity => `
        <div class="activity-item">
            <div class="activity-icon ${activity.type}">
                <i class="fas fa-${getActivityIcon(activity.type)}"></i>
            </div>
            <div class="activity-content">
                <p>${activity.title || activity.content}</p>
                <span class="activity-time">${formatTime(activity.timestamp)}</span>
            </div>
        </div>
    `).join('');
}

function getActivityIcon(type) {
    const icons = {
        'memory': 'brain',
        'note': 'sticky-note',
        'learning': 'lightbulb',
        'insight': 'eye',
        'snapshot': 'camera',
        'project': 'folder',
        'error': 'exclamation',
        'solution': 'check'
    };
    return icons[type] || 'circle';
}

// ===== MEMORY FUNCTIONS =====
async function addMemory(memoryType, content, importance) {
    const data = await apiCall('/api/brain/remember', 'POST', {
        content,
        memory_type: memoryType,
        importance: parseInt(importance)
    });
    
    if (data) {
        socket.emit('memory_added', data);
        return data;
    }
    return null;
}

async function getMemories(limit = 20) {
    return await apiCall(`/api/brain/memories?limit=${limit}`);
}

async function searchMemories(keyword) {
    return await apiCall(`/api/brain/search?keyword=${encodeURIComponent(keyword)}`);
}

async function deleteMemory(memoryId) {
    if (!confirm('Sigurno želiš da obrišeš ovu memoriju?')) return;
    
    const data = await apiCall(`/api/brain/forget/${memoryId}`, 'DELETE');
    if (data) {
        showNotification('Memorija obrisana', 'success');
        updateAllStats();
    }
}

async function updateMemoryImportance(memoryId, importance) {
    return await apiCall(`/api/brain/importance/${memoryId}`, 'PATCH', {
        importance
    });
}

// ===== SNAPSHOT FUNCTIONS =====
async function takeSnapshot() {
    const data = await apiCall('/api/brain/snapshot', 'POST');
    if (data) {
        socket.emit('snapshot_created', data);
        return data;
    }
    return null;
}

async function restoreSnapshot(snapshotId) {
    if (!confirm('Sigurno želiš da vrati stanje iz snapshota?')) return;
    
    const data = await apiCall(`/api/brain/snapshot/${snapshotId}`, 'POST');
    if (data) {
        showNotification('Snapshot vraćen', 'success');
        updateAllStats();
    }
}

// ===== MODAL FUNCTIONS =====
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

function openAddMemoryModal() {
    openModal('addMemoryModal');
}

function closeAddMemoryModal() {
    closeModal('addMemoryModal');
}

// Zatvori modal na klik van sadržaja
window.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// ===== FORM HANDLERS =====
function initializeEventListeners() {
    // Add Memory Form
    const memoryForm = document.getElementById('memoryForm');
    if (memoryForm) {
        memoryForm.addEventListener('submit', handleAddMemory);
    }
    
    // Importance slider
    const importanceInput = document.querySelector('input[name="importance"]');
    if (importanceInput) {
        importanceInput.addEventListener('input', (e) => {
            document.getElementById('importanceValue').textContent = e.target.value;
        });
    }
    
    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
}

async function handleAddMemory(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const memoryType = formData.get('memoryType');
    const content = formData.get('content');
    const importance = formData.get('importance');
    
    const result = await addMemory(memoryType, content, importance);
    
    if (result) {
        closeAddMemoryModal();
        e.target.reset();
        document.getElementById('importanceValue').textContent = '3';
    }
}

// ===== CHART FUNCTIONS =====
let memoryChart = null;

function updateMemoryChart(memoryTypes) {
    const ctx = document.getElementById('memoryChart');
    if (!ctx) return;
    
    const labels = Object.keys(memoryTypes);
    const data = Object.values(memoryTypes);
    
    if (memoryChart) {
        memoryChart.destroy();
    }
    
    memoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.map(l => capitalizeFirst(l)),
            datasets: [{
                data: data,
                backgroundColor: [
                    '#6366f1',
                    '#8b5cf6',
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b'
                ],
                borderColor: [
                    '#4f46e5',
                    '#7c3aed',
                    '#2563eb',
                    '#059669',
                    '#d97706'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: document.body.classList.contains('dark-mode') ? '#e2e8f0' : '#1f2937',
                        font: { size: 14 }
                    }
                }
            }
        }
    });
}

// ===== UTILITY FUNCTIONS =====
function showNotification(message, type = 'info') {
    // Kreiraj notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideInDown 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Ukloni nakon 3 sekunde
    setTimeout(() => {
        notification.style.animation = 'slideOutUp 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) return 'Upravo sada';
    if (minutes < 60) return `Pre ${minutes}m`;
    if (hours < 24) return `Pre ${hours}h`;
    if (days < 7) return `Pre ${days}d`;
    
    return date.toLocaleDateString('sr-RS');
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function playSound(type = 'success') {
    // Koristi Web Audio API za zvuk bez fajlova
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    if (type === 'success') {
        oscillator.frequency.value = 800;
        oscillator.frequency.exponentialRampToValueAtTime(1000, audioContext.currentTime + 0.1);
    } else if (type === 'error') {
        oscillator.frequency.value = 200;
    }
    
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.2);
}

// ===== ACTION FUNCTIONS =====
function viewMemories() {
    alert('Brzo će biti dostupna memorije stranica!');
}

function openBrainAnalysis() {
    alert('Brain analiza je u razvoju!');
}

// ===== CSS ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutUp {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(-100px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('✅ JavaScript učitan');
