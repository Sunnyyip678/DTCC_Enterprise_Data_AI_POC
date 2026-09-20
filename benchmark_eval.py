results = []
for test_case in gold_dataset:
    ai_output = run_ai_model(test_case["input"])
    results.append(
        {"expected": test_case["expected_output"], "actual": ai_output}
    )
