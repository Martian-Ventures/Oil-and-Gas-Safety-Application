// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    initTabs();
    
    // Set default dates
    setDefaultDates();
    
    
    // Add event listener for save audit button
    document.getElementById('save-audit').addEventListener('click', saveAudit);
});

function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
            
            // Update breadcrumb and page title based on active tab
            updatePageInfo(tabId);
        });
    });
}

function updatePageInfo(tabId) {
    const breadcrumb = document.getElementById('breadcrumb');
    const pageTitle = document.getElementById('pageTitle');
    
    switch(tabId) {
        case 'new-audit':
            breadcrumb.textContent = 'Home / Audit Management / New Audit';
            pageTitle.textContent = 'New Audit';
            break;
        case 'audit-details':
            breadcrumb.textContent = 'Audit Management / View All Audit / Audit Details';
            pageTitle.textContent = 'Audit Details';
            break;
    }
}

function setDefaultDates() {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    
    // Set default dates for audit forms
    const auditDate = document.getElementById('audit-date');
    const conductedDate = document.getElementById('conducted-date');
    
    if (auditDate) auditDate.value = formattedDate;
    if (conductedDate) conductedDate.value = formattedDate;
}

function saveAudit() {
    // Basic form validation
    const requiredFields = document.querySelectorAll('.required');
    let isValid = true;
    
    requiredFields.forEach(field => {
        const input = field.closest('.form-group').querySelector('input, select, textarea');
        if (input && !input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'red';
        } else if (input) {
            input.style.borderColor = '#ddd';
        }
    });
    
    if (!isValid) {
        alert('Please fill in all required fields marked with *');
        return;
    }
    
    // Simulate saving data
    alert('Audit saved successfully!');
    
    // In a real application, you would send data to a server here
    // Example:
    // const auditData = {
    //     organization: document.getElementById('organization').value,
    //     auditStandard: document.getElementById('audit-standard').value,
    //     auditDate: document.getElementById('audit-date').value,
    //     // ... other fields
    // };
    // 
    // fetch('/api/audits', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(auditData)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     alert('Audit saved successfully!');
    // })
    // .catch(error => {
    //     alert('Error saving audit: ' + error.message);
    // });
}

// Additional utility functions
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-GB'); // DD/MM/YYYY format
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Export functions for use in other modules (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initTabs,
        updatePageInfo,
        setDefaultDates,
        saveAudit,
        formatDate,
        validateEmail
    };
}

// Tab functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tabs
    initTabs();
    
    // Set default dates
    setDefaultDates();
    
    // Add event listener for save audit button
    document.getElementById('save-audit').addEventListener('click', saveAudit);
    
    // Add event listener for save plan button
    document.getElementById('save-plan').addEventListener('click', saveAuditPlan);
    
    // Add event listener for send approval button
    document.getElementById('send-approval').addEventListener('click', sendForApproval);
    
    // Add interactivity to audit plan table
    initAuditPlanTable();
});

function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs and contents
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab
            tab.classList.add('active');
            
            // Show corresponding content
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
            
            // Update breadcrumb and page title based on active tab
            updatePageInfo(tabId);
        });
    });
}

function updatePageInfo(tabId) {
    const breadcrumb = document.getElementById('breadcrumb');
    const pageTitle = document.getElementById('pageTitle');
    
    switch(tabId) {
        case 'audit-plan':
            breadcrumb.textContent = 'Home / Audit Management / Audit Plan';
            pageTitle.textContent = 'Audit Plan';
            break;
        case 'new-audit':
            breadcrumb.textContent = 'Home / Audit Management / New Audit';
            pageTitle.textContent = 'New Audit';
            break;
        case 'audit-details':
            breadcrumb.textContent = 'Audit Management / View All Audit / Audit Details';
            pageTitle.textContent = 'Audit Details';
            break;
    }
}

function setDefaultDates() {
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    
    // Set default dates for audit forms
    const auditDate = document.getElementById('audit-date');
    const conductedDate = document.getElementById('conducted-date');
    const planDate = document.getElementById('plan-date');
    
    if (auditDate) auditDate.value = formattedDate;
    if (conductedDate) conductedDate.value = formattedDate;
    if (planDate) planDate.value = formattedDate;
}

function saveAudit() {
    // Basic form validation
    const requiredFields = document.querySelectorAll('.required');
    let isValid = true;
    
    requiredFields.forEach(field => {
        const input = field.closest('.form-group').querySelector('input, select, textarea');
        if (input && !input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'red';
        } else if (input) {
            input.style.borderColor = '#ddd';
        }
    });
    
    if (!isValid) {
        alert('Please fill in all required fields marked with *');
        return;
    }

    if (!validateNewAuditForm()) {
        alert('Please fill in all required fields marked with *');
        return;
    }
    
    // Simulate saving data
    alert('Audit saved successfully!');
}

function saveAuditPlan() {
    const standard = document.getElementById('plan-standard').value;
    const date = document.getElementById('plan-date').value;
    
    if (!standard || !date) {
        alert('Please select both Standard and Plan Date');
        return;
    }
    
    // Simulate saving audit plan
    alert('Audit Plan saved successfully!');
    
    // In a real application, you would send data to a server here
    // and update the table accordingly
}

function sendForApproval() {
    // Simulate sending for approval
    const confirmation = confirm('Are you sure you want to send this audit plan for approval?');
    
    if (confirmation) {
        alert('Audit Plan has been sent for approval successfully!');
        
        // In a real application, you would update the status and send notifications
    }
}

