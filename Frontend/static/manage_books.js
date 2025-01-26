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
        updateCarouselWithRandomBook(books);
    })
    .catch(error => console.error('Error fetching books:', error));




window.load_loans = () => axios.get('http://127.0.0.1:5000/loans')
.then(response => {
    const loans = response.data;
    displayActiveLoans(loans)
})
.catch(error => console.error('Error fetching customers:', error));


const display_books = (books) => {
    const tableBody = document.getElementById('books-table-body');
    document.getElementById('books-title').innerHTML = 'Available Books:'
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

function viewBook(bookId) {
    changeContent('view_book-content')
    axios.get(`http://127.0.0.1:5000/books?book_id=${bookId}`)
        .then(response => {
            // Assuming the response contains the book data
            const book = response.data;
            
            if (book.message) {
                // Handle the case when no book is found (message is returned)
                alert(book.message);
            } else {
                currentBookId = book.id
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
            console.log(`editing book: ${book}`);
        })
        .then(() => {
            changeContent("edit_book-content");
        })
        .catch(error => {
            console.error('Error loading book data:', error);
        });

}

function editBook() {

    // Collect input values
    const title = document.getElementById('book-title').value || null;
    const author = document.getElementById('book-author').value || null;
    const yearPublished = document.getElementById('book-year').value || null;
    const genre = document.getElementById('book-genre').value || null;;
    const type = parseInt(document.getElementById('book-type').value) || null;;

    // Create the payload
    const updatedBook = {
        id: currentBookId,
        name: title,
        author: author,
        yearPublished: yearPublished,
        genre: genre,
        type: type,
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
        axios.delete(`http://127.0.0.1:5000/books`, {
            data: { id: bookId }
        })
            .then(response => {
                alert(`Book has been deleted successfully!`, response.data);
            })
    }
}

getUnavailableBooks = () => {
    axios.get('http://127.0.0.1:5000/books?filter=unavailable')
        .then(response => {
            unavailable_books = response.data
            console.log('Unavailable books:', unavailable_books);
            display_unavailable_books(unavailable_books)
        })
        .catch(error => {
            console.error('Error fetching unavailable books:', error);
        });
}

const display_unavailable_books = (unavailable_books) => {
    const tableBody = document.getElementById('books-table-body');
    document.getElementById('books-title').innerHTML = 'Unavailable Books:'
    tableBody.innerHTML = '';
    unavailable_books.forEach((book) => {
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

const restoreBook = (bookId) => {
    const confirmed = confirm(`Restore Book?`);
    if (confirmed) {
        axios.delete(`/books?action=restore`, {
            data: { id: bookId }
        })
            .then(response => {
                alert(`Book has been Restored successfully!`, response.data);
            })
    }
}  

const loanbook = (book_id) => {
    
    book_id = currentBookId
    console.log("Attempting to loan a book...");
    console.log(book_id);
    
    
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');

    let todaysDate = `${day}-${month}-${year}`
    let customerId = 1     // change this when implementing user auth
    

    loanData = {
        "customer_id" : customerId,
        "book_id" : book_id,
        "loan_date" : todaysDate
    }

    axios.post('http://127.0.0.1:5000/loans', loanData).then(response => {
        
        const loan = response.data;
        if (loan.message) {
            // Handle the case when no book is found (message is returned)
            alert(loan.message);
        } else {
            // If the book data is found, dynamically update the book details page
            loadBookDetails(loan);
        }
    })
    .catch(error => {
        console.error("loan failed...", error);
    });
    
}

const getBookResult= (books, query = '') => {
    const tableBody = document.getElementById('books-table-body');
    tableBody.innerHTML = ''; // Clear the table before displaying new data

    // Convert the query to lowercase for case-insensitive comparison
    const lowerCaseQuery = query.toLowerCase();

    // Filter books based on the query (if provided)
    const filteredBooks = books.filter(book => 
        book.name.toLowerCase().includes(lowerCaseQuery) ||
        book.author.toLowerCase().includes(lowerCaseQuery)
    );

    // Check if there are any matching books
    if (filteredBooks.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center">No books found</td>
            </tr>
        `;
        return;
    }

    // Display the filtered books
    filteredBooks.forEach((book, index) => {
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
};

const searchBook =() => {
    axios.get('http://127.0.0.1:5000/books')
    .then(response => {
        console.log(response.data);
        const books = response.data;
        const query = document.getElementById('search-bar').value.trim();
        getBookResult(books, query); 
    })

    .catch(error => console.error('Error fetching books:', error));
    
}
//-----------------------------------------------------------------------------------------------------


const displayActiveLoans = (activeLoans) =>{
    const tableBody = document.getElementById('books-table-body');
    tableBody.innerHTML = '';
    const title = document.getElementById('loan-title');
    title.innerHTML = 'Active Loans'
    let status = '';
    activeLoans.forEach((loan, index) => {
        const row = document.createElement('tr');

        if (loan.is_returned) {
            row.style.opacity = '0.5';
            status = "Returned"
        }

        if (!loan.is_returned) {
            status = "Active"
        }
        row.innerHTML = `
                <td>${index + 1}</td>
                <td>${loan.customer}</td>
                <td>${loan.book_id}</td>
                <td>${loan.loan_date}</td>
                <td>${loan.return_date}</td>
                <td>${status}</td>
                <td>
                    <div class="options-menu">
                        <button class="btn btn-light">+</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item text-success" href="#" onclick="returnLoan(${loan.loan_id})">Return</a>
                        </div>
                    </div>
                </td>
            `;
        tableBody.appendChild(row);
    });
}

const displayLateLoans = (late_loans) => {
    const tableBody = document.getElementById('books-table-body');
    const title = document.getElementById('loan-title');
    title.innerHTML = 'Late Loans'
    tableBody.innerHTML = '';
    let status = '';
    late_loans.forEach((loan, index) => {
        const row = document.createElement('tr');

        if (loan.is_returned) {
            row.style.opacity = '0.6';
            status = "Returned"
        }

        if (!loan.is_returned) {
            row.style.color = 'red'
            status = "Active"
        }
        row.innerHTML = `
                <td>${index + 1}</td>
                <td>${loan.customer}</td>
                <td>${loan.book_id}</td>
                <td>${loan.loan_date}</td>
                <td>${loan.return_date}</td>
                <td>${status}</td>
                <td>
                    <div class="options-menu">
                        <button class="btn btn-light">+</button>
                        <div class="dropdown-menu">
                            <a class="dropdown-item text-success" href="#" onclick="returnLoan(${loan.id})">Return</a>
                        </div>
                    </div>
                </td>
            `;
        tableBody.appendChild(row);
    });
}

getLateLoans = () => {
    axios.get("http://127.0.0.1:5000/loans?filter=late")
    .then(response => {
        late_loans = response.data
        console.log('late loans:', late_loans);
        displayLateLoans(late_loans)
    })
    .catch(error => {
        console.error('Error fetching late loans:', error);
    });
}

getReturnedLoans = () => {
    axios.get("http://127.0.0.1:5000/loans?filter=returned")
    .then(response => {
        returned_loans = response.data
        console.log('late loans:', returned_loans);
        displayReturnedLoans(returned_loans)
    })
    .catch(error => {
        console.error('Error fetching late loans:', error);
    });
}

const displayReturnedLoans = (returned_loans) => {
    const tableBody = document.getElementById('books-table-body');
    const title = document.getElementById('loan-title');
    title.innerHTML = 'Returned Loans'
    tableBody.innerHTML = '';
    let status = '';
    returned_loans.forEach((loan, index) => {
        const row = document.createElement('tr');

        if (loan.is_returned) {
            row.style.opacity = '0.7';
            row.style.color = 'green';
            status = "Returned"
        }

        if (!loan.is_returned) {
            status = "Active"
        }
        row.innerHTML = `
                <td>${index + 1}</td>
                <td>${loan.customer}</td>
                <td>${loan.book_id}</td>
                <td>${loan.loan_date}</td>
                <td>${loan.return_date}</td>
                <td>${status}</td>
            `;
        tableBody.appendChild(row);
    });
}

getLoanHistory = () => {
    axios.get("http://127.0.0.1:5000/loans?filter=history")
    .then(response => {
        loans_history = response.data
        console.log('late loans:', loans_history);
        displayLoansHistory(loans_history)
    })
    .catch(error => {
        console.error('Error fetching late loans:', error);
    });
}

const displayLoansHistory = async (all_loans) =>{
    const tableBody = document.getElementById('books-table-body');
    const title = document.getElementById('loan-title');
    title.innerHTML =  'Loans History'
    tableBody.innerHTML = '';
    let status = '';
    const late_loans_list = await lateLoans();

    all_loans.forEach((loan, index) => {
        const row = document.createElement('tr');

        if (loan.is_returned) {
            row.style.opacity = '0.7';
            row.style.color = 'green';
            status = "Returned"
        }

        else if (!loan.is_returned && late_loans_list.some(lateLoan => lateLoan.loan_id === loan.loan_id)) {
            status = "Active, Late"
            row.style.color = 'red';
        }

        else {
            status = "Active"
        }

        row.innerHTML = `
                <td>${index + 1}</td>
                <td>${loan.customer}</td>
                <td>${loan.book_id}</td>
                <td>${loan.loan_date}</td>
                <td>${loan.return_date}</td>
                <td>${status}</td>
            `;
        tableBody.appendChild(row);
    });
}

const lateLoans = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/loans?filter=late");
        return response.data; // Return the list of late loans
    } catch (error) {
        console.error('Error fetching late loans:', error);
        return []; // Return an empty list in case of error
    }
};

const returnLoan = (loan_id) =>{
    const confirmed = confirm(`Are you sure you want to mark this loan as returned?`);
    if (confirmed) {
        console.log(loan_id);
        axios.delete(`http://127.0.0.1:5000/loans`, {
            data: { loan_id: loan_id }
        })
        .then(response => {
            alert(`loan has been returned successfully!`, response.data);
        })
    
}}

const updateCarouselWithRandomBook = (books) => {
    const randomIndex = Math.floor(Math.random() * books.length);
    const randomBook = books[randomIndex];

    
    const carouselItem = document.querySelector('.carousel-item.active');
    if (carouselItem && randomBook) {
        carouselItem.querySelector('img').src = '/static/book.jpg'
        carouselItem.querySelector('h5').textContent = randomBook.name; 
    }
};