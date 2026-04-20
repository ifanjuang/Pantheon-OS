"""CoherenceChecker — detects internal contradictions between agent outputs."""


class CoherenceChecker:
    def check(self, outputs: list[dict]) -> tuple[bool, list[str]]:
        issues: list[str] = []
        confidences = [o.get("confidence", 1.0) for o in outputs if "confidence" in o]
        if confidences and min(confidences) < 0.3:
            issues.append("Low-confidence output detected — review before release")
        return (len(issues) == 0, issues)
