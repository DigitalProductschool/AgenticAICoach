// Attach event listener to the form submission
document.getElementById('upload-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('cv-file'); // File input element
    const jdInput = document.getElementById('job-description'); // Job description input
    const analyzeButton = document.querySelector('button[type="submit"]'); // Submit button
    const analyzingContainer = document.getElementById('analyzing-container'); // Analyzing overlay
    const resultModal = document.getElementById('result-modal'); // Result modal

    // Validate if a CV file is selected
    if (!fileInput.files[0]) {
        alert('Please select a CV file before submitting.');
        return;
    }

    // Show the analyzing overlay
    analyzingContainer.style.display = 'flex';

    const formData = new FormData();
    formData.append('cv_file', fileInput.files[0]); // Append the CV file
    formData.append('job_description', jdInput.value); // Append job description

    analyzeButton.disabled = true; // Disable the analyze button during processing

    try {
        // Send POST request to the analyze API endpoint
        const response = await fetch('/api/analyze/', {
            method: 'POST',
            body: formData,
        });

        // Handle non-OK responses
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to analyze the CV');
        }

        const data = await response.json(); // Parse JSON response

        // Hide the analyzing overlay
        analyzingContainer.style.display = 'none';

        // Display the result in a modal
        displayResultModal(data);
    } catch (error) {
        console.error(error); // Log error for debugging
        analyzingContainer.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    } finally {
        analyzeButton.disabled = false; // Re-enable the analyze button
    }
});

// Function to display the results in a modal
function displayResultModal(data) {
    const resultModal = document.getElementById('result-modal'); // Modal container
    const closeModalButton = document.createElement('button'); // Create close button
    closeModalButton.textContent = 'Close'; // Set button text
    closeModalButton.className = 'close-btn'; // Apply close button styles
    closeModalButton.onclick = () => {
        resultModal.style.display = 'none'; // Hide modal on click
    };

    if (data.status === 'success') {
        const markdownContent = marked.parse(data.result); // Parse markdown content
        const reportHTML = `
            <h3>Analysis Complete</h3>
            <div class="markdown-content">${markdownContent}</div>
            <p>Download your reports:</p>
            <ul>
                <li><a href="/api/structure" download="structure.md">Structure Report</a></li>
                <li><a href="/api/relevance" download="relevance.md">Relevance Report</a></li>
                <li><a href="/api/language" download="language.md">Language Report</a></li>
                <li><a href="/api/power" download="power.md">Power Report</a></li>
                <li><a href="/api/report" download="full_report.md">Full Report</a></li>
            </ul>
        `;
        resultModal.innerHTML = reportHTML; // Insert report HTML into modal
    } else {
        resultModal.innerHTML = `<p style="color: red;">Error: ${data.message}</p>`; // Display error
    }

    resultModal.appendChild(closeModalButton); // Add close button to modal
    resultModal.style.display = 'block'; // Show the modal
}
