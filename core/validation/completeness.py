"""CompletenessChecker — validates that required fields are present in a result."""


class CompletenessChecker:
    REQUIRED_FIELDS = ["answer", "sources", "confidence"]

    def check(self, result: dict) -> tuple[bool, list[str]]:
        missing = [f for f in self.REQUIRED_FIELDS if not result.get(f)]
        return (len(missing) == 0, missing)
