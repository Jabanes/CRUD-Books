
let currentCustomerId = null;

const addCustomer = () => {
    console.log("Attempting to add a customer");

    const birth_date = document.getElementById('birth-date').value;
    let customerAge;

    if (birth_date) {
        const [year, month, day] = birth_date.split('-').map(Number); // Extract year, month, and day as numbers
        const birthDateObj = new Date(year, month - 1, day); // Create a date object for the birth date
        const today = new Date(); // Current date
    
        // Calculate the age
        customerAge = today.getFullYear() - birthDateObj.getFullYear();
    
        // Adjust if the birthday hasn't occurred yet this year
        const birthdayPassedThisYear =
            today.getMonth() > birthDateObj.getMonth() ||
            (today.getMonth() === birthDateObj.getMonth() && today.getDate() >= birthDateObj.getDate());
    
        if (!birthdayPassedThisYear) {
            customerAge--;
        }
    }

    const customerData = {
        name: document.getElementById('customer-name').value,
        city: document.getElementById('city').value,
        age: customerAge,
    };

    if (!customerData.name || !customerData.city || !customerData.age) {
        alert('Please fill in all fields correctly.');
        return;
    }


    axios.post('http://127.0.0.1:5000/customers', customerData)


        .then(response => {
            console.log('customer added successfully:', response.data);
            alert('Customer added successfully!');
        })
        .catch(error => {
            console.error('Error adding customer:', error);
            alert('Failed to add the Customer. Please try again.');
        });
}

window.load_customers = () => axios.get('http://127.0.0.1:5000/customers')
    .then(response => {
        console.log(response.data);
        const customers = response.data;
        display_customers(customers)
    })
    .catch(error => console.error('Error fetching customers:', error));


const display_customers = (customers) => {
    const tableBody = document.getElementById('customers-table-body');
    document.getElementById('customers-title').innerHTML = 'Active Customers'
    customers.forEach((customer, index) => {
        const row = document.createElement('tr');

        if (!customer.active) {
            row.style.opacity = '0.5';
        }

        row.innerHTML = `
                <td>${index + 1}</td>
                <td>${customer.name}</td>
                <td>${customer.city}</td>
                <td>${customer.age}</td>

                <td>
                    <div class="tooltip-container">
                        <a href="#" class="view-icon" onclick="viewCustomer(${customer.id})">
                            <i class="fas fa-eye"></i>
                        </a>
                        <span class="tooltip-text">View customer</span>
                    </div>
                    <div class="options-menu">
                        <button class="btn btn-light">⋮</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="#" onclick="loadCustomerForEditing(${customer.id})">Edit</a>
                            <a class="dropdown-item text-danger" href="#" onclick="deleteCustomer(${customer.id})">Delete</a>
                        </div>
                    </div>
                </td>
            `;
        tableBody.appendChild(row);
    });
}

const viewCustomer = (customerId) => {
    currentCustomerId = customerId
    changeContent('view_customer-content')
    axios.get(`http://127.0.0.1:5000/customers?customer_id=${customerId}`)
        .then(response => {
            console.log(response.data);
            const customer = response.data;
            if (customer.message) {
                // Handle the case when no customer is found (message is returned)
                alert(customer.message);
            } else {
                // If the Customer data is found, dynamically update the customer details page
                loadCustomerDetails(customer);
            }
        })
        .catch(error => {
            console.error("Error fetching customer data:", error);
            console.log(`Current customer id = ${customerId}`);
        });
}

const loadCustomerDetails = (customer)=> {
    const customerName = document.getElementById("customer-name");
    const customerCity = document.getElementById("customer-city");
    const customerAge = document.getElementById("customer-age");
    const customerActive = document.getElementById("customer-active");
    const customerImage = document.getElementById("customer-image");
    // Set the Customers details
    customerName.textContent = customer.name || "Unknown Name";
    customerCity.textContent = customer.city || "Unknown City";
    customerAge.textContent = customer.age || "Unknown Age";
    customerActive.textContent = customer.active ? "Yes" : "No";
    // Set the default image if no image is provided
    customerImage.src = customer.image || "static/customer.jpg";  // Use the default image if no im
}

const loadCustomerForEditing =(customerId) => {
    currentCustomerId = customerId;
   
    axios.get(`/customers?customer_id=${customerId}`)
        .then(() => {
            changeContent("edit_customer-content");
        })
        .catch(error => {
            console.error('Error loading customer data:', error);
        });

}

