document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("predictForm");
    const raceSelect = document.getElementById("race-select");
    const weatherSelect = document.getElementById("weather-select");
    const resultField = document.getElementById("result");
    const predictButton = document.getElementById("predict-button");

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const raceName = raceSelect.value;
        const weather = weatherSelect.value;

        // Disable the button to prevent multiple submissions
        predictButton.disabled = true;

        fetch("/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(), // Assuming CSRF token is in a cookie
            },
            body: JSON.stringify({ race_name: raceName, weather: weather }),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (data.error) {
                    resultField.textContent = `Error: ${data.error}`;
                } else {
                    resultField.textContent = `Predicted Winner: ${data.winner}`;
                }
            })
            .catch((error) => {
                resultField.textContent = `Error: ${error.message}`;
            })
            .finally(() => {
                // Re-enable the button
                predictButton.disabled = false;
            });
    });

    function getCsrfToken() {
        const cookies = document.cookie.split("; ");
        for (const cookie of cookies) {
            const [name, value] = cookie.split("=");
            if (name === "csrftoken") {
                return value;
            }
        }
        return "";
    }
});





 





  


