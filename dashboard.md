---
layout: page
title: Farm Dashboard
description: Real-time data from Kalemie Agro poultry farm
---

## 🐔 Poultry Farm Dashboard

<div id="dashboard-content">
  <p>Loading data...</p>
</div>

<canvas id="tempChart" width="400" height="200"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
  async function loadDashboard() {
    try {
      const response = await fetch("https://api.kalemieagro.com/api/dashboard", {
        headers: {
          "Authorization": "Bearer YOUR_API_TOKEN"
        }
      });
      const data = await response.json();

      document.getElementById("dashboard-content").innerHTML = `
        <h3>🌡️ Temperature: ${data.temperature}°C</h3>
        <h3>💧 Humidity: ${data.humidity}%</h3>
        <h3>🍽️ Feed Level: ${data.feed_level}</h3>
        <h3>🚰 Water Level: ${data.water_level}</h3>
      `;

      const ctx = document.getElementById('tempChart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.temperature_readings.map((reading, index) => `T${index + 1}`),
          datasets: [{
            label: 'Temperature Over Time',
            data: data.temperature_readings,
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true,
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false
            }
          }
        }
      });
    } catch (error) {
      document.getElementById("dashboard-content").innerHTML = "<p>Error loading data.</p>";
      console.error("Dashboard fetch error:", error);
    }
  }

  loadDashboard();
</script>
