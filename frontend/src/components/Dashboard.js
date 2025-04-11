import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Dashboard.css";
import {
  FaSignOutAlt, FaFolderOpen, FaChartLine,
  FaFileAlt, FaRocket, FaExclamationCircle,
  FaExclamationTriangle, FaServer
} from "react-icons/fa";

const API_URL = "https://shadowsec-ai.onrender.com";

function Dashboard({ onLogout, token }) {
  const [targetUrl, setTargetUrl] = useState("");
  const [reports, setReports] = useState([]);
  const [summaries, setSummaries] = useState([]);
  const [recommendations, setRecommendations] = useState({});

  const axiosAuth = axios.create({
    baseURL: API_URL,
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const launchScan = async () => {
    try {
      await axiosAuth.post(`/scan`);
      alert("✅ Scan lancé avec succès !");
      fetchAllData();
    } catch (error) {
      console.error(error);
      alert("❌ Erreur lors du lancement du scan.");
    }
  };

  const fetchAllData = async () => {
    try {
      const [reportsRes, summariesRes] = await Promise.all([
        axiosAuth.get(`/reports`),
        axiosAuth.get(`/summaries`)
      ]);
      setReports(reportsRes.data);
      setSummaries(summariesRes.data);
    } catch (error) {
      console.error("Erreur lors du chargement des données :", error);
    }
  };

  const getRecommendations = async (filename) => {
    try {
      const res = await axiosAuth.get(`/recommendations/${filename}`);
      setRecommendations((prev) => ({
        ...prev,
        [filename]: res.data.recommandations
      }));
    } catch (error) {
      console.error("Erreur lors de la récupération des recommandations :", error);
    }
  };

  const getSeverityTag = (summary) => {
    const sqli = summary.some((s) => s.includes("SQLi"));
    const xss = summary.some((s) => s.includes("XSS"));
    const ports = summary.some((s) => s.includes("Ports"));

    if (sqli && xss) return <span className="tag danger">Critique</span>;
    if (sqli || xss) return <span className="tag warning">Élevée</span>;
    if (ports) return <span className="tag moderate">Modérée</span>;
    return <span className="tag safe">Faible</span>;
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  return (
    <div className="dashboard">
      <div className="header">
        <div className="logo">🛡️ <span>ShadowSec</span></div>
        <button className="logout" onClick={onLogout}><FaSignOutAlt /> Se déconnecter</button>
      </div>

      <h1 className="title">ShadowSec AI Dashboard</h1>
      <p className="subtitle">L’IA éthique au service de votre cybersécurité</p>

      <div className="scan-section">
        <input
          type="text"
          placeholder="https://example.com"
          value={targetUrl}
          onChange={(e) => setTargetUrl(e.target.value)}
        />
        <button onClick={launchScan}><FaRocket /> Lancer un Scan</button>
      </div>

      <div className="section">
        <h2><FaFolderOpen /> Rapports générés</h2>
        <div className="report-list">
          {reports.map((r) => (
            <div key={r.filename} className="report-file">
              <FaFileAlt />
              <a href={`${API_URL}/reports/${r.filename}`} target="_blank" rel="noreferrer">{r.filename}</a>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <h2><FaChartLine /> Résumés des rapports</h2>
        {summaries.map((summary) => (
          <div key={summary.filename} className="summary-card">
            <h4>{summary.filename}</h4>
            {getSeverityTag(summary.summary)}
            <ul>
              {summary.summary.map((item, idx) => (
                <li key={idx}>
                  {item.includes("SQLi") && <FaExclamationCircle color="red" />}
                  {item.includes("XSS") && <FaExclamationTriangle color="#e6b800" />}
                  {item.includes("Ports") && <FaServer color="#007bff" />}
                  {" "}{item}
                </li>
              ))}
            </ul>
            <button onClick={() => getRecommendations(summary.filename)} className="recommendation-btn">
              Voir recommandations IA
            </button>

            {recommendations[summary.filename] && (
              <div className="recommendation-box">
                <h5>💡 Recommandations IA :</h5>
                <pre>{recommendations[summary.filename]}</pre>
              </div>
            )}
          </div>
        ))}
      </div>

      <footer>
        <p>© 2025 ShadowSec. <a href="#">CGU</a> · <a href="#">Mentions légales</a> · <a href="#">Contact</a></p>
      </footer>
    </div>
  );
}

export default Dashboard;
