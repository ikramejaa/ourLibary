import React, { useState } from 'react';
import './Home.css';
import SearchForm from '../SearchForm';
import BookList from '../BookList';

const Home = () => {
  const [searchResults, setSearchResults] = useState([]);

  const handleSearch = (results) => {
    setSearchResults(results);
  };

  return (
    <div>
      <h2>Home Page</h2>
      <SearchForm onSearch={handleSearch} />
      <BookList books={searchResults} />
    </div>
  );
};

export default Home;