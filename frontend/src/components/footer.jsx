import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer className="js-footer">
      <div className="js-footer-container">
        {/* Main Footer Content */}
        <div className="js-footer-grid">
          {/* Product Links */}
          <div>
            <h4 className="js-footer-heading">Product</h4>
            <ul className="js-footer-links">
              <li><Link to="/scan">Resume Scanner</Link></li>
              <li><Link to="/job-matcher">Job Matcher</Link></li>
              <li><Link to="/resume-builder">Resume Builder</Link></li>
              <li><Link to="/cover-letters">Cover Letters</Link></li>
              <li><Link to="/pricing">Pricing</Link></li>
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h4 className="js-footer-heading">Resources</h4>
            <ul className="js-footer-links">
              <li><Link to="/blog">Blog</Link></li>
              <li><Link to="/career-advice">Career Advice</Link></li>
              <li><Link to="/resume-samples">Resume Samples</Link></li>
              <li><Link to="/ats-resume-check">ATS Resume Check</Link></li>
              <li><Link to="/help-center">Help Center</Link></li>
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h4 className="js-footer-heading">Company</h4>
            <ul className="js-footer-links">
              <li><Link to="/about">About Us</Link></li>
              <li><Link to="/press">Press</Link></li>
              <li><Link to="/careers">Careers</Link></li>
              <li><Link to="/contact">Contact</Link></li>
              <li><Link to="/legal">Legal</Link></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="js-footer-heading">Contact</h4>
            <ul className="js-footer-links">
              <li>support@resumescan.com</li>
              <li>+1 (555) 123-4567</li>
              <li>Mon-Fri 9AM-6PM EST</li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="js-footer-bottom">
          <div className="js-footer-logo">
            <Link to="/">ResumeScan</Link>
          </div>
          <div className="js-footer-copyright">
            © {new Date().getFullYear()} ResumeScan. All rights reserved.
          </div>
          <div className="js-footer-legal">
            <Link to="/privacy">Privacy Policy</Link>
            <Link to="/terms">Terms of Service</Link>
            <Link to="/cookies">Cookie Policy</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}