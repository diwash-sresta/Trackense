document.addEventListener('DOMContentLoaded', function () {
    // Add fade-in animation to elements
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(element => {
        element.classList.add('show');
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add hover effect to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseover', function () {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseout', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add smooth hover effects to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mouseover', function () {
            this.style.transform = 'translateY(-2px)';
        });

        button.addEventListener('mouseout', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add loading animations
    function addLoadingState(element) {
        element.classList.add('loading');
        element.disabled = true;
        const originalText = element.innerText;
        element.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Loading...
        `;
        return originalText;
    }

    function removeLoadingState(element, originalText) {
        element.classList.remove('loading');
        element.disabled = false;
        element.innerText = originalText;
    }

    // Apply loading state to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function (e) {
            const submitBtn = this.querySelector('[type="submit"]');
            if (submitBtn) {
                const originalText = addLoadingState(submitBtn);
                setTimeout(() => removeLoadingState(submitBtn, originalText), 1000);
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enhanced sidebar toggle functionality
    const toggleBtn = document.querySelector('.toggle-btn');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');

    function toggleSidebar(e) {
        e && e.preventDefault();

        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('main-content');
        const toggleIcon = document.getElementById('toggle-icon');

        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');

        // Store sidebar state
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));

        // Update ARIA attributes
        const isCollapsed = sidebar.classList.contains('collapsed');
        sidebar.setAttribute('aria-expanded', !isCollapsed);
        toggleBtn.setAttribute('aria-label', isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar');
    }

    // Restore sidebar state
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        toggleSidebar();
    }

    // Add click event listener
    toggleBtn.addEventListener('click', toggleSidebar);

    // Add keyboard navigation
    toggleBtn.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            toggleSidebar();
        }
    });
});
