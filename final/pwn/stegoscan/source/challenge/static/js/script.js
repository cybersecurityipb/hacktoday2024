function showerror(text) {
  document.getElementById('error').innerHTML = text;
  document.getElementById('error').style.display = 'block';
  
  setInterval(function(){
    document.getElementById('error').style.display = 'none';

  }, 5000)

}
function initImageUpload() {
  let uploadField = document.getElementById('file-input');

  uploadField.addEventListener('change', getFile);

  function getFile(e){
    let file = e.currentTarget.files[0];
    checkType(file);
  }

  function checkType(file){
    let imageType = /image.bmp/;
    if (!file.type.match(imageType)) {
      showerror('File is not a bitmap!');
    } 
    else if (!file) {
      showerror('No image selected');
    } 
    else {
      const endpoint = '/stegoscan';

      const formData = new FormData();
      formData.append('file', file);

      fetch(endpoint, {
        method: 'POST',
        body: formData
      })
        .then(response => response.text())
        .then(data => {
          const redirectURL = `results?response=${encodeURIComponent(data)}`;
          window.location.href = redirectURL;
        })
        .catch(error => {
          console.error('Error uploading file:', error);
          alert('An error occurred while uploading the file.');
      });
    }
  }
}

initImageUpload();