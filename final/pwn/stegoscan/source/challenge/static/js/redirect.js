// Get the response parameter from the URL
const urlParams = new URLSearchParams(window.location.search);
const response = urlParams.get('response');

// Display the response in the HTML
const responseElement = document.getElementById('response');
responseElement.textContent = response;
