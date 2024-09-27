// Function to generate a random key (dummy implementation)
function generateRandomKey() {
  return (
    Math.random().toString(36).substring(2, 15) +
    Math.random().toString(36).substring(2, 15)
  );
}

module.exports = generateRandomKey;
