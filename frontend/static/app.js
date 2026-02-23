async function sendLogs() {
    const rawInput = document.getElementById("logInput").value;

    const parsedInput = JSON.parse(rawInput); // convert textarea text into object

    const response = await fetch("klarity-production-6a25.up.railway.app/ingest", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(parsedInput) // send it directly
    });

    const data = await response.json();
    console.log(data);
    document.getElementById("output").innerText = data.analysis.summary;
}