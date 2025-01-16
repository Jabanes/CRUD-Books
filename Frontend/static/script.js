// Call the function when the page loads
window.onload = function() {
    loadHomeContent();
};

const SERVER = "http://127.0.0.1:5000"
axios.get().then(res=> console.log(res.data))

function toggleSidebar() {
    var sideMenu = document.getElementById("sideMenu");
    sideMenu.classList.toggle("show");
}

function changeContent(contentType) {
    console.log("changeContent function called with:", contentType);  // Debugging line
    var content = '';

    if (contentType === 'home-content') {
        console.log("Attempting to load home.html");  // Debugging line
        axios.get('/home')
            .then(response => {
                document.getElementById('dynamicFrame').innerHTML = response.data;
            })
            .catch(error => {
                console.error('Error loading home.html:', error);
            });
    } else {
        // Handle other content types...
        content = '<h4>This is static content</h4>';
        document.getElementById('dynamicFrame').innerHTML = content;
    }
}

function loadHomeContent() {
    console.log("Loading home.html content...");
    axios.get('/home')
        .then(response => {
            document.getElementById('dynamicFrame').innerHTML = response.data;
        })
        .catch(error => {
            console.error('Error loading home.html:', error);
        });
}

