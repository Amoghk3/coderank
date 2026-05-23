from app.models.enums import SubmissionStatus


class VerdictClassifier:

    @staticmethod
    def classify():
        return SubmissionStatus.ACCEPTED