import React, { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

 const checkURL = async () => {
  setLoading(true);
  try {
    const res = await axios.post("https://phishing-url-detector-2-d7yk.onrender.com/predict", {
      url: url,
    });
    setResult(`${res.data.result} (${res.data.confidence}%)`);
  } catch (error) {
    setResult("Error connecting to server");
  }
  setLoading(false);
};

return (
  <div style={{
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    background: "linear-gradient(to right, #667eea, #764ba2)"
  }}>
    <div style={{
      background: "white",
      padding: "30px",
      borderRadius: "10px",
      boxShadow: "0 4px 15px rgba(0,0,0,0.2)",
      textAlign: "center"
    }}>

      <h1>PhishDetect 🔒</h1>

      <input
        type="text"
        placeholder="Enter URL (https://example.com)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        style={{
          width: "300px",
          padding: "12px",
          borderRadius: "5px",
          border: "1px solid #ccc",
          marginBottom: "15px"
        }}
      />

      <br />

      <button
        onClick={checkURL}
        style={{
          padding: "10px 20px",
          backgroundColor: "#667eea",
          color: "white",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer"
        }}
      >
        Check URL
      </button>

      {/* Loading */}
      {loading && <p>Checking... 🔍</p>}

      {/* Result */}
      {!loading && result && (
        <p style={{
          color:
            result.includes("Phishing") ? "red" :
            result.includes("Safe") ? "green" : "orange",
          fontWeight: "bold",
          fontSize: "20px",
          marginTop: "15px"
        }}>
          {result}
        </p>
      )}

      <p style={{ fontSize: "12px", color: "gray", marginTop: "10px" }}>
        ML-powered phishing detection using Random Forest
      </p>

    </div>
  </div>
);}

export default App;
