document.addEventListener("DOMContentLoaded", function() {
    // DOM Elements
    const form = document.getElementById("postForm");
    const hotelInput = document.getElementById("hotel_name");
    const occasionInput = document.getElementById("occasion");
    const loadingElement = document.getElementById("loading");
    const errorElement = document.getElementById("errorMessage");
    const captionElement = document.getElementById("caption");
    const imageElement = document.getElementById("generatedImage");
    const resultContainer = document.getElementById("result");
    const socialShareSection = document.getElementById("socialShare");
    const shareInstagram = document.getElementById("shareInstagram");
    const shareFacebook = document.getElementById("shareFacebook");
    const shareTwitter = document.getElementById("shareTwitter");
    const shareLinkedIn = document.getElementById("shareLinkedIn");
    const editSection = document.getElementById("editSection");
    const additionalPrompt = document.getElementById("additionalPrompt");
    const regenerateBtn = document.getElementById("regenerateBtn");
    const useOriginalBtn = document.getElementById("useOriginalBtn");

    let originalImageUrl = '';

    // Reset functionality
    document.getElementById("resetBtn").addEventListener("click", function() {
        form.reset();
        captionElement.innerHTML = '';
        imageElement.src = '';
        imageElement.style.display = 'none';
        errorElement.style.display = 'none';
        socialShareSection.classList.add('hidden');
        editSection.classList.add('hidden');
        additionalPrompt.value = '';
    });

    // Form submission handler
    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        const hotelName = hotelInput.value.trim();
        const occasion = occasionInput.value.trim();

        if (!hotelName || !occasion) {
            showError("Please enter both hotel name and occasion!");
            return;
        }

        loadingElement.style.display = 'block';
        errorElement.style.display = 'none';
        imageElement.style.display = 'none';
        captionElement.innerHTML = '';
        socialShareSection.classList.add('hidden');
        editSection.classList.add('hidden');

        try {
            const response = await fetch("/generate/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    hotel_name: hotelName,
                    occasion: occasion
                })
            });

            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data);

            if (data.error) {
                throw new Error(data.error);
            }

            // Display caption
            captionElement.innerHTML = data.caption || "No caption generated";

            // Handle image display
            if (data.imageURL) {
                console.log("Raw imageURL from server:", data.imageURL);
                
                const normalizedUrl = data.imageURL.replace(/\\/g, '/');
                const fullImageUrl = normalizedUrl.startsWith('http') 
                    ? normalizedUrl 
                    : `${window.location.origin}${normalizedUrl}`;
                
                console.log("Corrected image URL:", fullImageUrl);

                const newImg = new Image();
                newImg.onload = function() {
                    console.log("Image loaded successfully");
                    imageElement.src = this.src;
                    imageElement.style.display = 'block';
                    
                    // Store the original image URL
                    originalImageUrl = this.src;
                    
                    // Show the edit section
                    editSection.classList.remove('hidden');
                    
                    // Set up social sharing
                    setupSocialSharing(data.caption, this.src);
                };
                
                newImg.onerror = function() {
                    console.error("Failed to load image");
                    const errorMsg = document.createElement('p');
                    errorMsg.textContent = '⚠️ Could not load generated image';
                    errorMsg.style.color = 'red';
                    resultContainer.appendChild(errorMsg);
                };
                
                newImg.src = `${fullImageUrl}?t=${Date.now()}`;
                newImg.alt = `${hotelName} ${occasion} celebration`;
            } else {
                console.log("No image URL in response");
                const noImageMsg = document.createElement('p');
                noImageMsg.textContent = 'No image was generated';
                noImageMsg.style.color = '#666';
                resultContainer.appendChild(noImageMsg);
            }

        } catch (error) {
            console.error("Error:", error);
            showError(error.message);
        } finally {
            loadingElement.style.display = 'none';
        }
    });

    // Regenerate image handler
    regenerateBtn.addEventListener('click', async function() {
        const prompt = additionalPrompt.value.trim();
        if (!prompt) {
            showError("Please enter some additional details for the image");
            return;
        }

        const hotelName = hotelInput.value.trim();
        const occasion = occasionInput.value.trim();

        loadingElement.style.display = 'block';
        editSection.style.opacity = '0.5';
        regenerateBtn.disabled = true;

        try {
            const response = await fetch("/regenerate-image/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    hotel_name: hotelName,
                    occasion: occasion,
                    additional_prompt: prompt
                })
            });

            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }

            const data = await response.json();
            console.log("Regeneration Response:", data);

            if (data.error) {
                throw new Error(data.error);
            }

            if (data.imageURL) {
                const normalizedUrl = data.imageURL.replace(/\\/g, '/');
                const fullImageUrl = normalizedUrl.startsWith('http') 
                    ? normalizedUrl 
                    : `${window.location.origin}${normalizedUrl}`;

                const newImg = new Image();
                newImg.onload = function() {
                    imageElement.src = this.src;
                    setupSocialSharing(captionElement.textContent, this.src);
                    editSection.style.opacity = '1';
                    regenerateBtn.disabled = false;
                };
                newImg.onerror = function() {
                    console.error("Failed to load regenerated image");
                    showError("Failed to load regenerated image");
                    editSection.style.opacity = '1';
                    regenerateBtn.disabled = false;
                };
                newImg.src = `${fullImageUrl}?t=${Date.now()}`;
            }

        } catch (error) {
            console.error("Regeneration Error:", error);
            showError(error.message);
            editSection.style.opacity = '1';
            regenerateBtn.disabled = false;
        } finally {
            loadingElement.style.display = 'none';
        }
    });

    // Use original image handler
    useOriginalBtn.addEventListener('click', function() {
        if (originalImageUrl) {
            imageElement.src = originalImageUrl;
            setupSocialSharing(captionElement.textContent, originalImageUrl);
        }
        additionalPrompt.value = '';
    });

    // Helper function to display errors
    function showError(message) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    // Social Media Sharing Setup
    function setupSocialSharing(caption, imageUrl) {
        socialShareSection.classList.remove('hidden');
        
        const encodedCaption = encodeURIComponent(caption);
        const encodedImageUrl = encodeURIComponent(imageUrl);
        const encodedCombined = encodeURIComponent(`${caption}\n\n${imageUrl}`);
        
        shareInstagram.href = `https://www.instagram.com/create/story?backgroundImage=${encodedImageUrl}`;
        shareFacebook.href = `https://www.facebook.com/sharer/sharer.php?u=${encodedImageUrl}&quote=${encodedCaption}`;
        shareTwitter.href = `https://twitter.com/intent/tweet?text=${encodedCombined}`;
        shareLinkedIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedImageUrl}`;
        
        [shareInstagram, shareFacebook, shareTwitter, shareLinkedIn].forEach(btn => {
            btn.addEventListener('click', function() {
                console.log(`Sharing to ${this.textContent.trim()}`);
            });
        });
    }
});