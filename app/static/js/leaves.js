

let rawLeavesGlobal = []; 

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.startsWith('/leaves')) {
        loadLeaves();
        if (document.getElementById('myBalance')) {
            showMyLeaveBalance();
        }
        
        document.querySelectorAll('input[name="filterStatus"]').forEach(radio => {
            radio.addEventListener('change', filterAndRenderLeavesTable);
        });
    }
});


async function loadLeaves() {
    try {
        let endpoint = '/leaves';
        if (currentUser && !currentUser.is_admin) {
            endpoint += '/me';
        }
        const response = await apiCall(endpoint);
        if (response.ok) {
            rawLeavesGlobal = await response.json();
            filterAndRenderLeavesTable();
        } else {
            showErrorRow('Error loading leave requests');
        }
    } catch (error) {
        showErrorRow('Network error');
    }
}


function filterAndRenderLeavesTable() {
    const tbody = document.querySelector('#leavesTable tbody');
    tbody.innerHTML = '';
    let filter = document.querySelector('input[name="filterStatus"]:checked');
    filter = filter ? filter.value : 'all';

    let filteredLeaves = rawLeavesGlobal || [];
    if (filter !== 'all') {
        filteredLeaves = filteredLeaves.filter(l => l.status === filter);
    }

    if (filteredLeaves.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No leave requests</td></tr>';
        return;
    }

    filteredLeaves.forEach(leave => {
        let actions = '';
        if (currentUser && currentUser.is_admin && leave.status === 'pending') {
            actions = `
                <button class="btn btn-success btn-sm me-1" onclick="approveLeave(${leave.id})">Approve</button>
                <button class="btn btn-danger btn-sm" onclick="rejectLeave(${leave.id})">Reject</button>
            `;
        }
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${leave.id}</td>
            <td>${leave.employee?.name || leave.employee_id}</td>
            <td>${leave.leave_type || ''}</td>
            <td>${formatDate(leave.start_date)}</td>
            <td>${formatDate(leave.end_date)}</td>
            <td>${leave.days_requested}</td>
            <td>${getStatusBadge(leave.status)}</td>
            <td>${actions}</td>
        `;
        tbody.appendChild(row);
    });
}


function showErrorRow(message) {
    const tbody = document.querySelector('#leavesTable tbody');
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">${message}</td></tr>`;
}


function showApplyLeaveModal() {
    const modal = new bootstrap.Modal(document.getElementById('applyLeaveModal'));
    if (currentUser && currentUser.is_admin && document.getElementById('employeeSelectDiv')) {
        document.getElementById('employeeSelectDiv').style.display = 'block';
    } else if (document.getElementById('employeeSelectDiv')) {
        document.getElementById('employeeSelectDiv').style.display = 'none';
    }
    modal.show();
}


async function approveLeave(leaveId) {
    if (!confirm('Approve this leave request?')) return;
    try {
        const response = await apiCall(`/leaves/${leaveId}/approve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        if (response.ok) {
            showAlert('Leave approved!', 'success');
            loadLeaves();
        } else {
            const err = await response.json();
            showAlert(err.detail || 'Error approving leave', 'danger');
        }
    } catch (error) {
        showAlert('Network error during approval', 'danger');
    }
}

async function rejectLeave(leaveId) {
    if (!confirm('Reject this leave request?')) return;
    try {
        const response = await apiCall(`/leaves/${leaveId}/reject`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        if (response.ok) {
            showAlert('Leave rejected!', 'success');
            loadLeaves();
        } else {
            const err = await response.json();
            showAlert(err.detail || 'Error rejecting leave', 'danger');
        }
    } catch (error) {
        showAlert('Network error during rejection', 'danger');
    }
}


async function showMyLeaveBalance() {
    if (!currentUser) return;
    try {
        const response = await apiCall(`/employees/${currentUser.id}/balance`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('myBalance').textContent = data.leave_balance + " days";
        }
    } catch {
       
    }
}


window.showApplyLeaveModal = showApplyLeaveModal;
window.approveLeave = approveLeave;
window.rejectLeave = rejectLeave;


