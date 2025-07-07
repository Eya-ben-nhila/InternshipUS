import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Scanner from './pages/Scanner';
import Results from './pages/Results';
import JobMatcher from './pages/JobMatcher';
import Profile from './pages/Profile';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import './App.css';

function ComingSoon() {
  return (
    <div style={{ minHeight: '60vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', background: '#f8fafc' }}>
      <h1 style={{ color: '#2563eb', fontSize: '2.5rem', marginBottom: 16 }}>Coming Soon</h1>
      <p style={{ color: '#64748b', fontSize: '1.2rem' }}>This page is under construction. Please check back later!</p>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="js-app">
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scan" element={<Scanner />} />
            <Route path="/results" element={<Results />} />
            <Route path="/match" element={<JobMatcher />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/coming-soon" element={<ComingSoon />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}