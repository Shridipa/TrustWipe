function copyCertID() {
  const certID = document.getElementById("cert-id").textContent;
  navigator.clipboard.writeText(certID).then(() => {
    alert("Certificate ID copied to clipboard!");
  });
}

function toggleDetails() {
  const details = document.getElementById("extra-details");
  details.style.display = details.style.display === "none" ? "block" : "none";
}