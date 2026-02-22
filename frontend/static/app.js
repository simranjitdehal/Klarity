async function sendLogs() {
    const rawInput = document.getElementById("logInput").value;

    const parsedInput = JSON.parse(rawInput); // convert textarea text into object

    const response = await fetch("http://127.0.0.1:8000/ingest", {
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