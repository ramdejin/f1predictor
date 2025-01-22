document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-button");
    const resultsContainer = document.getElementById("results-container");

    let pointsData = [];
    let finalData = [];

    // Load points.csv and final.csv
    Promise.all([
        fetch("/static/points.csv")
            .then(response => response.text())
            .then(data => {
                pointsData = parseCSV(data);
            })
            .catch(error => console.error("Error loading points.csv:", error)),

        fetch("/static/final.csv")
            .then(response => response.text())
            .then(data => {
                finalData = parseCSV(data);
            })
            .catch(error => console.error("Error loading final.csv:", error))
    ]).then(() => {
        console.log("CSV data loaded successfully");
    });

    // Parse CSV to JSON format
    function parseCSV(data) {
        const lines = data.trim().split("\n");
        const headers = lines[0].split(",");
        return lines.slice(1).map(line => {
            const values = line.split(",");
            const obj = {};
            headers.forEach((header, index) => {
                obj[header.trim().toLowerCase()] = values[index] ? values[index].trim() : "";
            });
            return obj;
        });
    }

    // Search functionality
    searchButton.addEventListener("click", () => {
        const query = searchInput.value.trim().toLowerCase();
        resultsContainer.innerHTML = "";

        if (!query) {
            resultsContainer.innerHTML = "<p>Please enter a search query.</p>";
            return;
        }

        // Find the closest match from points.csv
        const matchedDriver = findClosestMatch(query, pointsData, "driver");
        if (!matchedDriver) {
            resultsContainer.innerHTML = "<p>No matching driver found.</p>";
            return;
        }

        const driverName = matchedDriver.driver;
        const driverStats = { ...matchedDriver }; // Clone matched driver stats

        // Use the 'Total' column for Points
        driverStats.Points = driverStats.total || "N/A";

        // Filter final.csv data for the matched driver
        const driverFinalData = finalData.filter(row => row.winner === driverName);

        if (driverFinalData.length > 0) {
            // Fetch the first instance of the values directly
            const wins = driverFinalData[0].winner_driver_wins || "N/A";
            const podiums = driverFinalData[0].winner_driver_podiums || "N/A";
        
            driverStats.Wins = wins;
            driverStats.Podiums = podiums;
        } else {
            driverStats.Wins = "N/A";
            driverStats.Podiums = "N/A";
        }
        

        // Display results
        displayDriverStats(driverStats);
    });

    // Function to find the closest match
    function findClosestMatch(query, data, key) {
        const lowerCaseQuery = query.toLowerCase();
        const matches = data.filter(item => item[key] && item[key].toLowerCase().includes(lowerCaseQuery));
        if (matches.length > 0) {
            // Return the closest match (you can use custom logic here)
            return matches[0];
        }
        return null;
    }

    // Function to display driver stats
    function displayDriverStats(stats) {
        const driverStatsHTML = `
            <div class="driver-stats">
                <p><strong>Driver:</strong> ${stats.driver || "N/A"}</p>
                <p><strong>Team:</strong> ${stats.team || "N/A"}</p>
                <p><strong>Points:</strong> ${stats.Points}</p>
                <p><strong>Wins:</strong> ${stats.Wins}</p>
                <p><strong>Podiums:</strong> ${stats.Podiums}</p>
            </div>
            <hr>
        `;
        resultsContainer.innerHTML = driverStatsHTML;
    }
});





