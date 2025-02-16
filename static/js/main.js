document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generateBtn');
    const promptInput = document.getElementById('prompt');
    const statusDiv = document.getElementById('status');
    const resultDiv = document.getElementById('result');
    const generatedImage = document.getElementById('generatedImage');
    const downloadBtn = document.getElementById('downloadBtn');

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert('Please enter a prompt');
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
                body: JSON.stringify({ prompt: prompt + " holding a Happy Valentine's Day sign in a collage" })
            });

            if (!response.ok) {
                throw new Error('Failed to generate image');
            }

            const data = await response.json();
            
            // Display the generated image
            generatedImage.src = data.image_url;
            downloadBtn.href = data.image_url;
            
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
