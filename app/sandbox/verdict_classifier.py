from app.models.enums import (
    SubmissionStatus,
)


class VerdictClassifier:

    @staticmethod
    def normalize_output(
        output: str,
    ):
        return output.strip()

    @classmethod
    def compare_outputs(
        cls,
        expected: str,
        actual: str,
    ):
        return (
            cls.normalize_output(expected)
            ==
            cls.normalize_output(actual)
        )

    @classmethod
    def classify(
        cls,
        passed: bool,
    ):
        if passed:
            return SubmissionStatus.ACCEPTED

        return SubmissionStatus.WRONG_ANSWER