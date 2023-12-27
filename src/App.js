// App.js
import React, { useState } from 'react';
import Search from './components/Search';
import SearchResults from './components/SearchResults';
import './App.css';

const App = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [allResults] = useState([
    {
      id: 1,
      title: 'BURCOLICA GEORGIGA ET AENEIS',
      author: 'PUBLII VIRGLILII',
      image: 'https://ilovetypography.com/img/2016/02/John_Baskerville_1757.jpg',
    },
    {
      id: 2,
      title: 'of THEE I SING',
      author: 'BARACK OBAMA',
      image: 'https://publishdrive.com/media/posts/174/responsive/example-of-book-title-punctuation-xxl.jpg',
    },
    {
      id: 3,
      title: 'HARRY POTTER',
      author: 'JOHN TIFFANY & JACK THORNE',
      image: 'https://bukovero.com/wp-content/uploads/2016/07/Harry_Potter_and_the_Cursed_Child_Special_Rehearsal_Edition_Book_Cover.jpg',
    },
  ]);
  const [searchTerm, setSearchTerm] = useState('');

  // Fonction de recherche qui filtre les résultats en fonction de la valeur de recherche
  const handleSearch = () => {
    // Si la recherche est vide, afficher tous les résultats
    if (!searchTerm) {
      setSearchResults([]);
    } else {
      // Sinon, filtrer les résultats en fonction de la recherche
      const filteredResults = allResults.filter((result) =>
        result.title.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setSearchResults(filteredResults);
    }
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    // Déclencher la recherche à chaque changement de saisie
    handleSearch();
  };

  return (
    <div className="app">
      <header className="header">
        <nav>
          {/* Ajoutez vos liens de navigation ici */}
        </nav>
      </header>
      <Search onSearch={handleSearch} searchTerm={searchTerm} onInputChange={handleInputChange} />
      <SearchResults results={searchResults.length > 0 ? searchResults : allResults} />
    </div>
  );
};

export default App;

