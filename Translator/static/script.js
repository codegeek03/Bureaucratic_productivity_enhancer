// Inside your translateText() function in index.html
async function translate() {
    const englishText = document.getElementById('englishText').value;
    const status = document.getElementById('status');
    const translateBtn = document.getElementById('translateBtn');

    if (!englishText) {
        showStatus('Please enter text to translate', 'error');
        return;
    }

    try {
        translateBtn.disabled = true;
        showStatus('Translating...', 'info');

        const response = await fetch('/translate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: englishText,
                source_lang: "English",
                target_lang: "Hindi",
                country: "India"
            })
        });

        const data = await response.json();
        if (response.ok) {
            document.getElementById('hindiText').value = data.translated_text;
            showStatus('Translation completed successfully!', 'success');
        } else {
            throw new Error(data.detail || 'Translation failed');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        translateBtn.disabled = false;
    }
}