// 🎯 Button click animation
document.querySelectorAll(".btn").forEach(btn => {
  btn.addEventListener("click", function () {
    this.style.transform = "scale(0.95)";
    setTimeout(() => {
      this.style.transform = "scale(1)";
    }, 150);
  });
});

// 🔔 Auto hide alerts
setTimeout(() => {
  document.querySelectorAll(".alert").forEach(alert => {
    alert.style.display = "none";
  });
}, 4000);