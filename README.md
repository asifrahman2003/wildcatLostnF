# Wildcat Lost & Found

A smart lost-and-found web application for the University of Arizona campus that uses NLP to process natural language input and suggest the best locations to recover lost items.

## Features

- Natural language processing to extract lost items from user input
- Campus area-based location matching
- Modern, responsive UI with Tailwind CSS
- Deployed on Google Cloud Platform

## Project Structure

```
wildcat-lost-found/
├── backend/
│   ├── app.py         # GCP Cloud Function code
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html         # Main HTML file
│   ├── style.css         # Custom styles
│   ├── script.js         # Frontend logic
│   └── config.js         # Configuration file
└── README.md
```

## Setup & Deployment

### Backend (GCP Cloud Function)

1. Install Google Cloud SDK and initialize:
   ```bash
   gcloud init
   ```

2. Deploy the Cloud Function:
   ```bash
   cd backend
   gcloud functions deploy lost-found \
       --runtime python39 \
       --trigger-http \
       --allow-unauthenticated \
       --memory 1024MB \
       --region REGION
   ```

3. Note the Function URL provided in the deployment output.

### Frontend Deployment (GCP Cloud Storage)

1. Create a Cloud Storage bucket:
   ```bash
   gsutil mb gs://BUCKET_NAME
   ```

2. Make the bucket public:
   ```bash
   gsutil iam ch allUsers:objectViewer gs://BUCKET_NAME
   ```

3. Enable website hosting:
   ```bash
   gsutil web set -m index.html gs://BUCKET_NAME
   ```

4. Update the API endpoint in `frontend/config.js` with your Cloud Function URL.

5. Upload frontend files:
   ```bash
   cd frontend
   gsutil cp -r * gs://BUCKET_NAME
   ```

## Local Development

### Backend

1. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Run locally:
   ```bash
   python app.py
   ```

### Frontend

1. Serve the frontend directory using Python's built-in server:
   ```bash
   cd frontend
   python3 -m http.server 8000
   ```

2. Open http://localhost:8000 in browser.

## Configuration

### Backend Configuration

- The backend uses DistilBERT for NLP processing
- Memory allocation: 1024MB (configured during deployment)
- Timeout: 60 seconds (default)

### Frontend Configuration

Edit `frontend/config.js` to modify:
- API endpoint URL
- Maximum input length
- Available campus areas
- Request timeout

## Security Considerations

- CORS is enabled for the Cloud Function
- Frontend is served over HTTPS via Cloud Storage
- Input validation is implemented on both frontend and backend

## Error Handling

The application includes comprehensive error handling:
- Network request failures
- Invalid user input
- NLP processing errors
- Server-side errors

## Future Enhancements

Potential improvements:
- User authentication
- Search history
- Real-time location updates
- Integration with UArizona's official lost-and-found system
- Mobile app version

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
