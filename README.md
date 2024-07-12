# Blockchain-based Document Verification System

This project implements a secure and scalable document verification system using blockchain technology. It allows users to upload documents, store their hashes on the blockchain, and later verify the authenticity of these documents.

## Features

- User authentication with email verification
- Secure document upload and storage
- Blockchain-based document verification
- RESTful API for easy integration
- Local and blockchain-based integrity checks

## Technologies Used

- Backend: Python, Flask
- Database: SQLite (can be easily switched to PostgreSQL for production)
- Blockchain: Ethereum (local chain with Ganache for development)
- Smart Contract: Solidity
- Authentication: JWT (JSON Web Tokens)
- Email: Flask-Mail

## Prerequisites

- Python 3.8+
- Node.js and npm (for Truffle and Ganache)
- Ganache (for local blockchain)
- Truffle

## Setup and Installation

1. Clone the repository:
   ```
   https://github.com/Monis-Ahmed-Rizvi/block-chain-document-verfication
   cd blockchain_doc_verify
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the backend directory with the following content:
   ```
   SECRET_KEY=your_secret_key
   JWT_SECRET_KEY=your_jwt_secret
   MAIL_SERVER=smtp.googlemail.com
   MAIL_PORT=587
   MAIL_USE_TLS=1
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_email_password
   CONTRACT_ADDRESS=your_deployed_contract_address
   ```

4. Set up and deploy the smart contract:
   ```
   cd ../blockchain
   npm install -g truffle
   truffle compile
   truffle migrate
   ```
   Note the contract address after migration and update it in the `.env` file.

5. Initialize the database:
   ```
   cd ../backend
   flask db upgrade
   ```

6. Run the application:
   ```
   flask run
   ```

## API Endpoints

- POST /api/register - Register a new user
- GET /api/verify-email/<token> - Verify user's email
- POST /api/login - Login and receive an access token
- POST /api/upload - Upload a document (protected)
- GET /api/documents - Get user's documents (protected)
- GET /api/verify/<document_id> - Verify a document (protected)

## Testing

To run tests:
```
python -m unittest discover tests
```

## Deployment

For production deployment, consider the following:
- Use a production-grade server like Gunicorn
- Set up a reverse proxy with Nginx
- Use PostgreSQL instead of SQLite
- Deploy smart contracts to a live Ethereum network

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.