import { BrowserRouter as Router,Routes, Route } from 'react-router-dom';
import React from 'react';
import NavBar from './components/NavBar';
import AddBookForm from './components/AddBookForm';
import Home from './components/Home/Home';
import './App.css';


function App() {
    return (
      <Router>
        <div className="App">
        
        <NavBar />
      
          
          
        <div className='Form'>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/add-book" element={<AddBookForm />} />
          </Routes>
          </div>
</div>
      </Router>
    );
  };

export default App;
