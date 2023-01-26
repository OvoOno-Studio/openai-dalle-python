(function() {
    console.log('Logging... Welcome.');
    console.log('Form ID: ' + form);
    console.log('Endpoint: ' + endpoint);
    console.log('Type: ' + type);
 
    function onSubmit(){  
         event.preventDefault();
         // Execute the reCAPTCHA verification
         grecaptcha.ready(function() {
             grecaptcha.execute('6LdeTdAjAAAAAPGWzX9fKu4lUXMeef2zaAhs-nXy', { action: 'submit' }).then(function(token) {
                 // Add the reCAPTCHA token to the request header
                 const f = document.getElementById(form);
                 const csrf_token = document.getElementsByName("csrf_token")[0].value;

                 form === 'generate-form' && endpoint === '/generate' ? data = f.elements['text'].value : data = f.elements['photo'].files[0]; 

 
                 const imageContainer = document.getElementById('image-container');
                 const linkContainer = document.getElementById('link-container'); 
                 // Show loader on submiting form
                 document.getElementById('loader').style.display = 'block';
                 // Disable submit button of form while fetching
                 document.getElementById('g-recaptcha-button').disabled = true;
                 // Remove all child nodes of the image container
                 if (imageContainer.firstChild) {
                     while (imageContainer.firstChild) {
                         imageContainer.removeChild(imageContainer.firstChild);
                     }
                 }
 
                 if (linkContainer.firstChild) {
                     while (linkContainer.firstChild) {
                         linkContainer.removeChild(linkContainer.firstChild);
                     }
                 }

                 
                if (endpoint === '/image-variations') {
                    imageBlob = new Blob([data], {type: 'application/json'});
                    formData = new FormData(); 
                    request = new XMLHttpRequest(); 
                    formData.append('blob', imageBlob);
                    request.open(
                                "POST",
                                endpoint,
                                true
                            );
                    request.send(form);
                    console.log('sent');
                    return;
                }
 
                 fetch(endpoint, {
                     method: 'POST',
                     headers: {
                         'Content-Type': type, // text-plain
                         'x-recaptcha-token': token,
                         'x-csrf-token': csrf_token
                     },
                     body: data,
                 })
                 .then(response => {
                     if (!response.ok) {
                         throw new Error(`Request failed with status code: ${response.status}`);
                     }
 
                     return response.json();
                 })
                 .then(data => {
                     // Creating new elements for link and generated image
                     const image = document.createElement('img');
                     const url = document.createElement('a');
                     image.src = data.url;
                     url.href = data.url;
                     url.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24"><path d="M5,20H19V18H5M19,9H15V3H9V9H5L12,16L19,9Z" /></svg><span> Download Image </span>';
                     url.target = '_blank';
                     imageContainer.appendChild(image);
                     linkContainer.appendChild(url);
                     // Hide loader on image loading
                     document.getElementById('loader').style.display = 'none';
                     // Enable submit form button
                     document.getElementById('g-recaptcha-button').disabled = false;
                 })
                 .catch(error => {
                     console.error(error);
                     document.getElementById('loader').style.display = 'none';
                 });
             });
         }); 
     };
 
     window.onSubmit = onSubmit;
 }).call(this);
 
 