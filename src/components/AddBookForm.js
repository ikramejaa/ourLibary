
import React, { useState } from 'react';
import axios from 'axios';

const AddBookForm = () => {
  const [newBook, setNewBook] = useState({
    title: '',
    author: '',
    genre: [],
    link: '',
  });

  const handleInputChange = (e) => {
    setNewBook({ ...newBook, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await axios.post('http://localhost:5000/add_book', newBook);
      console.log('Book added successfully');
    } catch (error) {
      console.error('Error adding book:', error);
    }
  };

  return (
    <div>
      <h2>Add a New Book</h2>
      <form>
        <label>Title:</label>
        <input type="text" name="title" onChange={handleInputChange} />

        <label>Author:</label>
        <input type="text" name="author" onChange={handleInputChange} />

        <label>Genre:</label>
        <input type="text" name="genre" onChange={handleInputChange} />

        <label>Link:</label>
        <input type="text" name="link" onChange={handleInputChange} />

        <button type="button" onClick={handleSubmit}>
          Add Book
        </button>
      </form>
    </div>
  );
};

export default AddBookForm;
