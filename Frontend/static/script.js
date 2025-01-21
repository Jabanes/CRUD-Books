window.onload = () => {
    loadHomeContent(); // Load the home page content by default when the page loads
};

// Toggle the sidebar visibility
const toggleSidebar = () => {
    const sideMenu = document.getElementById("sideMenu");
    sideMenu.classList.toggle("show");
};

// Function to change the content of the frame based on the content type
const changeContent = (contentType) => {
    console.log("changeContent function called with:", contentType);  // Debugging line
    currentContent = contentType;

    if (contentType === 'home-content') {
        console.log("Loading home.html...");
        loadContentFromFile('static/home.html');  // Change path to static folder
    } else if (contentType === 'add-book') {
        console.log("Loading add-book.html...");
        loadContentFromFile('static/add-book.html');  // Change path to static folder
    } else if (contentType === 'display-books') {
        console.log("Loading display-books.html...");
        loadContentFromFile('static/display-books.html');
        window.load_books()
    } else if (contentType === 'view_book-content') {
        console.log("Loading view_book.html...");
        loadContentFromFile('static/view-book.html');
    }
    else if (contentType === 'edit_book-content') {
        console.log("Loading edit_book.html...");
        loadContentFromFile('static/edit-book.html');
    }
    else if (contentType === 'add-customer') {
        console.log("Loading add-customer.html...");
        loadContentFromFile('static/add-customer.html');
    }
    else if (contentType === 'display-customers') {
        console.log("Loading display-books.html...");
        loadContentFromFile('static/display-customers.html');
        window.load_customers()
    }
    else if (contentType === 'view_customer-content') {
        console.log("Loading view_customer.html...");
        loadContentFromFile('static/view-customer.html');
    }
    else if (contentType === 'edit_customer-content') {
        console.log("Loading edit_customer.html...");
        loadContentFromFile('static/edit-customer.html');
    }
    else {
        // Handle other content types if needed
        const content = '<h4>This is static content</h4>';
        document.getElementById('dynamicFrame').innerHTML = content;

    }
};

const refreshContent = () => {
    console.log("Refreshing content:", currentContent);
    changeContent(currentContent); // Reload the current content
};

// Helper function to load HTML content from file and inject it into the frame
const loadContentFromFile = (filePath) => {
    fetch(filePath)
        .then(response => response.text()) // Read the file content as text
        .then(data => {
            document.getElementById('dynamicFrame').innerHTML = data;  // Inject the content
        })
        .catch(error => {
            console.error(`Error loading ${filePath}:`, error);  // Handle errors
        });
};

// Function to load home content by default
const loadHomeContent = () => {
    console.log("Loading home.html content...");
    loadContentFromFile('static/home.html');  // Change path to static folder
};
  