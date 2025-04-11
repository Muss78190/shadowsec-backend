import React, { useState } from "react";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    try {
      const response = await fetch("https://shadowsec-ai.onrender.com/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ username, password }),
      });

      const data = await response.json();
      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        window.location.href = "/dashboard";
      } else {
        setMessage("❌ Identifiants incorrects.");
      }
    } catch (error) {
      setMessage("❌ Erreur réseau.");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "400px", margin: "auto" }}>
      <h2>Connexion à ShadowSec AI</h2>
      <input type="text" placeholder="Nom d'utilisateur" value={username} onChange={(e) => setUsername(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }} />
      <input type="password" placeholder="Mot de passe" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: "100%", padding: "0.5rem", marginBottom: "1rem" }} />
      <button onClick={handleLogin} style={{ padding: "0.75rem 1.5rem", cursor: "pointer" }}>Se connecter</button>
      {message && <p style={{ marginTop: "1rem", color: "red" }}>{message}</p>}
    </div>
  );
}

export default Login;
