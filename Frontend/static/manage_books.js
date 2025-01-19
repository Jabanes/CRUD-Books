
window.add_book = () => {
    console.log("Attempting to add a book");

    const publication_date = document.getElementById('publicationDate').value;
    let bookYearPublished;

    if (publication_date) {
        const [year, month, day] = publication_date.split('-');
        formattedDate = `${day}-${month}-${year}`; // Convert to '%d-%m-%Y'
        bookYearPublished = parseInt(year)
    }

    const bookData = {
        name: document.getElementById('title').value,
        author: document.getElementById('author').value,
        yearPublished: bookYearPublished,
        genre: document.getElementById('genre').value,
        type: parseInt(document.getElementById('type').value),
    };

    if (!bookData.name || !bookData.author || !bookData.yearPublished || !bookData.genre || isNaN(bookData.type)) {
        alert('Please fill in all fields correctly.');
        return;
    }

    console.log(`the year the book was published is: ${bookYearPublished}`)

    axios.post('http://127.0.0.1:5000/books', bookData)
        

        .then(response => {
            console.log('Book added successfully:', response.data);
            alert('Book added successfully!');
        })
        .catch(error => {
            console.error('Error adding book:', error);
            alert('Failed to add the book. Please try again.');
        });
};

window.load_books = () => axios.get('http://127.0.0.1:5000/books')
    .then(response => {
        console.log(response.data);
        const books = response.data;
        display_books(books)
    })
    .catch(error => console.error('Error fetching books:', error));

const display_books = (books) =>{
    const tableBody = document.getElementById('books-table-body');
        books.forEach((book, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${book.name}</td>
                <td>${book.author}</td>
                <td>
                    <div class="tooltip-container">
                        <a href="#" class="view-icon" onclick="viewBook(${book.id})">
                            <i class="fas fa-eye"></i>
                        </a>
                        <span class="tooltip-text">View Book</span>
                    </div>
                    <div class="options-menu">
                        <button class="btn btn-light">⋮</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item" href="#" onclick="editBook(${book.id})">Edit</a>
                            <a class="dropdown-item text-danger" href="#" onclick="deleteBook(${book.id})">Delete</a>
                        </div>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
}
// Functions to handle View, Edit, and Delete actions
function viewBook(bookId) {
    changeContent('view_book-content')
    axios.get(`/books?book_id=${bookId}`)
        .then(response => {
            // Assuming the response contains the book data
            const book = response.data;
            if (book.message) {
                // Handle the case when no book is found (message is returned)
                alert(book.message);
            } else {
                // If the book data is found, dynamically update the book details page
                updateBookDetails(book);
            }
        })
        .catch(error => {
            console.error("Error fetching book data:", error);
        });
}

function updateBookDetails(book) {
    const bookTitle = document.getElementById("book-title");
    const bookAuthor = document.getElementById("book-author");
    const bookYear = document.getElementById("book-year");
    const bookType = document.getElementById("book-type");
    const bookGenre = document.getElementById("book-genre");
    const bookAvailable = document.getElementById("book-available");
    const bookImage = document.getElementById("book-image");

    // Set the book details
    bookTitle.textContent = book.name || "Unknown Title";
    bookAuthor.textContent = book.author || "Unknown Author";
    bookYear.textContent = book.yearPublished || "Unknown Year";
    bookType.textContent = book.type || "Unknown Type";
    bookGenre.textContent = book.genre || "Unknown Genre";
    bookAvailable.textContent = book.available ? "Yes" : "No";

    // Set the default image if no image is provided
    bookImage.src = book.image || "static/book.jpg";  // Use the default image if no im
}
function editBook(bookId) {
    alert(`Edit book with ID: ${bookId}`);
}

function deleteBook(bookId) {
    const confirmed = confirm(`Are you sure you want to delete the book with ID: ${bookId}?`);
    if (confirmed) {
        alert(`Book with ID: ${bookId} deleted.`);
    }
}