const editcustomer = () =>{
    const name = document.getElementById('customer-name').value || null;
    const city = document.getElementById('customer-city').value || null;
    const age = document.getElementById('customer-age').value || null;
   

    const updatedCustomer = {
        id: currentCustomerId,
        name: name,
        city: city,
        age: age
    };

    // Send the PUT request
    axios.put(`/customers`, updatedCustomer)
        .then(response => {
            console.log('Customer updated successfully:', response.data);
            alert('Customer updated successfully!');
            // Optionally, redirect to the customer list or another page
        })
        .catch(error => {
            console.error('Error updating Customer:', error);
            alert('Failed to update Customer. Please try again.');
        });
}

const  deleteCustomer = (customerId) => {
    const confirmed = confirm(`Are you sure you want to delete this customer?`);
    if (confirmed) {
        console.log(customerId);
        axios.delete(`http://127.0.0.1:5000/customers`, {
            data: { id: customerId }
        })

        .then(response => {
            alert(`Customer has been deleted successfully!`, response.data);
            
        })
    }
}

getInactiveCustomers = () => {
    axios.get('http://127.0.0.1:5000/customers?filter=inactive')
        .then(response => {
            inactive_customers = response.data
            console.log('Unavailable Customers:', inactive_customers);
            displayInactiveCustomers(inactive_customers)
        })
        .catch(error => {
            console.error('Error fetching unavailable customers:', error);
        });
}

const displayInactiveCustomers = (inactive_customers) => {
    const tableBody = document.getElementById('customers-table-body');
    document.getElementById('customers-title').innerHTML = 'Inactive Customers';
    tableBody.innerHTML = '';
    inactive_customers.forEach((customer) => {
        const row = document.createElement('tr');

        if (!customer.available) {
            row.style.opacity = '0.5';
        }

        row.innerHTML = `
                <td>o</td>
                <td>${customer.name}</td>
                <td>${customer.city}</td>
                <td>${customer.age}</td>
                <td>
                    <div class="tooltip-container">
                        <a href="#" class="view-icon" onclick="viewCustomer(${customer.id})">
                            <i class="fas fa-eye"></i>
                        </a>
                        <span class="tooltip-text">View Customer</span>
                    </div>
                    <div class="options-menu">
                        <button class="btn btn-light">+</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item text-success" href="#" onclick="restoreCustomer(${customer.id})">Restore</a>
                        </div>
                    </div>
                </td>
            `;
        tableBody.appendChild(row);
    });
}
const restoreCustomer = (customerId) => {
    const confirmed = confirm(`Restore Customer?`);
    if (confirmed) {
        axios.delete(`http://127.0.0.1:5000/customers?action=restore`, {
            data: { id: customerId }
        })
        .then(response => {
            alert(`Customer has been Restored successfully!`, response.data);
        })
    }
}

const getCustomerResult= (customers, query = '') => {
    const tableBody = document.getElementById('customers-table-body');
    tableBody.innerHTML = ''; // Clear the table before displaying new data

    // Convert the query to lowercase for case-insensitive comparison
    const lowerCaseQuery = query.toLowerCase();

    // Filter customers based on the query (if provided)
    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(lowerCaseQuery) ||
        customer.city.toLowerCase().includes(lowerCaseQuery) ||
        customer.age.toString().includes(lowerCaseQuery)
    );

    // Check if there are any matching customers
    if (filteredCustomers.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center">No customers found</td>
            </tr>
        `;
        return;
    }

    // Display the filtered customers
    filteredCustomers.forEach((customer, index) => {
        const row = document.createElement('tr');

        if (!customer.active) {
            row.style.opacity = '0.5';
        }

        row.innerHTML = `
                <td>#</td>
                <td>${customer.name}</td>
                <td>${customer.city}</td>
                <td>${customer.age}</td>
                <td>
                    <div class="tooltip-container">
                        <a href="#" class="view-icon" onclick="viewCustomer(${customer.id})">
                            <i class="fas fa-eye"></i>
                        </a>
                        <span class="tooltip-text">View Customer</span>
                    </div>
                    <div class="options-menu">
                        <button class="btn btn-light">+</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item text-success" href="#" onclick="restoreCustomer(${customer.id})">Restore</a>
                        </div>
                    </div>
                </td>
            `;
        tableBody.appendChild(row);
    });
};

const searchCustomer =() => {
    axios.get('http://127.0.0.1:5000/customers')
    .then(response => {
        console.log(response.data);
        const customers = response.data;
        const query = document.getElementById('search-bar').value.trim();
        getCustomerResult(customers, query); 
    })

    .catch(error => console.error('Error fetching customers:', error));
    
}