function initAuditPlanTable() {
    const auditIcons = document.querySelectorAll('.planned-audit');
    
    auditIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const month = this.parentElement.cellIndex - 2; // Adjust for # and Organization columns
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                           'July', 'August', 'September', 'October', 'November', 'December'];
            const organization = this.parentElement.parentElement.cells[1].textContent;
            
            const action = confirm(`Schedule audit for ${organization} in ${months[month]}?`);
            
            if (action) {
                // In a real application, you would update the database here
                this.style.color = '#e74c3c'; // Change color to indicate action
                setTimeout(() => {
                    this.style.color = '#2ecc71'; // Change back after a moment
                }, 1000);
            }
        });
    });
}

// Additional utility functions
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleDateString('en-GB'); // DD/MM/YYYY format
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Export functions for use in other modules (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initTabs,
        updatePageInfo,
        setDefaultDates,
        saveAudit,
        saveAuditPlan,
        sendForApproval,
        initAuditPlanTable,
        formatDate,
        validateEmail
    };
}

// Additional function for new audit form validation
function validateNewAuditForm() {
    const requiredFields = [
        'organization', 'audit-type', 'audit-standard', 'scope',
        'audit-date', 'audit-time', 'duration', 'auditor', 
        'lead-auditor', 'auditee'
    ];
    
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            isValid = false;
            field.style.borderColor = 'red';
        } else if (field) {
            field.style.borderColor = '#ddd';
        }
    });
    
    // Validate shift selection
    const shiftSelected = document.querySelector('input[name="shift"]:checked');
    if (!shiftSelected) {
        isValid = false;
        document.querySelector('.shift-options').style.outline = '2px solid red';
        document.querySelector('.shift-options').style.padding = '5px';
    } else {
        document.querySelector('.shift-options').style.outline = 'none';
    }
    
    return isValid;
}

// Function to handle update audit button
document.getElementById('update-audit').addEventListener('click', function() {
    // Validate form before updating
    if (validateAuditDetailsForm()) {
        // Simulate update process
        alert('Audit details updated successfully!');
        
        // In real application, you would send data to server here
        // Example:
        // const auditData = {
        //     conductedDate: document.getElementById('conducted-date').value,
        //     auditSummary: document.getElementById('audit-summary').value,
        //     references: document.getElementById('references').value
        // };
        // 
        // fetch('/api/audits/update', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(auditData)
        // })
        // .then(response => response.json())
        // .then(data => {
        //     alert('Audit details updated successfully!');
        // })
        // .catch(error => {
        //     alert('Error updating audit: ' + error.message);
        // });
    }
});

// Function to validate audit details form
function validateAuditDetailsForm() {
    const requiredFields = [
        'conducted-date', 'audit-summary', 'references'
    ];
    
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field && !field.value.trim()) {
            isValid = false;
            field.style.borderColor = 'red';
        } else if (field) {
            field.style.borderColor = '#ddd';
        }
    });
    
    if (!isValid) {
        alert('Please fill in all required fields');
        return false;
    }
    
    return true;
}

// Function to handle search functionality
document.querySelectorAll('.search-input').forEach(input => {
    input.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const table = this.closest('.table-container').querySelector('table');
        const rows = table.querySelectorAll('tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});

// Function to handle add buttons
document.querySelectorAll('.table-actions .btn.btn-success').forEach(button => {
    button.addEventListener('click', function() {
        const tableTitle = this.closest('.table-header').querySelector('h3').textContent;
        
        if (tableTitle === 'Document Attachment') {
            // Handle upload functionality
            alert('Upload document functionality would open here');
            // In real application, you would trigger file upload dialog
            // document.getElementById('file-input').click();
        } else {
            // Handle add new record functionality
            alert('Add new ' + tableTitle.toLowerCase() + ' functionality would open here');
        }
    });
});

// Function to handle Close button in Document List
document.querySelector('.document-actions .btn-danger').addEventListener('click', function() {
    const confirmation = confirm('Are you sure you want to close this audit? This action cannot be undone.');
    
    if (confirmation) {
        // Simulate closing the audit
        alert('Audit closed successfully!');
        
        // In real application, you would update the audit status
        // Example:
        // fetch('/api/audits/close', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ auditId: 'current-audit-id' })
        // })
        // .then(response => response.json())
        // .then(data => {
        //     alert('Audit closed successfully!');
        //     // Redirect or refresh the page
        //     window.location.reload();
        // })
        // .catch(error => {
        //     alert('Error closing audit: ' + error.message);
        // });
    }
});

// Function to highlight the correct sidebar menu item
/*function highlightSidebarMenu() {
    const currentPage = window.location.pathname;
    const menuItems = document.querySelectorAll('.menu li');
    
    // Remove active class from all menu items
    menuItems.forEach(item => item.classList.remove('active'));
    
    // Determine which menu item should be active based on current content
    const pageTitle = document.getElementById('pageTitle').textContent;
    const breadcrumb = document.getElementById('breadcrumb').textContent;
    
    if (breadcrumb.includes('Audit Management') || pageTitle.includes('Audit')) {
        // Highlight Audit Management
        menuItems[1].classList.add('active'); // Audit Management is the second item (index 1)
    } else if (breadcrumb.includes('Dashboard') || pageTitle.includes('Dashboard')) {
        // Highlight Dashboard
        menuItems[0].classList.add('active'); // Dashboard is the first item (index 0)
    }
    // Add more conditions for other menu items as needed
}

// Call this function when the page loads and when tabs change
document.addEventListener('DOMContentLoaded', function() {
    highlightSidebarMenu();
});

// Also call it when tabs are switched (add this to your tab click event)
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // ... existing tab switching code ...
            
            // Update sidebar highlighting
            highlightSidebarMenu();
        });
    });
} */