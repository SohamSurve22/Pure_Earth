// pureEarth - Pollution Monitoring Platform
// Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    console.log('pureEarth application initialized');
    
    // Mobile Navigation Toggle
    initMobileNav();
    
    // Initialize flash message dismissal
    initFlashMessages();
    
    // Initialize page-specific functionalities
    const currentPage = document.body.dataset.page;
    
    switch(currentPage) {
        case 'dashboard':
            initDashboard();
            break;
        case 'aqi-calculator':
            initAQICalculator();
            break;
        case 'image-analyzer':
            initImageAnalyzer();
            break;
        case 'leaderboard':
            initLeaderboard();
            break;
        default:
            // Home page or other pages
            break;
    }
    
    // Add animations to elements as they come into view
    initScrollAnimations();
});

/**
 * Initialize mobile navigation
 */
function initMobileNav() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            
            // Change the toggle icon
            const icon = this.querySelector('i');
            if (icon.classList.contains('fa-bars')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}

/**
 * Initialize flash message dismissal
 */
function initFlashMessages() {
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    });
    
    // Auto-dismiss success messages after 5 seconds
    const successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });
}

/**
 * Initialize dashboard charts and statistics
 */
function initDashboard() {
    // Check if the required elements exist
    if (!document.getElementById('aqi-chart') || !document.getElementById('thermal-chart')) {
        return;
    }
    
    // Get chart data from the data attributes
    const aqiChartElement = document.getElementById('aqi-chart');
    const thermalChartElement = document.getElementById('thermal-chart');
    
    // Initialize charts if data exists
    if (aqiChartElement.dataset.categories) {
        const aqiCategories = JSON.parse(aqiChartElement.dataset.categories);
        initAQIPieChart(aqiCategories);
    }
    
    if (thermalChartElement.dataset.categories) {
        const thermalCategories = JSON.parse(thermalChartElement.dataset.categories);
        initThermalPieChart(thermalCategories);
    }
    
    // Initialize statistic counters
    initCountAnimation();
}

/**
 * Initialize AQI pie chart
 */
function initAQIPieChart(data) {
    const ctx = document.getElementById('aqi-chart').getContext('2d');
    
    // Prepare data for Chart.js
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Define colors for each AQI category
    const colors = {
        'Green': '#81C784',
        'Good': '#AED581',
        'Average': '#FFD54F',
        'Poor': '#EF5350'
    };
    
    // Map colors to data
    const backgroundColors = labels.map(label => colors[label] || '#ccc');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'AQI Submissions by Category',
                    font: {
                        size: 16
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

/**
 * Initialize Thermal Analysis pie chart
 */
function initThermalPieChart(data) {
    const ctx = document.getElementById('thermal-chart').getContext('2d');
    
    // Prepare data for Chart.js
    const labels = Object.keys(data);
    const values = Object.values(data);
    
    // Define colors for each thermal category
    const colors = {
        'Green': '#81C784',
        'Good': '#AED581',
        'Average': '#FFD54F',
        'Poor': '#EF5350'
    };
    
    // Map colors to data
    const backgroundColors = labels.map(label => colors[label] || '#ccc');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Thermal Analyses by Category',
                    font: {
                        size: 16
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true
            }
        }
    });
}

/**
 * Initialize count animation for statistics
 */
function initCountAnimation() {
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(stat => {
        const targetValue = parseFloat(stat.dataset.value);
        const duration = 1500; // Animation duration in ms
        const step = Math.ceil(targetValue / (duration / 16)); // 60fps
        let current = 0;
        
        const updateValue = () => {
            current += step;
            if (current >= targetValue) {
                current = targetValue;
                stat.textContent = targetValue;
                return;
            }
            stat.textContent = Math.floor(current);
            requestAnimationFrame(updateValue);
        };
        
        updateValue();
    });
}

/**
 * Initialize AQI Calculator form
 */
