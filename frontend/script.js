document.getElementById("run").addEventListener("click", async () => {
    const prompt = document.getElementById("prompt").value.trim();
    const resultBox = document.getElementById("result");
  
    if (!prompt) {
      resultBox.textContent = "Please enter a prompt first.";
      return;
    }
  
    resultBox.innerHTML = "<span class='loading'>Running inference...</span>";
  
    try {
      const response = await fetch("http://localhost:7072/api/infer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, region: "us-east" })
      });
  
      const data = await response.json();
  
      if (data.ok) {
        resultBox.innerHTML = `
          <strong>Output:</strong> ${data.output || "(no output)"}<br><br>
          <strong>Model:</strong> ${data.model}<br>
          <strong>Duration:</strong> ${data.duration_sec}s<br>
          <strong>Energy Used:</strong> ${data.energy_kwh.toFixed(6)} kWh<br>
          <strong>Carbon Emitted:</strong> ${data.carbon_kg.toFixed(6)} kg<br>
          <strong>Region:</strong> ${data.region}
        `;
      } else {
        resultBox.textContent = "Error: " + (data.error || "Unknown error");
      }
    } catch (err) {
      resultBox.textContent = "Failed to connect to backend.";
    }
  });
  