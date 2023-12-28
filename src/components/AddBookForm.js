import React, { useState } from 'react';
import axios from 'axios';

const AddBookForm = () => {
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    genre: [],
  });

  const handleInputChange = (e) => {
    setNewBook({ ...newBook, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission

    try {
      // Split the genre string into an array (assuming genres are comma-separated)
      const genresArray = newBook.genre.split(',').map((genre) => genre.trim());

      // Update the state with the genres array
      setNewBook({ ...newBook, genre: genresArray });

      await axios.post('http://localhost:5000/add_book', newBook);
      console.log('Book added successfully');
    } catch (error) {
      console.error('Error adding book:', error);
    }
  };

  return (
    <div>
      <h2>Add a New Book</h2>
      <form onSubmit={handleSubmit}>
        <label>Title:</label>
        <input type="text" name="title" onChange={handleInputChange} />

        <label>Author:</label>
        <input type="text" name="author" onChange={handleInputChange} />

        <label>Genre (comma-separated):</label>
        <input type="text" name="genre" onChange={handleInputChange} />

        <button type="submit">Add Book</button>
      </form>
    </div>
  );
};

export default AddBookForm;
