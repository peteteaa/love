document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const promptInput = document.getElementById('prompt');
    const recipientInput = document.getElementById('recipient');
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');
    const generatedImage = document.getElementById('generatedImage');
    const downloadBtn = document.getElementById('downloadBtn');

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        const recipient = recipientInput.value.trim();
        
        if (!prompt) {
            alert('Please enter a celebrity name');
            return;
        }

        if (!recipient) {
            alert('Please enter a recipient name');
            return;
        }

        // Show loading state
        statusDiv.classList.remove('hidden');
        resultDiv.classList.add('hidden');
        generateBtn.disabled = true;
        generateBtn.classList.add('opacity-50');

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    prompt: prompt + " holding a Happy Valentine's Day sign in a collage",
                    recipient: recipient
                })
            });

            if (!response.ok) {
                throw new Error('Failed to generate image');
            }

            // Get the image blob
            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);
            
            // Display the generated image
            generatedImage.src = imageUrl;
            downloadBtn.href = imageUrl;
            downloadBtn.download = `valentine-for-${recipient}.jpg`;
            
            // Prevent image from opening in new tab when loaded
            generatedImage.addEventListener('load', (e) => {
                e.preventDefault();
            });
            
            // Show the result
            resultDiv.classList.remove('hidden');
        } catch (error) {
            alert('Error generating image: ' + error.message);
        } finally {
            // Hide loading state
            statusDiv.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.classList.remove('opacity-50');
        }
    });

    // Show image once it's loaded
    generatedImage.addEventListener('load', () => {
        generatedImage.classList.remove('opacity-0');
    });
});
