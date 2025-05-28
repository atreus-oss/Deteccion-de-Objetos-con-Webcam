let apiUrlBase = null;
let currentStream = null;

// Función para construir URL sin doble slash
function buildUrl(path) {
  return (apiUrlBase || "").replace(/\/$/, "") + path;
}

// Obtener URL segura desde backend
fetch("/api/url")
  .then(res => {
    if (!res.ok) throw new Error("No se pudo obtener /api/url");
    return res.json();
  })
  .then(data => {
    apiUrlBase = data.url;

    if (!apiUrlBase) {
      throw new Error("La URL está vacía o indefinida");
    }

    console.log("La URL segura es:", apiUrlBase);

    actualizarStats(); // Primera carga
    setInterval(actualizarStats, 1000); // Luego cada 1 segundo
  })
  .catch(err => {
    console.error("Error al obtener la URL del backend:", err.message);
    document.getElementById("errorMsg").textContent =
      "Error al obtener la URL del backend.";
  });

// Cambiar cámara
function detenerStreamActual() {
  if (currentStream) {
    currentStream.getTracks().forEach(track => track.stop());
    currentStream = null;
  }
}

function usarCamara(facingMode = "user") {
  detenerStreamActual();

  const constraints = {
    video: {
      facingMode: { exact: facingMode }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints)
    .then(function (stream) {
      const video = document.getElementById("camFeed");
      video.srcObject = stream;
      currentStream = stream;
    })
    .catch(function (err) {
      console.error("No se pudo acceder a la cámara:", err);
      document.getElementById("errorMsg").textContent =
        "No se pudo acceder a la cámara (" + facingMode + ")";
    });
}

// Iniciar con cámara frontal por defecto
usarCamara("user");

// Consultar estadísticas en el backend
async function actualizarStats() {
  if (!apiUrlBase) return;

  try {
    const res = await fetch(buildUrl("/api/stats"));
    if (!res.ok) throw new Error("Error HTTP " + res.status);

    const data = await res.json();

    document.getElementById("personCount").textContent = data.person || 0;
    document.getElementById("vehicleCount").textContent = data.vehicle || 0;
    document.getElementById("othersCount").textContent = data.others || 0;
    document.getElementById("fpsCount").textContent = data.fps || 0;
    document.getElementById("errorMsg").textContent = "";
  } catch (err) {
    console.error("Error al actualizar datos:", err.message);
    document.getElementById("errorMsg").textContent =
      "Error al actualizar datos: " + err.message;
  }
}
