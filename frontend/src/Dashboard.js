import React, { useState } from "react";

function Dashboard() {
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("token");

  const handleScan = async () => {
    if (!url) {
      setMessage("❗️Veuillez entrer une URL.");
      return;
    }

    setLoading(true);
    setMessage("🔎 Scan en cours...");

    try {
      const response = await fetch("https://shadowsec-ai.onrender.com/scan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage(`✅ ${data.message}`);
      } else {
        setMessage(`❌ Erreur : ${data.detail || "Inconnue"}`);
      }
    } catch (error) {
      setMessage(`❌ Erreur de connexion : ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h2>Scanner une cible avec ShadowSec AI</h2>
      <input
        type="text"
        placeholder="ex : scanme.nmap.org"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }}
      />
      <button
        onClick={handleScan}
        disabled={loading}
        style={{ padding: "0.75rem 1.5rem", cursor: "pointer" }}
      >
        Lancer le scan
      </button>
      {message && <p style={{ marginTop: "1rem" }}>{message}</p>}
    </div>
  );
}

export default Dashboard;
