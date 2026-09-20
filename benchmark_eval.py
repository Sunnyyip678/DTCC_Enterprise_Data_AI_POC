import json

# 1. 黄金数据集 (Gold Dataset / Benchmark)
# 包含真实的输入案例、预期的正确输出以及边界校验数据
gold_dataset = [
    {
        "case_id": "TC-001",
        "input_trade": "Trade ID: TXN1001, Amount: $150,000.00, Status: Pending",
        "expected_status": "MATCH",
        "expected_amount": 150000.0,
    },
    {
        "case_id": "TC-002",
        "input_trade": "Trade ID: TXN1002, Amount: -$5,000.00, Status: Break",
        "expected_status": "BREAK",
        "expected_amount": 5000.0,
    },
    {
        "case_id": "TC-003",
        "input_trade": "Trade ID: TXN1003, Amount: Null, Status: Unknown",
        "expected_status": "EXCEPTION",
        "expected_amount": 0.0,
    },
]


# 2. 确定性硬规则护栏 (Deterministic Guardrails)
def apply_guardrails(ai_output):
    """在把 AI 输出呈现给用户前，执行 Python 级别的格式与数值合法性校验。"""
    if not isinstance(ai_output, dict):
        return False, "Output Format Error: Expected JSON/Dict"

    # 护栏规则 1：必须包含核心业务状态字段
    if "status" not in ai_output:
        return False, "Missing Status Field"

    # 护栏规则 2：金额不能为负数（金融合理性检查）
    if ai_output.get("amount", 0) < 0:
        return False, "Financial Logic Violation: Negative Amount"

    return True, "Guardrail Passed"


# 3. 评估指标计算与自动化 Benchmark 流程
def run_benchmark():
    passed_guardrails_count = 0
    exact_matches_count = 0
    total_cases = len(gold_dataset)

    print("=== Starting AI Evaluation against Gold Dataset ===\n")

    for case in gold_dataset:
        # 模拟 AI 模型的推理输出 (POC 阶段示例数据)
        # 在实际 API 接通后，此处替换为真实模型调用方法
        mock_ai_response = {
            "status": case["expected_status"],
            "amount": abs(case["expected_amount"]),
        }

        # 运行硬规则校验 (Guardrail Check)
        is_safe, msg = apply_guardrails(mock_ai_response)
        if is_safe:
            passed_guardrails_count += 1

        # 计算准确率 (Exact Match Metric)
        if mock_ai_response.get("status") == case["expected_status"]:
            exact_matches_count += 1

        print(
            f"[{case['case_id']}] Guardrail: {msg} | Match: {mock_ai_response.get('status') == case['expected_status']}"
        )

    # 4. 汇总展示核心评估结果 (Evaluation Metrics)
    guardrail_pass_rate = (passed_guardrails_count / total_cases) * 100
    accuracy_rate = (exact_matches_count / total_cases) * 100

    print("\n=== Final Benchmark Summary ===")
    print(f"Total Test Cases Evaluated: {total_cases}")
    print(f"Guardrail Pass Rate:        {guardrail_pass_rate:.1f}%")
    print(f"Accuracy (Exact Match):      {accuracy_rate:.1f}%")


if __name__ == "__main__":
    run_benchmark()
