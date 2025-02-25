
document.addEventListener("DOMContentLoaded", function () {
  // Establecer la fecha actual en los campos de fecha si están presentes
  const dateInputs = document.querySelectorAll('input[type="date"]');
  if (dateInputs.length > 0) {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const dd = String(today.getDate()).padStart(2, "0");
    const formattedDate = `${yyyy}-${mm}-${dd}`;

    dateInputs.forEach((input) => {
      if (input.value === "") {
        input.value = formattedDate;
      }
    });
  }

  
  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    setTimeout(function () {
      alerts.forEach((alert) => {
        const closeButton = alert.querySelector(".btn-close");
        if (closeButton) {
          closeButton.click();
        }
      });
    }, 5000);
  }

  
  const badges = document.querySelectorAll(".badge");
  badges.forEach((badge) => {
    badge.style.transition = "all 0.3s ease-in-out";
    badge.addEventListener("mouseover", function () {
      this.style.transform = "scale(1.1)";
    });
    badge.addEventListener("mouseout", function () {
      this.style.transform = "scale(1)";
    });
  });
});


function confirmarEliminar(mensaje) {
  return confirm(
    mensaje || "¿Estás seguro de que deseas eliminar este elemento?"
  );
}
