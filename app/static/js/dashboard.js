

let dashboardData = {
    totalEmployees: 0,
    pendingRequests: 0,
    myBalance: 0,
    thisMonthLeaves: 0
};

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname === '/dashboard') {
        loadDashboard();
    }
});

async function loadDashboard() {
    try {
        await Promise.all([
            loadDashboardStats(),
            loadRecentLeaves()
        ]);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showAlert('Error loading dashboard data', 'danger');
    }
}

async function loadDashboardStats() {
    try {
       
        const employeesResponse = await apiCall('/employees');
        if (employeesResponse.ok) {
            const employees = await employeesResponse.json();
            dashboardData.totalEmployees = employees.length;
            document.getElementById('totalEmployees').textContent = employees.length;
        }

        
        if (currentUser) {
            const balanceResponse = await apiCall(`/employees/${currentUser.id}/balance`);
            if (balanceResponse.ok) {
                const balance = await balanceResponse.json();
                dashboardData.myBalance = balance.leave_balance;
                document.getElementById('myBalance').textContent = balance.leave_balance + ' days';
            }
        }

       
        const leavesResponse = await apiCall('/leaves');
        if (leavesResponse.ok) {
            const leaves = await leavesResponse.json();
            
            
            const pendingCount = leaves.filter(leave => leave.status === 'pending').length;
            dashboardData.pendingRequests = pendingCount;
            document.getElementById('pendingRequests').textContent = pendingCount;
            
            
            const currentMonth = new Date().getMonth();
            const currentYear = new Date().getFullYear();
            const thisMonthCount = leaves.filter(leave => {
                const leaveDate = new Date(leave.start_date);
                return leaveDate.getMonth() === currentMonth && 
                       leaveDate.getFullYear() === currentYear;
            }).length;
            dashboardData.thisMonthLeaves = thisMonthCount;
            document.getElementById('thisMonthLeaves').textContent = thisMonthCount;
        }
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}

async function loadRecentLeaves() {
    try {
        const response = await apiCall('/leaves?limit=5');
        if (response.ok) {
            const leaves = await response.json();
            displayRecentLeaves(leaves);
        }
    } catch (error) {
        console.error('Error loading recent leaves:', error);
        document.getElementById('recentLeaves').innerHTML = 
            '<div class="text-center text-muted">Error loading recent leaves</div>';
    }
}

function displayRecentLeaves(leaves) {
    const container = document.getElementById('recentLeaves');
    
    if (leaves.length === 0) {
        container.innerHTML = '<div class="text-center text-muted">No recent leave requests</div>';
        return;
    }
    
    const leavesHTML = leaves.map(leave => `
        <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
            <div>
                <strong>${leave.employee?.name || 'Employee'}</strong>
                <div class="small text-muted">
                    ${formatDate(leave.start_date)} - ${formatDate(leave.end_date)}
                    (${leave.days_requested} days)
                </div>
            </div>
            <div class="text-end">
                ${getLeaveTypeBadge(leave.leave_type)}
                ${getStatusBadge(leave.status)}
            </div>
        </div>
    `).join('');
    
    container.innerHTML = leavesHTML;
}

function showApplyLeaveModal() {
    const modal = new bootstrap.Modal(document.getElementById('applyLeaveModal'));
    
   
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('startDate').min = today;
    document.getElementById('endDate').min = today;
    
    modal.show();
}


document.getElementById('applyLeaveForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    if (!validateForm(this)) {
        return;
    }
    
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    setLoadingState(submitBtn, true);
    
    try {
        const formData = {
            employee_id: currentUser.id,
            leave_type: document.getElementById('leaveType').value,
            start_date: document.getElementById('startDate').value,
            end_date: document.getElementById('endDate').value,
            reason: document.getElementById('reason').value
        };
        
        const response = await apiCall('/leaves/', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            showAlert('Leave application submitted successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('applyLeaveModal')).hide();
            this.reset();
            loadRecentLeaves(); 
        } else {
            const error = await response.json();
            showAlert(error.detail || 'Error submitting leave application', 'danger');
        }
    } catch (error) {
        showAlert('Error submitting leave application', 'danger');
    } finally {
        setLoadingState(submitBtn, false, originalText);
    }
});


document.getElementById('startDate').addEventListener('change', function() {
    const startDate = this.value;
    const endDateInput = document.getElementById('endDate');
    endDateInput.min = startDate;
    
    if (endDateInput.value && endDateInput.value < startDate) {
        endDateInput.value = startDate;
    }
});


window.showApplyLeaveModal = showApplyLeaveModal;