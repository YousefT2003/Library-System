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

document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.remove('active');
    }
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    }
});

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(flash => {
            flash.style.transition = 'opacity 0.5s ease';
            flash.style.opacity = '0';
            setTimeout(() => flash.remove(), 500);
        });
    }, 5000);
});

document.addEventListener('click', function(e) {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.querySelector('.menu-toggle');
    if (sidebar && sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) && !toggle.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    
    // متغيرات الشارتات
    let pieChart, barChart;

    // دالة لتنظيف الشارتات القديمة قبل الرسم
    function destroyChart(canvasId) {
        const existingChart = Chart.getChart(canvasId);
        if (existingChart) {
            existingChart.destroy();
        }
    }

    /* PIE CHART - Most Borrowed Categories */
    const pieCanvas = document.getElementById("pieChart");
    if (pieCanvas) {
        destroyChart("pieChart"); // تدمير أي شارت قديم
        pieChart = new Chart(pieCanvas, {
            type: "pie",
            data: {
                labels: [], 
                datasets: [{
                    label: "Borrowed Categories",
                    data: [], 
                    backgroundColor: ["#4a90e2", "#50e3c2", "#f5a623", "#e74c3c", "#9b59b6"],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { position: "bottom" } }
            }
        });
    }

    /* BAR CHART - Borrowings Per Month */
    const barCanvas = document.getElementById("barChart");
    if (barCanvas) {
        destroyChart("barChart"); // تدمير أي شارت قديم
        barChart = new Chart(barCanvas, {
            type: "bar",
            data: {
                labels: [], 
                datasets: [{
                    label: "Borrowings",
                    data: [], 
                    backgroundColor: "#4a90e2",
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { precision: 0 }
                    }
                }
            }
        });
    }

    // جلب البيانات وتحديث الشارتات
    fetch('/dashboard-data')
        .then(response => response.json())
        .then(data => {
            if (pieChart) {
                pieChart.data.labels = data.pie.labels;
                pieChart.data.datasets[0].data = data.pie.values;
                pieChart.update();
            }
            if (barChart) {
                barChart.data.labels = data.bar.labels;
                barChart.data.datasets[0].data = data.bar.values;
                barChart.update();
            }
        })
        .catch(err => console.error("Error fetching dashboard data:", err));
});