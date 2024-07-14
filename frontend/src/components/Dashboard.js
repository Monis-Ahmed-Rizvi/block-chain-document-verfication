import React, { useState, useEffect } from 'react';
import { Container, Typography, Button, List, ListItem, ListItemText, CircularProgress, Snackbar, AppBar, Toolbar } from '@mui/material';
import { getDocuments, uploadDocument, verifyDocument } from '../services/api';
import { useNavigate } from 'react-router-dom';

const Dashboard = ({ setToken }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await getDocuments();
      setDocuments(response.data.documents);
    } catch (error) {
      setError('Failed to load documents. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    try {
      setUploading(true);
      await uploadDocument(file);
      setSuccess('Document uploaded successfully');
      fetchDocuments();
    } catch (error) {
      setError('Failed to upload document. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleVerify = async (documentId) => {
    try {
      const response = await verifyDocument(documentId);
      setSuccess(`Document verified: ${response.data.is_valid_blockchain ? 'Valid' : 'Invalid'}`);
    } catch (error) {
      setError('Failed to verify document. Please try again.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    navigate('/login');
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>Dashboard</Typography>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Container style={{ marginTop: '2rem' }}>
        {loading ? (
          <CircularProgress />
        ) : (
          <>
            <input
              accept="*/*"
              style={{ display: 'none' }}
              id="raised-button-file"
              type="file"
              onChange={handleUpload}
              disabled={uploading}
            />
            <label htmlFor="raised-button-file">
              <Button variant="contained" component="span" disabled={uploading}>
                {uploading ? 'Uploading...' : 'Upload Document'}
              </Button>
            </label>
            <List>
              {documents.map((document) => (
                <ListItem key={document.id}>
                  <ListItemText 
                    primary={document.filename}
                    secondary={`Uploaded: ${new Date(document.timestamp).toLocaleString()}`}
                  />
                  <Button onClick={() => handleVerify(document.id)}>Verify</Button>
                </ListItem>
              ))}
            </List>
          </>
        )}
        <Snackbar
          open={!!error || !!success}
          autoHideDuration={6000}
          onClose={() => { setError(''); setSuccess(''); }}
          message={error || success}
        />
      </Container>
    </>
  );
};

export default Dashboard;