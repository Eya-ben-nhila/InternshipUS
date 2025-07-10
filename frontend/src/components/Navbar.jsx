import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  const links = [
    { name: 'Home', path: '/' },
    { name: 'Resume & Job Matcher', path: '/scan' },
    { name: 'Profile', path: '/profile' },
  ];

  return (
    <nav className="js-navbar">
      <div className="js-nav-container">
        {/* Logo */}
        <Link to="/" className="js-nav-logo">
          ResumeScan
        </Link>

        {/* Navigation Menu */}
        <ul className="js-nav-menu">
          {links.map((link) => (
            <li key={link.name}>
              <Link
                to={link.path}
                className={location.pathname === link.path ? 'text-blue-600' : ''}
              >
                {link.name}
              </Link>
            </li>
          ))}
          <li>
            <Link to="/scan" className="js-nav-cta">
              Scan Resume
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}