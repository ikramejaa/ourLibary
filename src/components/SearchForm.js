// SearchForm.js
import React, { useState } from 'react';
import axios from 'axios';

const SearchForm = ({ onSearch }) => {
  const [query, setQuery] = useState('');

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/search_books', { query });
      onSearch(response.data);
    } catch (error) {
      console.error('Error searching books:', error);
    }
  };

  return (
    <div className="Search">
      <input type="text" value={query} onChange={(e) => setQuery(e.target.value)}
       placeholder="Search for Book, Author or Theme"  />
      <button className="button-search" onClick={handleSearch}>Search</button>
    </div>
  );
};

export default SearchForm;
