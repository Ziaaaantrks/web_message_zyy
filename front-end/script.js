document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form");
  const alertBox = document.getElementById("custom-alert");
  const alertMsg = document.getElementById("alert-message");
  const alertIcon = document.getElementById("alert-icon");
   //panggil jika data siap
   console.log("Data siap")
  // Fungsi pembantu untuk memunculkan alert
  function myAlert(message, type) {
    alertMsg.innerText = message;
    alertIcon.innerText = type === "success" ? "✅" : "❌";
    
    alertBox.className = `custom-alert show ${type}`;
    
    // Hilang otomatis setelah 4 detik
    setTimeout(() => {
      alertBox.classList.remove("show");
    }, 4000);
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = Object.fromEntries(new FormData(this).entries());

    try {
      const res = await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await res.json();
      console.log(result)
      console.log(data)
      if (!res.ok) throw new Error(result.message || "Gagal kirim data");
      // Panggil alert sukses
      myAlert("Berhasil! Pesan terkirim 🚀", "success");
      this.reset();

    } catch (err) {
      // Panggil alert gagal
      myAlert("Gagal mengirim pesan! ada beberapa kendala");
    }
  });
});