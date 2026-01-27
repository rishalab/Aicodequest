import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Navbar from "../Components/Navbar";
import "../styles/login.css";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/start-game`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "ngrok-skip-browser-warning": "true" },
        body: JSON.stringify({ username }),
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("username", username);
        console.log(data)
        console.log(data["_id"])
        localStorage.setItem("sessionId", data["_id"]);
        localStorage.setItem("userSession", JSON.stringify(data.session));
        navigate("/home");
      } else {
        setError(data.error || "Login failed");
      }
    } catch (err) {
      setError("Network error. Please check your connection.");
      console.error("Login error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <Navbar />

      {/* Login Content */}
      <div className="login-content">
        <form className="login-form" onSubmit={handleSubmit}>
          <h1>Welcome</h1>
          <p className="subtitle">
            AICodeQuest: A comprehension game between <span className="highlight">AI</span> and <span className="highlight">Human</span>
          </p>

          <input
            className="login-input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            required
            disabled={loading}
          />

          {error && <div className="error-message">{error}</div>}

          <button className="login-btn" type="submit" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
