import { msToMinSec } from "../utils/time";
import "../styles/leaderboard.css";

export default function LeaderBoard({ leaderboard }) {
  return (
    <section className="leaderboard-section">
      <div className="leaderboard-container">
        <h2>Leader Board</h2>
        {!leaderboard ? (
          <p className="leaderboard-loading">Loading...</p>
        ) : (
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>User Score</th>
                <th>AI Score</th>
                <th>Avg Human Time</th>
                <th>Human Bug Detection Acc</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((user, index) => (
                <tr key={user.username}>
                  <td>{index + 1}</td>
                  <td>{user.username}</td>
                  <td>{user.human_score}</td>
                  <td>{user.ai_score}</td>
                  <td>{msToMinSec(user.avg_human_time_ms)}</td>
                  <td>{(user.bug_detection_accuracy.human * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}
