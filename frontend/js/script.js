let apiUrlBase = null;

fetch("/api/url")
  .then(res => res.json())
  .then(data => {
    apiUrlBase = data.url;
    console.log("La URL segura es:", apiUrlBase);

    //Cargar video dinámicamente
    document.getElementById("camFeed").src = apiUrlBase + "/video_feed";

    //Iniciar stats
    actualizarStats();
    setInterval(actualizarStats, 1000);
  })
  .catch(err => {
    console.error("No se pudo obtener la URL segura:", err);
    document.getElementById("errorMsg").textContent = "Error al obtener la URL del backend.";
  });

async function actualizarStats() {
  if (!apiUrlBase) return;

  try {
    const res = await fetch(apiUrlBase + "/api/stats");
    if (!res.ok) throw new Error('Error HTTP ' + res.status);
    const data = await res.json();

    document.getElementById("personCount").textContent = data.person || 0;
    document.getElementById("vehicleCount").textContent = data.vehicle || 0;
    document.getElementById("othersCount").textContent = data.others || 0;
    document.getElementById("fpsCount").textContent = data.fps || 0;
    document.getElementById("errorMsg").textContent = '';
  } catch (err) {
    document.getElementById("errorMsg").textContent = 'Error al actualizar datos: ' + err.message;
    console.error("Error al actualizar datos:", err);
  }
}

setInterval(actualizarStats, 1000);
actualizarStats();