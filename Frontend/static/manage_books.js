let currentBookId = null;

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

            if (!book.available) {
                row.style.opacity = '0.5';
            }

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
                            <a class="dropdown-item" href="#" onclick="loadBookForEditing(${book.id})">Edit</a>
                            <a class="dropdown-item text-danger" href="#" onclick="deleteBook(${book.id})">Delete</a>
                        </div>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
}


const fetchBooks = () => {
    axios.get('/books')
        .then(response => {
            const books = response.data;
            display_books(books);
        })
        .catch(error => {
            console.error('Error fetching books:', error);
        });
};

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
                loadBookDetails(book);
            }
        })
        .catch(error => {
            console.error("Error fetching book data:", error);
        });
}
function loadBookDetails(book) {
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
function loadBookForEditing(bookId) {
    currentBookId = bookId;
    axios.get(`/books?book_id=${bookId}`)
        .then(response => {
            const book = response.data;
            console.log("editing book:");
            console.log(book);
            
            console.log('Book name:', book.name);

            // Book Title
            const bookTitleInput = document.getElementById('book-title');
            if (bookTitleInput) {
                bookTitleInput.placeholder = book.name || 'Unknown';
                console.log('bookTitleInput:', bookTitleInput);
            }

            // Author
            const bookAuthorInput = document.getElementById('book-author');
            if (bookAuthorInput) {
                bookAuthorInput.placeholder = book.author || 'Unknown';
            }

            // Year Published
            const bookYearInput = document.getElementById('book-year');
            if (bookYearInput) {
                bookYearInput.placeholder = book.yearPublished || 'Unknown';
            }

            // Genre
            const bookGenreSelect = document.getElementById('book-genre');
            if (bookGenreSelect) {
                bookGenreSelect.value = book.genre || '';
            }

            // Type
            const bookTypeSelect = document.getElementById('book-type');
            if (bookTypeSelect) {
                bookTypeSelect.value = book.type || '';
            }

            // Availability
            const bookAvailableCheckbox = document.getElementById('book-available');
            if (bookAvailableCheckbox) {
                bookAvailableCheckbox.checked = book.available || false;
            }
        })
        .then(() => {
            changeContent("edit_book-content");
        })
        .catch(error => {
            console.error('Error loading book data:', error);
        });

}

function editBook(bookId) {
    // Collect input values
    const title = document.getElementById('book-title').value || document.getElementById('book-title').placeholder;
    const author = document.getElementById('book-author').value || document.getElementById('book-author').placeholder;
    const yearPublished = document.getElementById('book-year').value || document.getElementById('book-year').placeholder;
    const genre = document.getElementById('book-genre').value || '';
    const type = parseInt(document.getElementById('book-type').value) || 1;
    const available = document.getElementById('book-available').checked;

    // Create the payload
    const updatedBook = {
        id: currentBookId,
        name: title,
        author: author,
        yearPublished: yearPublished,
        genre: genre,
        type: type,
        available: available
    };

    // Send the PUT request
    axios.put(`/books`, updatedBook)
        .then(response => {
            console.log('Book updated successfully:', response.data);
            alert('Book updated successfully!');
            // Optionally, redirect to the book list or another page
        })
        .catch(error => {
            console.error('Error updating book:', error);
            alert('Failed to update book. Please try again.');
        });
}

function deleteBook(bookId) {
    const confirmed = confirm(`Are you sure you want to delete this book?`);
    if (confirmed) {
        console.log(bookId);
        axios.delete(`/books`, {
            data: {id : bookId}
        })
        .then(response => {
            alert(`Book has been deleted successfully!`, response.data);
        })
        }
    }

showUnavailableBooks  = () =>{
    axios.get('/books?filter=unavailable')
    .then(response => {
        unavailable_books = response.data
        console.log('Unavailable books:', unavailable_books);
        display_unavailable_books(unavailable_books) 
      })
      .catch(error => {
        console.error('Error fetching unavailable books:', error);
      });
}

const display_unavailable_books = (unavailable_books) =>{
    const tableBody = document.getElementById('books-table-body');
    tableBody.innerHTML = '';
    unavailable_books.forEach((book, index) => {
            const row = document.createElement('tr');

            if (!book.available) {
                row.style.opacity = '0.5';
            }

            row.innerHTML = `
                <td>o</td>
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
                        <button class="btn btn-light">+</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item text-success" href="#" onclick="restoreBook(${book.id})">Restore</a>
                        </div>
                    </div>
                </td>
            `;
            tableBody.appendChild(row);
        });
}

const restoreBook= (bookId) =>{
    const confirmed = confirm(`Restore Book?`);
    if (confirmed) {
        axios.delete(`/books?action=restore`, {
            data: {id : bookId}
        })
        .then(response => {
            alert(`Book has been Restored successfully!`, response.data);
        })
        }
}   