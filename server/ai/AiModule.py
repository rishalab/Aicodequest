import requests
import time
import os

from dotenv import load_dotenv

load_dotenv()

class RateLimitError(Exception):
    pass


class AiModule:
    def __init__(self):
        """
        Groq-only model rotation.
        Order = priority (best → fallback)
        """

        self.api_key = os.getenv("GROQ_API_KEY")
        print("API KEY ", self.api_key)
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.models = [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "llama-4-maverick-17b-128e-instruct",
            "groq/compound",
        ]

        self.current_index = 0
        self.endpoint = "https://api.groq.com/openai/v1/chat/completions"

    # -------------------- PUBLIC API --------------------

    def inject_bug(self, code: str, level: str) -> str:
        """
        Injects ONE subtle bug into code.
        Automatically switches Groq models on rate limit.
        """

        prompt = self._build_prompt_to_inject(code, level)
        print("prompt  :\n ",prompt)
        for _ in range(len(self.models)):
            model = self.models[self.current_index]

            try:
                return self._call_groq(model, prompt)
            except RateLimitError:
                print(f"[AiModule] Rate limit hit on {model}, switching model...")
                self._switch_model()
            except Exception as e:
                print(f"[AiModule] Error on {model}: {e}")
                self._switch_model()

        raise RuntimeError("All Groq models exhausted")

    def detect_bug_by_ai(self, code: str) -> str:
        """
        Detects the bug given by the Human
        Automatically switches Groq models on rate limit.
        """

        prompt = self._build_prompt_to_detect(code)
        print("prompt  ; ",prompt)
        for _ in range(len(self.models)):
            model = self.models[self.current_index]
            print("Modle : ",model)
            try:
                return self._call_groq(model, prompt)
            except RateLimitError:
                print(f"[AiModule] Rate limit hit on {model}, switching model...")
                self._switch_model()
            except Exception as e:
                print(f"[AiModule] Error on {model}: {e}")
                self._switch_model()

        raise RuntimeError("All Groq models exhausted")

    # -------------------- GROQ CALL --------------------

    def _call_groq(self, model: str, prompt: str) -> str:
        response = requests.post(
            self.endpoint,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a programming instructor."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2
            },
            timeout=15
        )

        if response.status_code == 429:
            raise RateLimitError()

        response.raise_for_status()
        print("response ", response.json()["choices"][0]["message"])
        return response.json()["choices"][0]["message"]["content"]

    # -------------------- HELPERS --------------------

    def _switch_model(self):
        self.current_index = (self.current_index + 1) % len(self.models)
        time.sleep(0.2)

    def _build_prompt_to_inject(self, code: str, level: str) -> str:
        prompt_based_on_level={
            "A1": f"""
                Inject A1-level bugs (Surface / Syntactic bugs) into the following code.

                A1 Definition (Surface-Level Bugs):
                Errors that are obvious on inspection
                Localized to a single line or expression
                Do NOT alter the underlying algorithm

                Allowed Bug Types (ONLY these):
                Off-by-one loop boundary errors (i < n → i <= n, i = 0 → i = 1)
                Missing or incorrect return statement
                Wrong variable initialization (e.g., sum = 1 instead of 0)
                Incorrect constant or literal value
                Simple arithmetic operator mistake (+ ↔ -, * ↔ +)
                Indexing mistake (arr[i] → arr[i+1] or arr[i-1])
                Using the wrong existing variable name

                STRICT CONSTRAINTS:
                Inject bugs ONLY inside the problem-solving function(s)
                Do NOT modify the main() function
                main() is used strictly for test case execution and must remain correct
                Do NOT add, remove, or rename functions
                Do NOT change input/output handling
                Do NOT Add COMMENTS to the code but keep the ORIGINAL comment on the top of CODE
                RETURN only code no extra things like ```c code ```
                Do NOT duplicate any function definitions
                Do NOT repeat code blocks
                Output exactly one complete program

                Output Rules:
                Bug must cause incorrect output or edge-case failure
                Do NOT explain the bug
                Output ONLY the modified code
                No markdown, no backticks
                Do NOT add comments explaining the change
                CODE:
                {code}
                """,
            "A2": f"""
                Inject A2-level bugs (Semantic / Logic-Level bugs) into the following code.

                A2 Definition (Semantic Bugs):
                Bugs that preserve syntactic correctness
                Logic is locally wrong but structurally plausible
                Requires reasoning about program behavior to detect
                Algorithmic intent remains mostly intact

                Allowed Bug Types (ONLY these):
                Incorrect comparison or condition that works for common cases but fails on edge cases
                Wrong logical operator or conditional structure (e.g., weakened or strengthened condition)
                Incorrect variable update inside a loop (updating the wrong variable or at the wrong time)
                Use-before-update or update-before-use errors
                Incorrect initialization that subtly affects logic (not obvious constants)
                Returning too early or too late from a function
                Mishandling exactly one boundary case (empty input, single element, last iteration)
                Incorrect loop termination condition that still allows execution
                Incorrect but plausible invariant that produces reasonable-looking outputs
                Do NOT Add COMMENTS to the code but keep the ORIGINAL comment on the top of CODE
                RETURN only code no extra things like ```c code ```

                STRICT CONSTRAINTS:
                Inject bugs ONLY inside the problem-solving function(s)
                Do NOT modify the main() function
                main() is used strictly for test case execution and must remain correct
                Do NOT introduce syntax errors or compilation failures
                Do NOT change the overall algorithm to a different one
                Do NOT add, remove, or rename functions

                Output Rules:
                Bug must cause incorrect output or edge-case failure
                Bug should NOT be immediately obvious by inspection
                Do NOT explain the bug
                Output ONLY the modified code
                No markdown, no backticks
                Do NOT add comments explaining the change

                CODE:
                {code}
                """,
            "A3": f"""
                Inject A3-level bugs (Algorithmic / Structural bugs) into the following code.

                A3 Definition (Algorithmic Bugs):
                Bugs caused by an incorrect or incomplete algorithmic decision
                Code remains syntactically correct and structurally coherent
                Requires reasoning about the algorithm, not just local logic
                Often fails on specific input classes or scales

                Allowed Bug Types (ONLY these):
                Replace a correct algorithmic step with an incorrect or incomplete one
                Use an incorrect recurrence, invariant, or state transition
                Break optimal substructure while keeping code logically consistent
                Incorrectly reduce problem size in recursion or iteration
                Skip or mis-handle a required preprocessing step (e.g., sorting, deduplication)
                Assume an input property that does not always hold (e.g., sorted, unique, non-empty)
                Use an inappropriate data structure that preserves syntax but breaks correctness
                Introduce an algorithmic shortcut that works for small/simple cases but fails generally

                STRICT CONSTRAINTS:
                Inject bugs ONLY inside the problem-solving function(s)
                Do NOT modify the main() function
                main() is used strictly for test case execution and must remain correct
                Code must compile and run
                Do NOT introduce syntax errors or type errors
                Do NOT reduce the bug to a surface-level typo or simple condition change
                Do NOT replace the algorithm with a completely different one
                Do NOT Add COMMENTS to the code but keep the ORIGINAL comment on the top of CODE
                RETURN only code no extra things like ```c code ```

                Output Rules:
                Bug must cause incorrect results or failure on specific input classes
                Bug should not be immediately obvious by inspection
                Do NOT explain the bug
                Output ONLY the modified code
                No markdown, no backticks
                Do NOT add comments explaining the change

                CODE:
                {code}
                """,
            "A4": f"""
                Inject A4-level bugs (AI-Hallucination / Overgeneralization bugs) into the following code.

                A4 Definition (AI-Hallucination Bugs):
                Bugs that resemble confident but incorrect reasoning by large language models
                Code appears clean, reasonable, and well-structured
                Failure stems from false assumptions, overgeneralization, or misapplied patterns
                Typically passes basic or common test cases but fails on edge or adversarial inputs

                Allowed Bug Types (ONLY these):
                Assume an unstated or unjustified precondition (e.g., sorted input, non-empty array, unique elements)
                Overgeneralize from common examples while ignoring rare or corner cases
                Apply a familiar algorithmic pattern in an inappropriate context (e.g., binary search without ensuring sortedness)
                Introduce redundant or “helpful-looking” logic that subtly alters correctness
                Hard-code or partially generalize behavior based on typical training examples
                Use an incorrect default, fallback, or shortcut that works for most inputs
                Merge multiple solution strategies in a way that breaks invariants
                Simplify a condition too aggressively, removing a necessary case
                Add an unnecessary optimization that degrades correctness in corner cases

                STRICT CONSTRAINTS:
                Inject bugs ONLY inside the problem-solving function(s)
                Do NOT modify the main() function
                main() is used strictly for test case execution and must remain correct
                Code must compile and run
                Do NOT introduce syntax errors or missing symbols
                Bug should NOT be a simple typo, wrong operator, or local logic mistake
                Bug should NOT be an explicit algorithm replacement
                Do NOT Add COMMENTS to the code but keep the ORIGINAL comment on the top of CODE
                RETURN only code no extra things like ```c code ```

                Output Rules:
                Bug must appear plausible and confident
                Bug should pass common or simple test cases
                Bug should fail on edge cases or adversarial inputs
                Do NOT explain the bug
                Output ONLY the modified code
                No markdown, no backticks
                Do NOT add comments explaining the change

                CODE:
                {code}
                """,

        }
        return prompt_based_on_level[level]
    
    def _build_prompt_to_detect(self, code: str) -> str:
            return f"""
            Fix the bug in this code. Output ONLY the corrected code without any formatting, explanations, or backticks.

            RULES:
            - Output only the corrected code
            - No ``` or markdown
            - No explanations or comments
            - Code must run correctly
            - Fix only the bug, don't refactor

            Buggy code:
            {code}

            Corrected code:
            """
