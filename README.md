## LIVrary : A Comprehensive Web App for Library Management

**Welcome to LIVrary, a feature-rich web application designed to streamline library operations and enhance the user experience for both patrons and administrators!**

**Key Features**

* **User Management:**

    * Users can request books from the admin (: mailto:[email address removed]).
    * Browse and read ebooks in PDF format from their bookshelf (with a maximum of 5 books at a time).  (: [invalid URL removed])
    * Maintain a bookshelf with a 7-day loan period. Requested books are automatically revoked after 7 days to maintain circulation. (: [invalid URL removed])
    * Search for books by title, author, or genre using a convenient search functionality. (: [invalid URL removed])
    * Keep track of favorite books for easy access. (: [invalid URL removed])
    * Add notes to books for personal reference. (: [invalid URL removed])
    * Choose a colorful avatar to personalize their experience. (: [invalid URL removed])
    * Receive email alerts if they don't log in daily to stay engaged (optional). (: [invalid URL removed])
    * Get a monthly report via email with a PDF attachment summarizing their library activity (books returned, issued, logged-in timestamps). (: mailto:[email address removed])

* **Admin Management:**

    * Create, Read, Update, and Delete (CRUD) functionalities for genres, books, user requests, and overdue books. (: [invalid URL removed])
    * Manage the library's collection efficiently.

* **Advanced Functionalities:**

    * **Asynchronous Tasks:** Leverage Celery and Redis for background tasks, ensuring a smooth user experience. (: [invalid URL removed])
    * **Email Notifications:** An integrated mail client sends automated email alerts and reports. (: [invalid URL removed])
    * **Customizable Reports:**  Generate PDF reports containing library activity details using PDFKit. (: [invalid URL removed])
    * **News Updates:** Stay informed! Access current news headlines in PDF format based on your region. News updates are refreshed asynchronously every three hours. (: [invalid URL removed])

**Technical Stack**

* Backend:
    * Flask RESTX  - API framework for robust backend development.
    * Swagger UI - User-friendly interface for API documentation.
    * SQLAlchemy - Powerful object-relational mapper (ORM) for database interactions.
    * Flask-Caching, Celery, Redis - Tools for efficient caching and asynchronous tasks.
    * Custom SMTP Server - Handles email communication.
    * JWT Tokens - Secure user authentication and authorization.
* Frontend:
    * Vue.js 2 - Modern JavaScript framework for a dynamic and interactive user interface.
    * Bootstrap - Popular CSS framework for responsive design.
    * Jinja2 - Template engine for server-side rendering.
    * Axios/Fetch - HTTP libraries for seamless communication between frontend and backend.
    * Matplotlib - Python library for data visualization (charts and analytics).
* Security:
    * HTTPS enforced using self-signed certificates for secure communication.

**Getting Started (For Developers)**

This section will be crucial for developers looking to deploy or contribute to the project.  I'd recommend adding detailed instructions on how to:

1.  Install Prerequisites
2.  Clone the repository
3.  Set up the development environment
4.  Run the application

**Conclusion**

LIVrary provides a comprehensive solution for managing libraries and enhancing the user experience. Its feature-rich design caters to both patrons and administrators, streamlining workflows and fostering a love for reading!