function initAQICalculator() {
    const aqiForm = document.getElementById('aqi-form');
    
    if (!aqiForm) return;
    
    aqiForm.addEventListener('submit', function(e) {
        // Form validation is handled by the browser's built-in validation
        // Let the form submit normally to the server
    });
    
    // Live AQI calculation preview
    const inputFields = aqiForm.querySelectorAll('input, select');
    const previewElement = document.getElementById('aqi-preview');
    
    if (previewElement) {
        inputFields.forEach(field => {
            field.addEventListener('change', calculatePreviewAQI);
        });
    }
}

/**
 * Calculate AQI preview based on form values
 */
function calculatePreviewAQI() {
    const form = document.getElementById('aqi-form');
    const previewElement = document.getElementById('aqi-preview');
    
    // Get values from form
    const energyConsumption = parseFloat(form.querySelector('[name="energy_consumption"]').value) || 0;
    const fuelType = form.querySelector('[name="fuel_type"]').value;
    const wasteEmissions = parseFloat(form.querySelector('[name="waste_emissions"]').value) || 0;
    const vehiclesOperated = parseInt(form.querySelector('[name="vehicles_operated"]').value) || 0;
    const windSpeed = parseFloat(form.querySelector('[name="wind_speed"]').value) || 0;
    const rainfall = parseFloat(form.querySelector('[name="rainfall"]').value) || 0;
    
    // Check if all required fields are filled
    if (!energyConsumption || !fuelType || !wasteEmissions || !vehiclesOperated || !windSpeed || !rainfall) {
        previewElement.innerHTML = '<div class="alert alert-info">Fill all fields for preview calculation</div>';
        return;
    }
    
    // Prepare data for API call
    const data = {
        energy_consumption: energyConsumption,
        fuel_type: fuelType,
        waste_emissions: wasteEmissions,
        vehicles_operated: vehiclesOperated,
        wind_speed: windSpeed,
        rainfall: rainfall
    };
    
    // Call API for calculation
    fetch('/api/aqi-calculator', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            previewElement.innerHTML = `<div class="alert alert-error">${result.error}</div>`;
            return;
        }
        
        // Update preview with result
        previewElement.innerHTML = `
            <div class="aqi-preview-result">
                <div class="aqi-score">${result.aqi_score}</div>
                <div class="aqi-category category-${result.aqi_category}">${result.aqi_category}</div>
                <p>This is a preview calculation. Submit the form to save your data.</p>
            </div>
        `;
    })
    .catch(error => {
        previewElement.innerHTML = `<div class="alert alert-error">Error calculating AQI: ${error.message}</div>`;
    });
}

/**
 * Initialize Image Analyzer
 */
function initImageAnalyzer() {
    const uploadContainer = document.querySelector('.upload-container');
    const fileInput = document.getElementById('thermal-image');
    
    if (!uploadContainer || !fileInput) return;
    
    // Handle drag and drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, () => {
            uploadContainer.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadContainer.addEventListener(eventName, () => {
            uploadContainer.classList.remove('dragover');
        }, false);
    });
    
    uploadContainer.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            updateFileNameDisplay(files[0].name);
        }
    }
    
    // Update file name display when a file is selected
    fileInput.addEventListener('change', function() {
        if (this.files.length) {
            updateFileNameDisplay(this.files[0].name);
        }
    });
    
    function updateFileNameDisplay(fileName) {
        const fileNameDisplay = document.querySelector('.file-name');
        if (fileNameDisplay) {
            fileNameDisplay.textContent = fileName;
            fileNameDisplay.classList.add('file-selected');
        }
    }
}

/**
 * Initialize Leaderboard
 */
function initLeaderboard() {
    // Add animations to leaderboard rows
    const leaderboardRows = document.querySelectorAll('.leaderboard-table tbody tr');
    
    leaderboardRows.forEach((row, index) => {
        // Add staggered animation delay
        row.style.animationDelay = `${index * 0.1}s`;
        row.classList.add('animate-fade-in');
    });
}

/**
 * Initialize scroll animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (!animatedElements.length) return;
    
    // Check if elements are in viewport
    function checkInView() {
        animatedElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('visible');
            }
        });
    }
    
    // Add listener for scroll
    window.addEventListener('scroll', checkInView);
    
    // Check on load
    checkInView();
}
