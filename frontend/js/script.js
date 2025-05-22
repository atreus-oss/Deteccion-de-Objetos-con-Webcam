async function actualizarStats() {
    try {
        const res = await fetch('http://localhost:8000/api/stats');
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

navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            document.getElementById("cam").srcObject = stream;
        })
        .catch((err) => {
            console.error("No se pudo acceder a la cámara:", err);
        });