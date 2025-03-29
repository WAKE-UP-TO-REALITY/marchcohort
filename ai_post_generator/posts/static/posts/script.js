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

    // Reset functionality
    document.getElementById("resetBtn").addEventListener("click", function() {
        form.reset();
        captionElement.innerHTML = '';
        imageElement.src = '';
        imageElement.style.display = 'none';
        errorElement.style.display = 'none';
        socialShareSection.classList.add('hidden');
    });

    // Form submission handler
    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        // Get and validate inputs
        const hotelName = hotelInput.value.trim();
        const occasion = occasionInput.value.trim();

        if (!hotelName || !occasion) {
            showError("Please enter both hotel name and occasion!");
            return;
        }

        // UI Loading state
        loadingElement.style.display = 'block';
        errorElement.style.display = 'none';
        imageElement.style.display = 'none';
        captionElement.innerHTML = '';
        socialShareSection.classList.add('hidden');

        try {
            // API Request
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

            // Handle response
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
                
                // Normalize path (fix Windows backslashes)
                const normalizedUrl = data.imageURL.replace(/\\/g, '/');
                
                // Construct full URL
                const fullImageUrl = normalizedUrl.startsWith('http') 
                    ? normalizedUrl 
                    : `${window.location.origin}${normalizedUrl}`;
                
                console.log("Corrected image URL:", fullImageUrl);

                // Create new image element for reliable loading
                const newImg = new Image();
                newImg.onload = function() {
                    console.log("Image loaded successfully");
                    imageElement.src = this.src;
                    imageElement.style.display = 'block';
                    
                    // Set up social sharing
                    setupSocialSharing(data.caption, fullImageUrl);
                };
                
                newImg.onerror = function() {
                    console.error("Failed to load image");
                    const errorMsg = document.createElement('p');
                    errorMsg.textContent = '⚠️ Could not load generated image';
                    errorMsg.style.color = 'red';
                    resultContainer.appendChild(errorMsg);
                };
                
                // Load with cache busting
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

    // Helper function to display errors
    function showError(message) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }

    // Social Media Sharing Setup
    function setupSocialSharing(caption, imageUrl) {
        // Show the social sharing section
        socialShareSection.classList.remove('hidden');
        
        // Encode content for URLs
        const encodedCaption = encodeURIComponent(caption);
        const encodedImageUrl = encodeURIComponent(imageUrl);
        const encodedCombined = encodeURIComponent(`${caption}\n\n${imageUrl}`);
        
        // Instagram (Story only - feed posts require manual upload)
        shareInstagram.href = `https://www.instagram.com/create/story?backgroundImage=${encodedImageUrl}`;
        
        // Facebook
        shareFacebook.href = `https://www.facebook.com/sharer/sharer.php?u=${encodedImageUrl}&quote=${encodedCaption}`;
        
        // Twitter
        shareTwitter.href = `https://twitter.com/intent/tweet?text=${encodedCombined}`;
        
        // LinkedIn
        shareLinkedIn.href = `https://www.linkedin.com/sharing/share-offsite/?url=${encodedImageUrl}`;
        
        // Add click handlers to track shares (optional)
        [shareInstagram, shareFacebook, shareTwitter, shareLinkedIn].forEach(btn => {
            btn.addEventListener('click', function() {
                console.log(`Sharing to ${this.textContent.trim()}`);
                // Here you could add analytics tracking
            });
        });
    }

    // Download image functionality
    document.getElementById('downloadBtn')?.addEventListener('click', function() {
        if (imageElement.src) {
            const a = document.createElement('a');
            a.href = imageElement.src;
            a.download = `hotel-post-${Date.now()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    });

    // Copy text to clipboard
    document.getElementById('copyBtn')?.addEventListener('click', function() {
        const textToCopy = `${captionElement.textContent}`;
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                const originalText = this.textContent;
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = originalText;
                }, 2000);
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                showError('Failed to copy text to clipboard');
            });
    });
});