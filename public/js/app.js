/* ============================================
   Library Management System — JavaScript
   ============================================ */

/**
 * Toggle sidebar visibility on mobile.
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

/**
 * Open a modal by ID.
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        // Focus first input in the modal
        setTimeout(() => {
            const input = modal.querySelector('input:not([type="hidden"])');
            if (input) input.focus();
        }, 100);
    }
}

/**
 * Close a modal by ID.
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

// Close modal when clicking overlay background
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    }
});

// Auto-dismiss flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.transition = 'opacity 0.5s ease';
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 500);
        });
    }, 5000);
});

// Close sidebar on mobile when clicking outside
document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');
    if (sidebar && sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

document.addEventListener("DOMContentLoaded", function () {

    /* PIE CHART - Most Borrowed Categories */
    const pieCanvas = document.getElementById("pieChart");

    if (pieCanvas) {
        new Chart(pieCanvas, {
            type: "pie",
            data: {
                labels: [
                    "Science",
                    "Technology",
                    "Literature",
                    "History",
                    "Other"
                ],
                datasets: [{
                    label: "Borrowed Categories",
                    data: [12, 19, 8, 10, 5],
                    backgroundColor: [
                        "#4a90e2",
                        "#50e3c2",
                        "#f5a623",
                        "#e74c3c",
                        "#9b59b6"
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }


    /* BAR CHART - Borrowings Per Month */
    const barCanvas = document.getElementById("barChart");

    if (barCanvas) {
        new Chart(barCanvas, {
            type: "bar",
            data: {
                labels: [
                    "Jan","Feb","Mar","Apr","May","Jun",
                    "Jul","Aug","Sep","Oct","Nov","Dec"
                ],
                datasets: [{
                    label: "Borrowings",
                    data: [5, 8, 12, 6, 9, 15, 7, 10, 14, 11, 8, 6],
                    backgroundColor: "#4a90e2",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

});
