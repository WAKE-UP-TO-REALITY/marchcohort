document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("postForm");
    const hotelNameInput = document.getElementById("hotel_name");
    const occasionInput = document.getElementById("occasion");
    const resultContainer = document.getElementById("result");
    const imageElement = document.getElementById("generatedImage");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();
        
        const hotelName = hotelNameInput.value.trim();
        const occasion = occasionInput.value.trim();

        if (!hotelName || !occasion) {
            alert("Please enter both hotel name and occasion!");
            return;
        }

        resultContainer.innerHTML = "Generating post...";
        imageElement.style.display = "none"; // Hide image initially

        try {
            const response = await fetch("/generate/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ hotel_name: hotelName, occasion: occasion }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Response from server:", data);

            if (data.error) {
                resultContainer.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            } else {
                resultContainer.innerHTML = `<p><strong>Generated Caption:</strong> ${data.caption}</p>`;
                if (data.imageURL) {
                    const fullImagePath = window.location.origin + data.imageURL; // Ensure full URL
                    imageElement.src = fullImagePath;
                    imageElement.style.display = "block";
                } else {
                    imageElement.style.display = "none";
                }
                
            }
        } catch (error) {
            console.error("Error fetching data:", error);
            resultContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    });
});
