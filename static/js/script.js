document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initSidebar();
});

function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        html.classList.add('dark');
    } else {
        html.classList.remove('dark');
    }
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                html.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
        });
    }
    
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                html.classList.add('dark');
            } else {
                html.classList.remove('dark');
            }
        }
    });
}

function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const openBtn = document.getElementById('openSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    
    function openSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.remove('-translate-x-full');
            overlay.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    }
    
    function closeSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.add('-translate-x-full');
            overlay.classList.add('hidden');
            document.body.style.overflow = '';
        }
    }
    
    if (openBtn) {
        openBtn.addEventListener('click', openSidebar);
    }
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeSidebar);
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidebar();
        }
    });
    
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            closeSidebar();
        }
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    const bgColor = type === 'success' ? 'bg-green-500' :
                    type === 'error' ? 'bg-red-500' :
                    type === 'warning' ? 'bg-yellow-500' :
                    'bg-indigo-500';
    
    notification.className = `fixed top-4 right-4 z-50 px-4 py-3 rounded-lg shadow-lg animate-fade-in ${bgColor} text-white`;
    
    const container = document.createElement('div');
    container.className = 'flex items-center';
    
    const span = document.createElement('span');
    span.textContent = message;
    container.appendChild(span);
    
    const button = document.createElement('button');
    button.className = 'ml-4 text-white hover:text-gray-200';
    button.innerHTML = '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>';
    button.addEventListener('click', function() {
        notification.remove();
    });
    container.appendChild(button);
    
    notification.appendChild(container);
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function confirmAction(message) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50';
        
        const dialog = document.createElement('div');
        dialog.className = 'bg-white dark:bg-slate-800 rounded-lg shadow-xl max-w-md w-full p-6 animate-fade-in';
        
        const title = document.createElement('h3');
        title.className = 'text-lg font-semibold text-gray-900 dark:text-white mb-4';
        title.textContent = 'Confirm Action';
        dialog.appendChild(title);
        
        const msgPara = document.createElement('p');
        msgPara.className = 'text-gray-600 dark:text-gray-300 mb-6';
        msgPara.textContent = message;
        dialog.appendChild(msgPara);
        
        const btnContainer = document.createElement('div');
        btnContainer.className = 'flex justify-end space-x-3';
        
        const cancelBtn = document.createElement('button');
        cancelBtn.className = 'btn btn-secondary';
        cancelBtn.textContent = 'Cancel';
        cancelBtn.addEventListener('click', () => {
            modal.remove();
            resolve(false);
        });
        btnContainer.appendChild(cancelBtn);
        
        const confirmBtn = document.createElement('button');
        confirmBtn.className = 'btn btn-danger';
        confirmBtn.textContent = 'Confirm';
        confirmBtn.addEventListener('click', () => {
            modal.remove();
            resolve(true);
        });
        btnContainer.appendChild(confirmBtn);
        
        dialog.appendChild(btnContainer);
        modal.appendChild(dialog);
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
                resolve(false);
            }
        });
        
        document.body.appendChild(modal);
    });
}