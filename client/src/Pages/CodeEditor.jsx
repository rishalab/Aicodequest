import Editor from "@monaco-editor/react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../Components/Navbar";
import "../styles/editor.css";
import { useRef } from "react";

export default function CodeEditor() {
  const navigate = useNavigate();
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("");
  const [results, setResults] = useState([]);
  const [overallPass, setOverallPass] = useState(null);
  const [openIndex, setOpenIndex] = useState(null);
  const [turn, setTurn] = useState(0);
  const [action, setAction] = useState([]);
  const [selectedAction, setSelectedAction] = useState("");
  const [hasSubmitted, setHasSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const [aiCorrectedCode, setAiCorrectedCode] = useState("");
  const [level, setLevel] = useState("");
  const [isRunningTests, setIsRunningTests] = useState(false);
  const [showLevelOverlay, setShowLevelOverlay] = useState(false);

  const lastLevelRef = useRef("");

  const session_id = localStorage.getItem("sessionId");

  const fetchCode = async (withDelay = false) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/get-code?session_id=${session_id}`,{
      headers: {
        "ngrok-skip-browser-warning": "true"
      }
    });
      const data = await res.json();

      if (data.status === "completed") {
        navigate("/home");
        return;
      }

      const previousLevel = lastLevelRef.current;
      const newLevel = data.level || "";

      setCode(data.code || "");
      setLanguage(data.language || "");
      setTurn(data.turn || 0);
      setAction(data.allowed_actions || []);
      setLevel(newLevel);

      // Show overlay when level changes OR on first load
      if (newLevel && (newLevel !== previousLevel || previousLevel === "")) {
        setShowLevelOverlay(true);
      }

      lastLevelRef.current = newLevel;

      console.log("Fetched new code:", data);
    } catch (err) {
      console.error("Error fetching code:", err);
    } finally {
      if (withDelay) {
        setTimeout(() => setIsLoading(false), 5000);
      } else {
        setIsLoading(false);
      }
    }
  };

  useEffect(() => {
    fetchCode();
  }, []);

  const handleSubmit = async () => {
    setIsLoading(true);
    setIsRunningTests(true);
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/submit-code`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        body: JSON.stringify({
          session_id,
          code,
          language,
          action,
        }),
      });

      const data = await res.json();

      setResults(data["results_info"]["results"] || []);
      setOverallPass(data.results_info?.overall_pass ?? false);
      setHasSubmitted(true);
      setMsg(data["msg"]);
      setAiCorrectedCode(data["ai_corrected_code"]);
      console.log("Submit response:", data);
    } catch (err) {
      console.error(err);
    } finally {
      setIsRunningTests(false);
      setIsLoading(false);
    }
  };

  const handleActionClick = async (actionText) => {
    try {
      setSelectedAction(actionText);
      console.log("Selected action:", actionText);

      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/submit-action`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        body: JSON.stringify({
          session_id,
          action: actionText,
          turn,
        }),
      });

      const data = await res.json();
      console.log("Action response:", data);

      setHasSubmitted(false);
      setSelectedAction("");
      setResults([]);
      setOverallPass(null);

      setIsLoading(true);

      setTimeout(async () => {
        await fetchCode(true);
      }, 500);
    } catch (err) {
      console.error("Failed to send action:", err);
      setIsLoading(false);
    }
  };

  const LEVEL_INFO = {
    A1: {
      questionRange: "1-2",
      title: "Level A1: Syntax-Level Bugs",
      description: "Syntax-level or shallow bugs (off-by-one, typos, minor indexing errors).",
      bugTypes: [
        { type: "Off-by-one", example: "for i in range(0) → range(0+1)" },
        { type: "Missing return", example: "Remove return result from branch" },
        { type: "Wrong initialization", example: "let x = 0 when it should be x = 1" }
      ]
    },
    A2: {
      questionRange: "3-4",
      title: "Level A2: Semantic Bugs",
      description: "Semantic bugs caused by incorrect operators or conditions.",
      bugTypes: [
        { type: "Wrong operator", example: "if sum > max → sum < max" },
        { type: "Reversed logic", example: "if x < threshold → x > threshold" },
        { type: "Wrong operation", example: "product *= x → product += x" }
      ]
    },
    A3: {
      questionRange: "5-6",
      title: "Level A3: Edge Cases",
      description: "Missing edge cases or boundary condition failures.",
      bugTypes: [
        { type: "Missing edge case", example: "Not handling empty arrays" },
        { type: "Wrong algorithm", example: "Radians without all-negative handling" },
        { type: "Wrong data type", example: "Using list when dict is required" }
      ]
    },
    A4: {
      questionRange: "7-10",
      title: "Level A4: AI-Style Logic Bugs",
      description: "Plausible but incorrect logic or overgeneralized reasoning (AI-style bugs).",
      bugTypes: [
        { type: "Fake API", example: "arr.find_median() (doesn't exist)" },
        { type: "Wrong algorithm", example: "Misunderstood pattern" },
        { type: "Plausible error", example: "Summing indices instead of values" }
      ]
    }
  };

  const getCurrentLevelInfo = () => {
    return LEVEL_INFO[lastLevelRef.current] || LEVEL_INFO.A1;
  };

  return (
    <div className="editor-page">
      <Navbar />

      {/* Level Information Overlay */}
      {showLevelOverlay && (
        <div className="level-overlay-backdrop">
          <div className="level-overlay-content">
            <h1 className="level-overlay-title">
              {getCurrentLevelInfo().title}
            </h1>
            
            <p className="level-overlay-question-range">
              Questions {getCurrentLevelInfo().questionRange} of 10
            </p>

            <p className="level-overlay-description">
              {getCurrentLevelInfo().description}
            </p>

            <div className="level-overlay-bug-types">
              <h3 className="bug-types-title">
                Bug Types for This Level:
              </h3>
              
              {getCurrentLevelInfo().bugTypes.map((bug, index) => (
                <div 
                  key={index} 
                  className="bug-type-item"
                  style={{
                    borderBottom: index < getCurrentLevelInfo().bugTypes.length - 1 ? "1px solid #334155" : "none"
                  }}
                >
                  <p className="bug-type-name">
                    {bug.type}
                  </p>
                  <code className="bug-type-example">
                    {bug.example}
                  </code>
                </div>
              ))}
            </div>

            <div className="level-overlay-warning">
              <p className="warning-title">
                ⚠️ Important Instruction for Attack Mode:
              </p>
              <p className="warning-text">
                When injecting bugs, please inject only <strong>{lastLevelRef.current || "A1"}-level bugs</strong> as described above. 
                Stay within the bug taxonomy for this level.
              </p>
            </div>

            <button
              onClick={() => setShowLevelOverlay(false)}
              className="level-overlay-start-btn"
            >
              Start Coding
            </button>
          </div>
        </div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <div className="loading-overlay">
          {isRunningTests ? (
            <p className="loading-text">Running test cases...</p>
          ) : (
            <>
              <h3>Level {lastLevelRef.current}</h3>
              <p style={{ marginTop: "8px", fontSize: "14px", color: "#cbd5f5" }}>
                {getCurrentLevelInfo().description}
              </p>
              <p className="loading-text">Preparing next level...</p>
            </>
          )}
        </div>
      )}

      {/* Toolbar */}
      <div className="editor-toolbar">
        <div className="mode-message">
          {turn === 0
            ? "You are in defense mode. Find and fix the bug, then submit."
            : "You are in attack mode. Inject a subtle bug and submit."}
        </div>
        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={isLoading}
        >
          {isLoading ? "Processing..." : "Submit"}
        </button>
      </div>

      {/* Editor */}
      <div className="editor-container">
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={(value) => setCode(value)}
          theme="vs-dark"
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            automaticLayout: true,
          }}
        />
      </div>

      {/* Results Overlay */}
      {hasSubmitted && action && action.length > 0 && (
        <div className="results-overlay">
          <div className="results-box">
            <h2>Submission Results</h2>

            {/* Test Results */}
            {results.length > 0 && (
              <div>
                <h3>Test Results</h3>
                <div className="test-cases">
                  {results.map((test, index) => {
                    const isOpen = openIndex === index;
                    return (
                      <div key={index} className="test-case">
                        <div
                          className={`test-case-header ${test.pass ? "passed" : "failed"}`}
                          onClick={() => setOpenIndex(isOpen ? null : index)}
                        >
                          <span>Test Case {index + 1}</span>
                          <span>{test.pass ? "Passed" : "Failed"}</span>
                        </div>
                        {isOpen && (
                          <div className="test-case-details">
                            <div>
                              <span>Input:</span> <code>{test.stdin || "(empty)"}</code>
                            </div>
                            <div>
                              <span>Expected:</span> <code>{test.expected}</code>
                            </div>
                            <div>
                              <span>Output:</span> <code>{test.stdout || "(empty)"}</code>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>

                {msg && <p className="result-message">{msg}</p>}
                
                {aiCorrectedCode !== "" && (
                  <pre style={{ 
                    whiteSpace: "pre-wrap", 
                    background: "#0f172a",
                    color: "#e5e7eb",
                    padding: "12px",
                    borderRadius: "8px",
                    overflowX: "auto"
                  }}>
                    <code>{aiCorrectedCode}</code>
                  </pre>
                )}

                {overallPass !== null && (
                  <div className={`overall-result ${overallPass ? "passed" : "failed"}`}>
                    {overallPass ? "All tests passed!" : "Some tests failed"}
                  </div>
                )}
              </div>
            )}

            {/* Action Selection */}
            <div className="action-section">
              <h3>Choose Your Next Action</h3>
              <p>Select an action to continue:</p>

              <div className="action-grid">
                {action.map((actionText, index) => (
                  <button
                    key={index}
                    className={`action-btn ${selectedAction === actionText ? "selected" : ""}`}
                    disabled={isLoading}
                    onClick={() => handleActionClick(actionText)}
                  >
                    {actionText}
                  </button>
                ))}
              </div>

              {selectedAction && !isLoading && (
                <div className="action-feedback">
                  <p>
                    Action selected: <strong>{selectedAction}</strong>
                  </p>
                  <p>Processing action and fetching new code...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}