import importlib
from piston.PistonModule import PistonAPI

def run_tests(level, q_idx, code, language):
    module = importlib.import_module(f"tests.{level}.{q_idx+1}")
    TEST_CASES = module.TEST_CASES
    
    api = PistonAPI()
    results = []
    all_passed = True

    for t in TEST_CASES:
        result = api.execute(
            code=code,
            language=language,
            stdin=t["stdin"]
        )

        # DEBUG ONCE if needed
        # print("RAW:", result)

        # Handle compile error
        if "compile" in result and result["compile"].get("stderr"):
            all_passed = False
            results.append({
                "stdin": t["stdin"],
                "expected": t["expected"],
                "stdout": "",
                "pass": False,
                "error": "compile_error"
            })
            continue

        run = result.get("run", {})
        stdout = (run.get("stdout") or run.get("stderr") or "").strip()
        passed = stdout == t["expected"]

        if not passed:
            all_passed = False
        
        results.append({
            "stdin": t["stdin"],
            "expected": t["expected"],
            "stdout": stdout,
            "pass": passed,
        })

    return {
        "overall_pass": all_passed,
        "message": "All test cases passed" if all_passed else "One or more test cases failed",
        "results": results
    }
