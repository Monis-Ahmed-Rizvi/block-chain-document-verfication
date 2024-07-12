# Blockchain-based Document Verification System

This project implements a secure and scalable document verification system using blockchain technology. It allows users to upload documents, store their hashes on the blockchain, and later verify the authenticity of these documents.

## Features

- User authentication with email verification
- Secure document upload and storage
- Blockchain-based document verification
- RESTful API for easy integration

## Technologies Used

- Backend: Python, Flask
- Database: SQLite (PostgreSQL for production)
- Blockchain: Ethereum (local chain with Ganache for development)
- Authentication: JWT (JSON Web Tokens)
- Email: Flask-Mail

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/blockchain-doc-verify.git
   cd blockchain-doc-verify
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following:
   ```
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret
   MAIL_SERVER=smtp.googlemail.com
   MAIL_PORT=587
   MAIL_USE_TLS=1
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   ```

5. Initialize the database:
   ```
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

## API Endpoints

- POST /api/register - Register a new user
- POST /api/login - Login and receive an access token
- POST /api/upload - Upload a document (protected)
- GET /api/documents - Get user's documents (protected)
- GET /api/verify/<document_id> - Verify a document (protected)

## Future Improvements

- Integration with Ethereum mainnet
- Frontend development with React
- Enhanced security features (2FA, CSRF protection)
- Performance optimization with caching
- Comprehensive test suite
- CI/CD pipeline

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.