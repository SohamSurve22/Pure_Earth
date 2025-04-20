// pureEarth - Pollution Monitoring Platform
// Image Upload Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize image upload functionality
    initImageUpload();
});

/**
 * Initialize image upload functionality with preview
 */
function initImageUpload() {
    const uploadForm = document.getElementById('image-form');
    const fileInput = document.getElementById('thermal-image');
    const previewContainer = document.getElementById('image-preview');
    
    if (!uploadForm || !fileInput) return;
    
    // Set up drag and drop zone
    const dropZone = document.querySelector('.upload-container');
    if (dropZone) {
        setupDragAndDrop(dropZone, fileInput);
    }
    
    // Add file input change listener
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            // Display file details
            displayFileDetails(file);
            
            // Show preview if possible
            if (previewContainer) {
                showImagePreview(file, previewContainer);
            }
        }
    });
    
    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        if (!fileInput.files.length) {
            e.preventDefault();
            showError('Please select a thermal image to upload');
        }
    });
}

/**
 * Set up drag and drop functionality
 * @param {HTMLElement} dropZone - The drop zone element
 * @param {HTMLElement} fileInput - The file input element
 */
function setupDragAndDrop(dropZone, fileInput) {
    // Prevent default behavior for all drag events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Highlight drop zone when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });
    
    // Remove highlight when item is dragged away
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropZone.classList.add('dragover');
    }
    
    function unhighlight() {
        dropZone.classList.remove('dragover');
    }
    
    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            // Trigger change event
            const event = new Event('change');
            fileInput.dispatchEvent(event);
        }
    }
}

/**
 * Display file details in the UI
 * @param {File} file - The selected file
 */
function displayFileDetails(file) {
    const fileNameDisplay = document.querySelector('.file-name');
    const fileSizeDisplay = document.querySelector('.file-size');
    
    if (fileNameDisplay) {
        fileNameDisplay.textContent = file.name;
        fileNameDisplay.classList.add('file-selected');
    }
    
    if (fileSizeDisplay) {
        // Format file size
        let size = file.size;
        let unit = 'bytes';
        
        if (size > 1024) {
            size = size / 1024;
            unit = 'KB';
        }
        
        if (size > 1024) {
            size = size / 1024;
            unit = 'MB';
        }
        
        fileSizeDisplay.textContent = `${size.toFixed(2)} ${unit}`;
    }
}

/**
 * Show image preview in the provided container
 * @param {File} file - The image file
 * @param {HTMLElement} container - The container for the preview
 */
function showImagePreview(file, container) {
    // Clear previous preview
    container.innerHTML = '';
    
    // Only process image files
    if (!file.type.match('image.*')) {
        container.innerHTML = '<p class="error-message">Selected file is not an image</p>';
        return;
    }
    
    // Create image preview
    const img = document.createElement('img');
    img.classList.add('preview-image');
    img.file = file;
    
    container.appendChild(img);
    
    // Use FileReader to read the file and set the image source
    const reader = new FileReader();
    reader.onload = (function(aImg) {
        return function(e) {
            aImg.src = e.target.result;
        };
    })(img);
    
    reader.readAsDataURL(file);
    
    // Add loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.classList.add('loading-indicator');
    loadingIndicator.innerHTML = '<div class="spinner"></div><p>Analyzing image...</p>';
    container.appendChild(loadingIndicator);
    
    // Remove loading indicator when image is loaded
    img.onload = function() {
        container.removeChild(loadingIndicator);
    };
}

/**
 * Show error message
 * @param {string} message - The error message to display
 */
function showError(message) {
    // Check if error container exists
    let errorContainer = document.querySelector('.error-container');
    
    // Create error container if it doesn't exist
    if (!errorContainer) {
        errorContainer = document.createElement('div');
        errorContainer.classList.add('error-container');
        
        // Add to form
        const form = document.getElementById('image-form');
        form.insertBefore(errorContainer, form.firstChild);
    }
    
    // Set error message
    errorContainer.innerHTML = `
        <div class="alert alert-error">
            ${message}
            <button type="button" class="alert-close">&times;</button>
        </div>
    `;
    
    // Add close button functionality
    const closeButton = errorContainer.querySelector('.alert-close');
    closeButton.addEventListener('click', function() {
        errorContainer.innerHTML = '';
    });
    
    // Smooth scroll to error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
