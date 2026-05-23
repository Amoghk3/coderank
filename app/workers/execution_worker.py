import time

from app.core.logging import logger

from app.core.sync_database import (
    SessionLocal,
)

from app.models.enums import (
    SubmissionStatus,
)

from app.models.submission import Submission

from app.workers.celery_app import (
    celery_app,
)


@celery_app.task
def execute_submission_task(
    submission_id: str,
):
    logger.info(
        f"Executing submission={submission_id}"
    )

    db = SessionLocal()

    try:

        submission = (
            db.query(Submission)
            .filter(
                Submission.id == submission_id
            )
            .first()
        )

        if not submission:
            logger.error(
                f"Submission not found={submission_id}"
            )

            return

        submission.status = (
            SubmissionStatus.RUNNING
        )

        db.commit()

        time.sleep(3)

        submission.status = (
            SubmissionStatus.ACCEPTED
        )

        submission.runtime_ms = 120
        submission.memory_kb = 2048

        db.commit()

        logger.info(
            f"Completed submission={submission_id}"
        )

    except Exception as e:

        logger.exception(
            f"Execution failed={str(e)}"
        )

        if submission:

            submission.status = (
                SubmissionStatus.FAILED
            )

            db.commit()

    finally:
        db.close()