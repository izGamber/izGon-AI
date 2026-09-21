/**
 * izGon AI - Frontend JavaScript
 * Real-time komunikacija sa Brain Engine-om
 */

// ===== SOCKET.IO SETUP =====
let socket;
try {
    socket = io({
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5
    });
    
    socket.on('connect', () => {
        console.log('✅ Socket.IO povezan');
        updateStats();
    });
    
    socket.on('disconnect', () => {
        console.log('❌ Socket.IO odключen');
    });
    
    socket.on('memory_added', () => {
        updateStats();
        refreshActivity();
    });
    
} catch (e) {
    console.warn('Socket.IO not available:', e);
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Aplikacija učitana');
    updateStats();
    refreshActivity();
    loadTheme();
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
async function updateStats() {
    try {
        const response = await fetch('/api/brain/stats');
        if (!response.ok) return;
        
        const data = await response.json();
        
        const totalMem = document.getElementById('totalMemories');
        if (totalMem) totalMem.textContent = data.total_memories || 0;
        
        const totalSnap = document.getElementById('totalSnapshots');
        if (totalSnap) totalSnap.textContent = data.snapshot_count || 0;
        
        const brainStatus = document.getElementById('brainStatus');
        if (brainStatus) {
            brainStatus.textContent = data.brain_health === 'optimal' ? '✅ Optimalno' : '⚠️ Potrebno učenje';
        }
        
        console.log('✅ Stats updated:', data);
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

async function refreshActivity() {
    try {
        const response = await fetch('/api/activities');
        if (!response.ok) return;
        
        const activities = await response.json();
        const list = document.getElementById('activityList');
        
        if (list) {
            if (activities.length === 0) {
                list.innerHTML = '<p class="loading">Nema aktivnosti</p>';
            } else {
                list.innerHTML = activities.map(a => `
                    <div class="activity-item">
                        <div class="activity-icon">
                            <i class="fas fa-${getActivityIcon(a.type)}"></i>
                        </div>
                        <div class="activity-content">
                            <p>${a.title}</p>
                            <span class="activity-time">${new Date(a.timestamp).toLocaleString('sr-RS')}</span>
                        </div>
                    </div>
                `).join('');
            }
        }
        
        console.log('✅ Activity refreshed');
    } catch (error) {
        console.error('Error refreshing activity:', error);
    }
}

function getActivityIcon(type) {
    const icons = {
        'note': 'sticky-note',
        'learning': 'graduation-cap',
        'insight': 'lightbulb',
        'error': 'exclamation-circle',
        'solution': 'check-circle'
    };
    return icons[type] || 'circle';
}

// ===== MODAL FUNCTIONS =====
function openAddMemoryModal() {
    const modal = document.getElementById('addMemoryModal');
    if (modal) modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

function openBrainAnalysis() {
    alert('Brain analiza - coming soon');
}

function viewMemories() {
    alert('Sve memorije - coming soon');
}

// ===== FORM HANDLING =====
document.addEventListener('DOMContentLoaded', () => {
    const memoryForm = document.getElementById('memoryForm');
    if (memoryForm) {
        memoryForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const content = formData.get('content');
            const memoryType = formData.get('memoryType');
            const importance = formData.get('importance');
            
            try {
                const response = await fetch(`/api/brain/remember?content=${encodeURIComponent(content)}&memory_type=${memoryType}&importance=${importance}`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    alert('✅ Memorija čuvana!');
                    closeModal('addMemoryModal');
                    e.target.reset();
                    updateStats();
                    refreshActivity();
                    if (socket) socket.emit('memory_added', {});
                } else {
                    alert('❌ Greška pri čuvanju memorije');
                }
            } catch (error) {
                console.error('Error saving memory:', error);
                alert('❌ Greška: ' + error.message);
            }
        });
    }
    
    // Importance slider
    const importanceSlider = document.querySelector('input[name="importance"]');
    const importanceValue = document.getElementById('importanceValue');
    if (importanceSlider && importanceValue) {
        importanceSlider.addEventListener('input', (e) => {
            importanceValue.textContent = e.target.value;
        });
    }
});

// ===== ACTIONS =====
async function takeSnapshot() {
    try {
        const response = await fetch('/api/brain/snapshot', { method: 'POST' });
        if (response.ok) {
            const data = await response.json();
            alert(`✅ Snapshot kreiran! (${data.memory_count} memorija)`);
            updateStats();
        }
    } catch (error) {
        console.error('Error taking snapshot:', error);
        alert('❌ Greška pri kreiranju snapshota');
    }
}

// ===== THEME TOGGLE =====
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});

// Auto-refresh stats every 30 seconds
setInterval(updateStats, 30000);

console.log('✅ App.js loaded successfully');
