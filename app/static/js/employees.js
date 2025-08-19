document.addEventListener('DOMContentLoaded', function() {
    loadEmployees();

    if (document.getElementById('addEmployeeForm')) {
        document.getElementById('addEmployeeForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            if (!validateForm(this)) return;

            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            setLoadingState(submitBtn, true);

            const formData = {
                name: document.getElementById('employeeName').value,
                email: document.getElementById('employeeEmail').value,
                department: document.getElementById('employeeDepartment').value,
                joining_date: document.getElementById('employeeJoiningDate').value,
                password: document.getElementById('employeePassword').value,
                is_admin: document.getElementById('isAdmin').checked
            };

            try {
                const response = await apiCall('/employees/', {
                    method: 'POST',
                    body: JSON.stringify(formData)
                });
                if (response.ok) {
                    showAlert('Employee added!', 'success');
                    bootstrap.Modal.getInstance(document.getElementById('addEmployeeModal')).hide();
                    this.reset();
                    loadEmployees();
                } else {
                    const err = await response.json();
                    showAlert(err.detail || 'Failed to add employee', 'danger');
                }
            } catch (err) {
                showAlert('Network or server error', 'danger');
            } finally {
                setLoadingState(submitBtn, false, originalText);
            }
        });
    }
});


async function loadEmployees() {
    const tbody = document.querySelector('#employeesTable tbody');
    tbody.innerHTML = '<tr><td colspan="8" class="text-center"><i class="fas fa-spinner fa-spin"></i> Loading employees...</td></tr>';
    try {
        const response = await apiCall('/employees');
        tbody.innerHTML = '';
        if (response.ok) {
            const employees = await response.json();
            if (employees.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No employees</td></tr>';
                return;
            }
            employees.forEach(emp => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${emp.id}</td>
                    <td>${emp.name}</td>
                    <td>${emp.email}</td>
                    <td>${emp.department}</td>
                    <td>${formatDate(emp.joining_date)}</td>
                    <td>${emp.leave_balance}</td>
                    <td>${emp.is_active ? 'Active' : 'Inactive'}</td>
                    <td></td>
                `;
                tbody.appendChild(row);
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Failed to load employees</td></tr>';
        }
    } catch (error) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Network error</td></tr>';
    }
}


function showAddEmployeeModal() {
    const modal = new bootstrap.Modal(document.getElementById('addEmployeeModal'));
    modal.show();
}

window.showAddEmployeeModal = showAddEmployeeModal;

