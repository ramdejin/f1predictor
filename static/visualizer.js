document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('myChart');
    if (!canvas) {
        console.error('Canvas element with ID "myChart" not found!');
        return;
    }

    const ctx = canvas.getContext('2d');

    fetch('points.csv')
        .then(response => response.text())
        .then(csvData => parseAndProcessCSV(csvData))
        .then(({ labels, datasets }) => createChart(ctx, labels, datasets))
        .catch(error => console.error("Error loading or parsing CSV data:", error));
});

/**
 * Parses CSV, extracts points data, converts to cumulative scores per driver across races
 * @param {string} csvData Raw CSV data
 * @returns {Promise<{labels: Array<string>, datasets: Array<Object>}>}
 */
function parseAndProcessCSV(csvData) {
    const rows = csvData.trim().split('\n');
    const header = rows.shift().split(',');; // Extract the header row

    // Dynamically map race columns (1 through 24)
    const raceIndices = Array.from({ length: 24 }, (_, index) => index + 4);

    const driverData = {};

    // Parse each row to process the race points data
    rows.forEach(row => {
        const cols = row.split(',');

        const driverName = cols[1];
        const pointsArray = raceIndices.map(index => parseInt(cols[index], 10) || 0);

        // Calculate cumulative points over time
        const cumulativePoints = pointsArray.reduce((acc, points, index) => {
            if (index === 0) {
                acc.push(points); // Initialize with first race's points
            } else {
                acc.push(acc[index - 1] + points); // Add cumulative points from previous race
            }
            return acc;
        }, []);

        // Map driver name to cumulative points data
        driverData[driverName] = cumulativePoints;
    });

    // Prepare the data for plotting
    const labels = Array.from({ length: 24 }, (_, i) => `Race ${i + 1}`); // X-axis labels
    const datasets = Object.keys(driverData).map(driver => ({
        label: driver,
        data: driverData[driver],
        borderColor: randomRGBA(),
        backgroundColor: "rgba(0,0,0,0)",
        borderWidth: 2,
    }));

    return { labels, datasets };
}

/**
 * Dynamically creates a chart using provided Chart.js data
 * @param {CanvasRenderingContext2D} ctx Canvas rendering context
 * @param {Array<string>} labels X-axis labels
 * @param {Array<Object>} datasets Data series for each driver
 */
function createChart(ctx, labels, datasets) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Races"
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: "Point Total"
                    }
                }
            }
        }
    });
}

/**
 * Generate random RGBA values for chart colors
 */
function randomRGBA() {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgba(${r}, ${g}, ${b}, 0.6)`;
}
