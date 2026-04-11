// // async function sendLogs() {
// //     const rawInput = document.getElementById("logInput").value;

// //     const parsedInput = JSON.parse(rawInput); // convert textarea text into object

// //     // const response = await fetch("https://klarity-production-6a25.up.railway.app/ingest", { # for production
// //     const response = await fetch("http://127.0.0.1:8000/ingest", {
// //         method: "POST",
// //         headers: {
// //             "Content-Type": "application/json"
// //         },
// //         body: JSON.stringify(parsedInput) // send it directly
// //     });

// //     const data = await response.json();
// //     console.log(data);
// //     document.getElementById("output").innerText = data.analysis.summary;
// // }

// async function fetchLatest() {
//     const response = await fetch(
//         "http://127.0.0.1:8000/latest"
//     );

//     const data = await response.json();

//     if (data.analysis) {
//         document.getElementById("output").innerText =
//             data.analysis.summary;
//     }
// }

// // Fetch immediately on page load
// fetchLatest();

// // Then poll every 5 seconds
// setInterval(fetchLatest, 5000);

function sendLogs() {
    fetch("http://127.0.0.1:8000/logs/completed", {
        headers: {
            "x-api-key": "ske985d2519612d30974583064f8a5c84f"
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            document.getElementById("output").innerText = data.message;
            return;
        }

        document.getElementById("output").innerText =
`Summary: ${data.ai_summary}

Cause: ${data.probable_cause}

Fix: ${data.fix_summary}

Steps: ${data.detailed_steps}

Severity: ${data.severity}`;
    });
}