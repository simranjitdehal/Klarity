// async function sendLogs() {
//     const rawInput = document.getElementById("logInput").value;

//     const parsedInput = JSON.parse(rawInput); // convert textarea text into object

//     // const response = await fetch("https://klarity-production-6a25.up.railway.app/ingest", { # for production
//     const response = await fetch("http://127.0.0.1:8000/ingest", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(parsedInput) // send it directly
//     });

//     const data = await response.json();
//     console.log(data);
//     document.getElementById("output").innerText = data.analysis.summary;
// }

async function fetchLatest() {
    const response = await fetch(
        "https://klarity-production-6a25.up.railway.app/latest"
    );

    const data = await response.json();

    if (data.analysis) {
        document.getElementById("output").innerText =
            data.analysis.summary;
    }
}

// Fetch immediately on page load
fetchLatest();

// Then poll every 5 seconds
setInterval(fetchLatest, 5000);