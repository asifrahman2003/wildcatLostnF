document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    const resultsSection = document.getElementById('results');
    const locationsList = document.getElementById('locationsList');
    const loadingSpinner = document.getElementById('loading');

    // Initialize the results section as hidden
    resultsSection.classList.add('hidden');

    // Handle form submission
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const itemDescription = document.getElementById('itemDescription').value.trim();
        const location = document.getElementById('location').value;

        if (!itemDescription || !location) {
            alert('Please fill in both fields before searching.');
            return;
        }

        try {
            // Show loading spinner and hide results
            loadingSpinner.classList.remove('hidden');
            resultsSection.classList.add('hidden');
            locationsList.innerHTML = '';

            // Make API request
            const response = await fetch(`http://localhost:8000/lost-found?item=${encodeURIComponent(itemDescription)}&area=${encodeURIComponent(location)}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            const data = await response.json();
            console.log('API Response:', data);

            // Hide loading spinner
            loadingSpinner.classList.add('hidden');

            // Show results section
            resultsSection.classList.remove('hidden');

            // Clear previous results
            locationsList.innerHTML = '';

            if (Array.isArray(data) && data.length > 0) {
                // Create and append location cards
                data.forEach(location => {
                    const locationCard = document.createElement('div');
                    locationCard.className = 'bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow duration-200 mb-4';
                    locationCard.innerHTML = `
                        <div class="flex items-start justify-between">
                            <div class="flex-grow">
                                <h4 class="text-lg font-semibold text-gray-800">${location.name}</h4>
                                <p class="text-gray-600 mt-1">
                                    <i class="fas fa-map-marker-alt text-[#AB0520] mr-2"></i>
                                    ${location.area}
                                </p>
                                ${location.note ? `
                                    <p class="text-sm text-gray-500 mt-2">
                                        <i class="fas fa-info-circle mr-1"></i>
                                        ${location.note}
                                    </p>
                                ` : ''}
                            </div>
                            <a href="${location.link}" 
                               target="_blank" 
                               rel="noopener noreferrer"
                               class="flex items-center text-[#AB0520] hover:text-[#8C0420] transition-colors duration-200 ml-4">
                                <span class="text-sm mr-1">Details</span>
                                <i class="fas fa-external-link-alt text-sm"></i>
                            </a>
                        </div>
                    `;
                    locationsList.appendChild(locationCard);
                });
            } else {
                // Show no results message
                locationsList.innerHTML = `
                    <div class="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                        <p class="text-yellow-700">
                            <i class="fas fa-exclamation-triangle mr-2"></i>
                            No specific locations found. Please try a different description or check with UAPD Lost & Found.
                        </p>
                    </div>
                `;
            }

        } catch (error) {
            console.error('Error:', error);
            loadingSpinner.classList.add('hidden');
            resultsSection.classList.remove('hidden');
            locationsList.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-md p-4">
                    <p class="text-red-700">
                        <i class="fas fa-exclamation-circle mr-2"></i>
                        An error occurred while searching. Please try again later.
                    </p>
                </div>
            `;
        }
    });

    // Handle location dropdown
    const locationSelect = document.getElementById('location');
    locationSelect.addEventListener('change', () => {
        if (locationSelect.value) {
            locationSelect.classList.add('text-gray-900');
        } else {
            locationSelect.classList.remove('text-gray-900');
        }
    });
});