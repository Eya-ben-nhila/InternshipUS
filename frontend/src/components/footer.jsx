import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="js-footer">
      <div className="js-footer-container">
        <div className="js-footer-grid">
          {/* Product Links */}
          <div>
            <h4 className="js-footer-heading">Product</h4>
            <ul className="js-footer-links">
              <li><Link to="/">Home</Link></li>
              <li><Link to="/scan">Resume & Job Matcher</Link></li>
              <li><Link to="/profile">Profile</Link></li>
            </ul>
          </div>
          {/* Company Links */}
          <div>
            <h4 className="js-footer-heading">Company</h4>
            <ul className="js-footer-links">
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/contact">Contact</Link></li>
            </ul>
          </div>
          {/* Legal Links */}
          <div>
            <h4 className="js-footer-heading">Legal</h4>
            <ul className="js-footer-links">
              <li><Link to="/privacy">Privacy Policy</Link></li>
              <li><Link to="/terms">Terms of Service</Link></li>
              <li><Link to="/cookies">Cookie Policy</Link></li>
            </ul>
          </div>
        </div>
        <div className="js-footer-bottom">
          <div className="js-footer-logo">
            <Link to="/">ResumeScan</Link>
          </div>
          <div className="js-footer-copyright">
            © {new Date().getFullYear()} ResumeScan. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
}