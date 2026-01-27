import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { msToMinSec } from "../utils/time";
import Navbar from "../Components/Navbar";
import LeaderBoard from "../Components/LeaderBoard";
import "../styles/home.css";

export default function Home() {
  const username = localStorage.getItem("username");
  const [summary, setSummary] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/api/get-results`,{
      headers: {
        "ngrok-skip-browser-warning": "true"
      }
    })
      .then(async res => {
        const text = await res.text();
        console.log("RAW RESPONSE:", text.slice(0, 200));
        console.log("API URL =", import.meta.env.VITE_API_URL);

        return JSON.parse(text);
      })
      .then(data => {
        if (data.success) {
          setSummary(data.summary);
          setLeaderboard(data.leaderboard);
        }
      })
      .catch(err => console.error("error:", err));
  }, []);

  return (
    <div className="home-page">
      <Navbar />

      {/* Welcome Section */}
      <section className="welcome-section">
        <h1>Welcome, <span>{username}</span></h1>
        <p className="subtitle">AICodeQuest: A comprehension game between AI and Human</p>
        <Link to="/editor">
          <button className="play-now-btn">Play Now</button>
        </Link>
      </section>

      {leaderboard.length === 0 ? (
        <p className="stats-loading">No leaderboard data yet</p>
      ) : (
        <LeaderBoard leaderboard={leaderboard} />
      )}

      {/* Stats Section */}
      <br />
      <section className="stats-section">
        <h3>Stats</h3>
        {!summary ? (
          <p className="stats-loading">Loading stats...</p>
        ) : (
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-label">Total bugs solved</div>
              <div className="stat-value">{summary.total_bugs_solved}</div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Total No.of Participants</div>
              <div className="stat-value">{summary.total_participants}</div>
            </div>
            <div className="stat-item"> 
              <div className="stat-label">Overall Bug Detection Acc</div>
              <div className="stat-value">{summary?.bug_detection_accuracy?.human != null
                ? summary.bug_detection_accuracy.human * 100
                : "N/A"}%
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-label">Total Avg Human Time</div>
              <div className="stat-value">{msToMinSec(summary.avg_human_time_ms)}</div>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
