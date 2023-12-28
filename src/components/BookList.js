import React from 'react';
import axios from 'axios';

const BookList = ({ books }) => {
  const downloadBook = async (bookId) => {
    try {
      // Make a GET request to the back-end endpoint for downloading a book
      const response = await axios.get(`http://localhost:5000/download_book/${bookId}`, {
        responseType: 'blob', // Specify the response type as a binary blob
      });

      // Create a Blob object from the binary data
      const blob = new Blob([response.data], { type: 'application/pdf' });

      // Create a download link and trigger the download
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = 'book.pdf';
      link.click();
    } catch (error) {
      console.error('Error downloading book:', error);
      // Handle errors if necessary
    }
  };

  return (
    <div>
      <h2>Search Results</h2>
      <ul>
        {books.map((book) => (
          <li key={book._id}>
            <p>Title: {book._source.title}</p>
            <p>Author: {book._source.author}</p>
            <p>Genres: {book._source.genre.join(', ')}</p>
            <button onClick={() => downloadBook(book._id)}>Download</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BookList;
