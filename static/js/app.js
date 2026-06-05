/**
 * Superkey Finder — Client-side interactions
 */

// ─── Theme Toggle ───────────────────────────────────────
function initTheme() {
    const saved = localStorage.getItem('theme');
    if (saved) {
        document.documentElement.setAttribute('data-theme', saved);
    }
    // Default is dark (no data-theme attribute needed, :root handles it)
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'light' ? 'dark' : 'light';

    if (next === 'dark') {
        document.documentElement.removeAttribute('data-theme');
    } else {
        document.documentElement.setAttribute('data-theme', next);
    }

    localStorage.setItem('theme', next);
}

// Apply saved theme immediately (before paint)
initTheme();

// ─── Clear Form ─────────────────────────────────────────
function clearForm() {
    document.getElementById('attributes').value = '';
    document.getElementById('dependencies').value = '';
    document.getElementById('attributes').focus();

    // Hide results with a fade-out if visible
    const results = document.getElementById('results');
    if (results) {
        results.style.opacity = '0';
        results.style.transform = 'translateY(12px)';
        setTimeout(() => {
            results.style.display = 'none';
        }, 300);
    }
}

// ─── Smooth Scroll to Results ───────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const results = document.getElementById('results');
    if (results) {
        // Small delay so the animations play out first
        setTimeout(() => {
            results.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 350);
    }
});
