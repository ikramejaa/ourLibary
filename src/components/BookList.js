import React from 'react';
import axios from 'axios';
import './BookList.css';

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
    <div className="book-list">
      {books.map((book) => (
        <div key={book._id} className="book-card">
          <img src={`http://localhost:5000/images/${book._source.image}`} alt={`Cover of ${book._source.title}`} 
                      style={{ width: '100%', height: '300px' }}  // Ajustez la largeur et la hauteur de l'image
                      />
          <p style={{ fontWeight: 'bold' }}>{book._source.title}</p>
          <p><span style={{ fontWeight: 'bold' }}>Author:</span> {book._source.author}</p>
          <p><span style={{ fontWeight: 'bold' }}>Theme:</span> {book._source.genre.join(', ')}</p>
          <button className="button-card" onClick={() => downloadBook(book._id)}>Download</button>
        </div>
      ))}
    </div>
    </div>
  );
};

export default BookList;
