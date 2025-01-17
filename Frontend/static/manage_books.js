window.add_book = () => {
    console.log("Attempting to add a book");

    const publication_date = document.getElementById('publicationDate').value;
    

    if (publication_date) {
        const [year, month, day] = publication_date.split('-');
        formattedDate = `${day}-${month}-${year}`; // Convert to '%d-%m-%Y'
    }

    const bookData = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        publication_date: formattedDate,
        genre: document.getElementById('genre').value,
        type: parseInt(document.getElementById('type').value),
    };

    if (!bookData.title || !bookData.author || !bookData.publication_date || !bookData.genre || isNaN(bookData.type)) {
        alert('Please fill in all fields correctly.');
        return;
    }

    axios.post('http://127.0.0.1:5000/books', bookData)
        console.log(bookData)

        .then(response => {
            console.log('Book added successfully:', response.data);
            alert('Book added successfully!');
        })
        .catch(error => {
            console.error('Error adding book:', error);
            alert('Failed to add the book. Please try again.');
        });
};
