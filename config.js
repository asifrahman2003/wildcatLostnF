// Configuration for the Wildcat Lost & Found application

// The API endpoint for the Cloud Function
// Replace this URL with your actual deployed Cloud Function URL
const API_ENDPOINT = 'https://REGION-PROJECT_ID.cloudfunctions.net/lost-found';

// Additional configuration options can be added here
const CONFIG = {
    // Maximum length for item description
    MAX_ITEM_LENGTH: 100,
    
    // Available campus areas
    CAMPUS_AREAS: [
        'Central Campus',
        'Library Area',
        'South Campus',
        'East Campus',
        'North Campus'
    ],
    
    // Default area
    DEFAULT_AREA: 'Central Campus',
    
    // API request timeout (in milliseconds)
    REQUEST_TIMEOUT: 10000
};