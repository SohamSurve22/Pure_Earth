// pureEarth - Pollution Monitoring Platform
// Chart Configuration File

/**
 * Default chart configuration options
 */
const chartDefaultOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        duration: 1500,
        easing: 'easeOutQuart'
    },
    plugins: {
        legend: {
            labels: {
                font: {
                    family: "'Poppins', 'Segoe UI', sans-serif",
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.7)',
            titleFont: {
                family: "'Poppins', 'Segoe UI', sans-serif",
                size: 14,
                weight: 'bold'
            },
            bodyFont: {
                family: "'Poppins', 'Segoe UI', sans-serif",
                size: 13
            },
            padding: 10,
            cornerRadius: 5,
            displayColors: true
        }
    }
};

/**
 * Color palettes for various chart types
 */
const chartColorPalettes = {
    // Nature-inspired color palette
    primary: [
        '#4CAF50', // leaf-green
        '#2E7D32', // forest-green
        '#64B5F6', // sky-blue
        '#1976D2', // deep-blue
        '#795548', // earth-brown
        '#D32F2F', // clay-red
        '#FFC107'  // sunshine-yellow
    ],
    // AQI category specific colors
    aqi: {
        'Green': '#81C784',
        'Good': '#AED581',
        'Average': '#FFD54F',
        'Poor': '#EF5350'
    },
    // For line and area charts
    gradients: {
        green: {
            start: 'rgba(76, 175, 80, 0.8)',
            end: 'rgba(76, 175, 80, 0.1)'
        },
        blue: {
            start: 'rgba(100, 181, 246, 0.8)',
            end: 'rgba(100, 181, 246, 0.1)'
        }
    }
};

/**
 * Creates a line chart configuration
 * @param {object} data - Chart data with labels and values
 * @param {string} title - Chart title
 * @param {string} yAxisLabel - Y-axis label
 * @returns {object} Chart.js configuration object
 */
function createLineChartConfig(data, title, yAxisLabel) {
    return {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: title,
                data: data.values,
                borderColor: chartColorPalettes.primary[0],
                backgroundColor: 'rgba(76, 175, 80, 0.1)',
                borderWidth: 2,
                pointBackgroundColor: chartColorPalettes.primary[0],
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            ...chartDefaultOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yAxisLabel,
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        padding: 10
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                ...chartDefaultOptions.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    };
}

/**
 * Creates a bar chart configuration
 * @param {object} data - Chart data with labels and values
 * @param {string} title - Chart title
 * @param {string} yAxisLabel - Y-axis label
 * @returns {object} Chart.js configuration object
 */
function createBarChartConfig(data, title, yAxisLabel) {
    return {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: title,
                data: data.values,
                backgroundColor: data.labels.map((label, index) => 
                    chartColorPalettes.primary[index % chartColorPalettes.primary.length]
                ),
                borderWidth: 1,
                borderRadius: 5
            }]
        },
        options: {
            ...chartDefaultOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: yAxisLabel,
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        padding: 10
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            },
            plugins: {
                ...chartDefaultOptions.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    };
}

/**
 * Creates a pie/doughnut chart configuration
 * @param {object} data - Chart data with labels and values
 * @param {string} title - Chart title
 * @param {boolean} isDoughnut - Whether to create a doughnut chart (default: true)
 * @returns {object} Chart.js configuration object
 */
function createPieChartConfig(data, title, isDoughnut = true) {
    // Map colors based on labels if they match AQI categories, or use the primary palette
    const backgroundColors = data.labels.map(label => {
        if (chartColorPalettes.aqi[label]) {
            return chartColorPalettes.aqi[label];
        }
        const index = data.labels.indexOf(label);
        return chartColorPalettes.primary[index % chartColorPalettes.primary.length];
    });
    
    return {
        type: isDoughnut ? 'doughnut' : 'pie',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.values,
                backgroundColor: backgroundColors,
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        },
        options: {
            ...chartDefaultOptions,
            cutout: isDoughnut ? '60%' : 0,
            plugins: {
                ...chartDefaultOptions.plugins,
                title: {
                    display: true,
                    text: title,
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    padding: {
                        top: 10,
                        bottom: 30
                    }
                }
            }
        }
    };
}
