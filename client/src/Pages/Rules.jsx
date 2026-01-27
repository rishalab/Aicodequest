import Navbar from "../Components/Navbar";

export default function Rules() {
  return (
    <>
      <Navbar />
      <div
        className="min-h-screen px-6 py-10"
        style={{ backgroundColor: "white" }}
      >
        <div
          className="max-w-4xl mx-auto rounded-xl shadow-lg p-8 border"
          style={{ backgroundColor: "#white" }}
        >
          <h1
            className="text-3xl font-bold mb-4"
            style={{ color: "#E4334D" }}
          >
            How to Play AICodeQuest
          </h1>

          <p className="mb-6 text-gray-700">
            AICodeQuest is a turn-based programming game where you battle an AI
            by <b>fixing bugs</b> and <b>injecting subtle bugs</b> into code.
            If you truly understand the code, you win.
          </p>

          {/* Game Flow */}
          <h2
            className="text-xl font-semibold mb-2"
            style={{ color: "#E4334D" }}
          >
            Game Flow
          </h2>
          <ul className="list-disc ml-6 mb-6 text-gray-700">
            <li>10 questions per game</li>
            <li>Difficulty increases from A1 → A4</li>
            <li>Each question has up to 2 turns</li>
          </ul>

          {/* Defense */}
          <h2
            className="text-xl font-semibold mb-2"
            style={{ color: "#E4334D" }}
          >
            Turn 0 – Defense (Fix the Bug)
          </h2>
          <ul className="list-disc ml-6 mb-6 text-gray-700">
            <li>The AI gives you buggy code</li>
            <li>Fix <b>one or more bugs</b></li>
            <li>All test cases pass → <b>You win (+1 point)</b></li>
            <li>Any test case fails → <b>AI wins</b></li>
          </ul>

          {/* Attack */}
          <h2
            className="text-xl font-semibold mb-2"
            style={{ color: "#E4334D" }}
          >
            Turn 1 – Attack (Trick the AI)
          </h2>
          <ul className="list-disc ml-6 mb-6 text-gray-700">
            <li>You receive code</li>
            <li>Inject one or more subtle bug</li>
            <li>AI tries to detect and fix it</li>
            <li>If AI fails any test → <b>You win (+1 point)</b></li>
          </ul>

          {/* Bug Levels */}
          <h2
            className="text-xl font-semibold mb-2"
            style={{ color: "#E4334D" }}
          >
            Bug Levels
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            {[
              ["A1", "Syntax errors (off-by-one, wrong operators)"],
              ["A2", "Semantic / logic mistakes"],
              ["A3", "Algorithmic or structural bugs"],
              ["A4", "AI hallucinations & fake assumptions"],
            ].map(([level, desc]) => (
              <div
                key={level}
                className="rounded-lg p-4"
                style={{ backgroundColor: "#e88a96" }}
              >
                <p className="font-semibold text-white">{level}</p>
                <p className="text-white text-sm">{desc}</p>
              </div>
            ))}
          </div>

          {/* Rules */}
          <h2
            className="text-xl font-semibold mb-2"
            style={{ color: "#E4334D" }}
          >
            Important Rules
          </h2>
          <ul className="list-disc ml-6 mb-6 text-gray-700">
            <li>No refactoring or rewriting the solution</li>
            <li>All test cases must pass to win</li>
            <li>Current language support: <b>C</b></li>
          </ul>

          {/* Goal */}
          <div
            className="mt-8 p-5 rounded-lg"
            style={{ backgroundColor: "#E4334D" }}
          >
            <p className="text-white font-semibold">
              Goal:
            </p>
            <p className="text-white">
              Detecting Perturbations shows you understand the code.  
              Creating perturbations proves you understand it deeply.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
