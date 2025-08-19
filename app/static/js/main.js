
const API_BASE_URL = '/api/v1';
let currentUser = null;


document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
});


function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        fetchCurrentUser();
        updateNavigation(true);
    } else {
        updateNavigation(false);
        const protectedPages = ['/dashboard', '/employees', '/leaves'];
        if (protectedPages.includes(window.location.pathname)) {
            window.location.href = '/login';
        }
    }
}

async function fetchCurrentUser() {
    try {
        const response = await apiCall('/employees/me');
        if (response.ok) {
            currentUser = await response.json();
            updateUserInfo();
        } else {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Error fetching user:', error);
    }
}

function updateNavigation(isAuthenticated) {
    const loginLink = document.getElementById('loginLink');
    const logoutLink = document.getElementById('logoutLink');
    
    if (isAuthenticated) {
        loginLink.style.display = 'none';
        logoutLink.style.display = 'block';
    } else {
        loginLink.style.display = 'block';
        logoutLink.style.display = 'none';
    }
}


function updateUserInfo() {
    const userInfoElement = document.getElementById('userInfo');
    if (userInfoElement && currentUser) {
        userInfoElement.textContent = `Welcome, ${currentUser.name} (${currentUser.is_admin ? 'Admin' : 'Employee'})`;
    }

    
    const adminElements = document.querySelectorAll('.admin-only');
    adminElements.forEach(el => {
        el.style.display = (currentUser && currentUser.is_admin) ? 'block' : 'none';
    });

    
    if (currentUser && !currentUser.is_admin) {
        const addEmployeeBtn = document.getElementById('addEmployeeBtn');
        if (addEmployeeBtn) addEmployeeBtn.style.display = 'none';

        const manageEmployeesBtn = document.getElementById('manageEmployeesBtn');
        if (manageEmployeesBtn) manageEmployeesBtn.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('token');
    currentUser = null;
    window.location.href = '/login';
}


async function apiCall(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        defaultHeaders['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        headers: defaultHeaders,
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        return response;
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}


function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();
    
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" id="${alertId}" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHTML);
    
    
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}


function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}


function getStatusBadge(status) {
    const statusClasses = {
        'pending': 'badge bg-warning text-dark',
        'approved': 'badge bg-success',
        'rejected': 'badge bg-danger'
    };
    
    return `<span class="${statusClasses[status] || 'badge bg-secondary'}">${status.charAt(0).toUpperCase() + status.slice(1)}</span>`;
}


function getLeaveTypeBadge(type) {
    const typeClasses = {
        'vacation': 'badge bg-info text-dark',
        'sick': 'badge bg-warning text-dark',
        'personal': 'badge bg-secondary',
        'emergency': 'badge bg-danger',
        'maternity': 'badge bg-success',
        'paternity': 'badge bg-success'
    };
    
    return `<span class="${typeClasses[type] || 'badge bg-primary'}">${type.charAt(0).toUpperCase() + type.slice(1)}</span>`;
}


function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}


function setLoadingState(element, isLoading, originalText = '') {
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = originalText;
    }
}


function createTableRow(data, columns, actions = []) {
    const row = document.createElement('tr');
    
    columns.forEach(column => {
        const cell = document.createElement('td');
        if (typeof column === 'function') {
            cell.innerHTML = column(data);
        } else {
            cell.textContent = data[column] || '';
        }
        row.appendChild(cell);
    });
    
 
    if (actions.length > 0) {
        const actionsCell = document.createElement('td');
        const actionsHTML = actions.map(action => {
            return `<button class="btn btn-sm ${action.class}" onclick="${action.onclick}">${action.text}</button>`;
        }).join(' ');
        actionsCell.innerHTML = actionsHTML;
        row.appendChild(actionsCell);
    }
    
    return row;
}


window.checkAuth = checkAuth;
window.logout = logout;
window.apiCall = apiCall;
window.showAlert = showAlert;
window.formatDate = formatDate;
window.formatDateTime = formatDateTime;
window.getStatusBadge = getStatusBadge;
window.getLeaveTypeBadge = getLeaveTypeBadge;
window.validateForm = validateForm;
window.setLoadingState = setLoadingState;
