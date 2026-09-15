class FixValidator:
    def validate(
        self,
        test_result: dict[str, object],
        patch: str,
    ) -> dict[str, object]:
        tests_passed = bool(
            test_result.get("success", False)
        )

        patch_generated = bool(
            patch.strip()
        )

        if tests_passed and patch_generated:
            status = "validated"
        elif not patch_generated:
            status = "no_patch"
        else:
            status = "failed"

        return {
            "status": status,
            "tests_passed": tests_passed,
            "patch_generated": patch_generated,
            "test_output": test_result.get(
                "output",
                "",
            ),
        }