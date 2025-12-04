# DevNotebook

## Overview

DevNotebook is a productivity-focused web application designed to help developers plan, organize, and track their project ideas, plans, and tasks before diving into code. The application follows a clean, modern interface inspired by Linear and Notion, emphasizing clarity and efficiency in information presentation.

The system is built as a Flask web application with user authentication, providing personalized dashboards where developers can manage their ideas, active projects, and pending tasks. The application features a responsive design with dark mode support and uses Tailwind CSS for styling.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**UI Framework**: The application uses Tailwind CSS for styling with a custom design system based on Material Design principles. The interface features:
- Responsive, mobile-first layout with a fixed sidebar (250px) on desktop that collapses on mobile
- Dark mode support with theme persistence using localStorage
- System font stack for native feel and performance
- Card-based component system for content organization

**Template Structure**: Jinja2 templates with a base layout pattern:
- `base.html`: Main layout with sidebar navigation and content wrapper
- `landing.html`: Public-facing homepage for unauthenticated users
- `login.html` and `register.html`: Authentication pages
- `dashboard.html`: User dashboard showing stats and activity
- `index.html`: Alternative dashboard view

**Client-Side Features**:
- Theme toggle between light/dark modes with system preference detection
- Sidebar toggle for mobile responsiveness
- CSRF protection for all forms

### Backend Architecture

**Framework**: Flask (Python web framework) with the following structure:
- Single monolithic application file (`main.py`)
- SQLAlchemy ORM for database operations
- Flask-Login for session management and authentication
- Flask-WTF for CSRF protection

**Authentication System**:
- Username/email-based registration and login
- Password hashing using Werkzeug security utilities
- Session-based authentication with Flask-Login
- Safe URL redirection validation to prevent open redirect vulnerabilities
- Login required decorator for protected routes

**Application Configuration**:
- Environment-based configuration using `SECRET_KEY` and `SESSION_SECRET` for session security
- Database URL configured via `DATABASE_URL` environment variable
- SQLAlchemy track modifications disabled for performance

### Data Storage

**ORM**: SQLAlchemy with Flask-SQLAlchemy integration

**Database Schema**:

**Users Table**:
- `id`: Integer primary key
- `username`: Unique string (max 80 chars)
- `email`: Unique string (max 120 chars)
- `password_hash`: Hashed password string (max 256 chars)
- `created_at`: Timestamp with UTC default

The database connection is configured to work with PostgreSQL (via `DATABASE_URL` environment variable), though the ORM is database-agnostic and could work with other SQL databases.

**Design Rationale**: The current schema is minimal, focusing only on user authentication. The application appears to be in early development stages, with placeholder statistics in the dashboard suggesting that additional tables for ideas, projects, and tasks are planned but not yet implemented.

### Security Considerations

**CSRF Protection**: Flask-WTF CSRF tokens required for all form submissions

**Password Security**: Werkzeug's `generate_password_hash` and `check_password_hash` for secure password storage

**Session Security**: Secret key-based session encryption

**URL Validation**: Custom `is_safe_url` function prevents open redirect vulnerabilities by validating redirect targets against the application's host

## External Dependencies

### Python Libraries
- **Flask**: Core web framework
- **Flask-SQLAlchemy**: ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **Werkzeug**: Password hashing utilities

### Frontend Libraries
- **Tailwind CSS**: Loaded via CDN for utility-first styling
- **Custom CSS**: Minimal custom styles in `static/css/style.css` for:
  - Scrollbar styling (light/dark variants)
  - Card component base styles
  - CSS variables for transitions

### JavaScript
- **Vanilla JavaScript**: Client-side functionality in `static/js/script.js` for:
  - Theme toggle functionality
  - Sidebar mobile menu
  - LocalStorage for theme persistence

### Database
- **PostgreSQL**: Primary database (configured via `DATABASE_URL` environment variable)
- Connection managed through SQLAlchemy ORM

### Environment Variables Required
- `SECRET_KEY` or `SESSION_SECRET`: Flask session encryption
- `DATABASE_URL`: PostgreSQL connection string

### Design Assets
- **SVG Icons**: Inline SVG icons throughout the interface (no icon library dependency)
- **System Fonts**: No web fonts, uses native system font stack for performance