from datetime import (
    datetime,
    UTC,
)

from app.core.logging import logger

from app.core.sync_database import (
    SessionLocal,
)

from app.core.metrics import (
    submission_counter,
    accepted_counter,
    execution_time_histogram,
)

from app.models.enums import (
    SubmissionStatus,
    ExecutionJobStatus,
)

from app.models.execution_job import (
    ExecutionJob,
)

from app.models.execution_result import (
    ExecutionResult,
)

from app.models.judge_case_result import (
    JudgeCaseResult,
)

from app.models.leaderboard import (
    Leaderboard,
)

from app.models.solved_problem import (
    SolvedProblem,
)

from app.models.submission import (
    Submission,
)

from app.models.test_case import (
    TestCase,
)

from app.sandbox.docker_runner import (
    DockerRunner,
)

from app.sandbox.verdict_classifier import (
    VerdictClassifier,
)

from app.workers.celery_app import (
    celery_app,
)
import asyncio
from app.core.websocket_manager import (
    manager,
)


@celery_app.task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_kwargs={"max_retries": 3},
)
def execute_submission_task(
    execution_job_id: str,
):

    logger.info(
        f"Starting execution job={execution_job_id}"
    )

    db = SessionLocal()

    execution_job = None

    try:

        submission_counter.inc()

        execution_job = (
            db.query(ExecutionJob)
            .filter(
                ExecutionJob.id
                == execution_job_id
            )
            .first()
        )

        if not execution_job:

            logger.error(
                "Execution job not found"
            )

            return

        submission = (
            db.query(Submission)
            .filter(
                Submission.id
                == execution_job.submission_id
            )
            .first()
        )

        if not submission:

            logger.error(
                "Submission not found"
            )

            execution_job.status = (
                ExecutionJobStatus.FAILED
            )

            execution_job.error_message = (
                "Submission missing"
            )

            db.commit()

            return

        execution_job.status = (
            ExecutionJobStatus.RUNNING
        )

        execution_job.started_at = (
            datetime.now(UTC)
        )

        submission.status = (
            SubmissionStatus.RUNNING
        )

        asyncio.run(
            manager.send_submission_update(
                str(submission.id),

                {
                    "status": "RUNNING",
                },
            )
        )

        db.commit()

        if submission.is_judge:

            leaderboard = (
                db.query(Leaderboard)
                .filter(
                    Leaderboard.user_id
                    == submission.user_id
                )
                .first()
            )

            if not leaderboard:

                leaderboard = Leaderboard(
                    user_id=submission.user_id,
                    accepted_count=0,
                    total_submissions=0,
                    total_score=0,
                    best_runtime_ms=None,
                )

                db.add(leaderboard)

            leaderboard.total_submissions += 1

            db.commit()

        query = (
            db.query(TestCase)
            .filter(
                TestCase.problem_id
                == submission.problem_id
            )
        )

        if not submission.is_judge:

            query = query.filter(
                TestCase.is_hidden == False
            )

        test_cases = query.all()

        all_passed = True

        for test_case in test_cases:

            with execution_time_histogram.time():

                result = DockerRunner.run_code(
                    language_name=(
                        submission.language.name
                    ),
                    source_code=(
                        submission.source_code
                    ),
                    stdin_input=(
                        test_case.input_data
                    ),
                )

            execution_result = ExecutionResult(
                submission_id=submission.id,

                stdout=result["stdout"],

                stderr=result["stderr"],
            )

            db.add(execution_result)

            if result["timeout"]:

                submission.status = (
                    SubmissionStatus
                    .TIME_LIMIT_EXCEEDED
                )

                all_passed = False

                judge_result = JudgeCaseResult(
                    submission_id=submission.id,

                    test_case_id=test_case.id,

                    expected_output=(
                        test_case.expected_output
                    ),

                    actual_output="",

                    passed=False,
                )

                db.add(judge_result)

                break

            if result["exit_code"] != 0:

                submission.status = (
                    SubmissionStatus
                    .RUNTIME_ERROR
                )

                all_passed = False

                judge_result = JudgeCaseResult(
                    submission_id=submission.id,

                    test_case_id=test_case.id,

                    expected_output=(
                        test_case.expected_output
                    ),

                    actual_output=(
                        result["stderr"]
                    ),

                    passed=False,
                )

                db.add(judge_result)

                break

            actual_output = (
                result["stdout"]
            )

            passed = (
                VerdictClassifier.compare_outputs(
                    test_case.expected_output,
                    actual_output,
                )
            )

            judge_result = JudgeCaseResult(
                submission_id=submission.id,

                test_case_id=test_case.id,

                expected_output=(
                    test_case.expected_output
                ),

                actual_output=actual_output,

                passed=passed,
            )

            db.add(judge_result)

            if not passed:

                all_passed = False

        db.commit()

        if submission.status not in [

            SubmissionStatus.RUNTIME_ERROR,

            SubmissionStatus
            .TIME_LIMIT_EXCEEDED,
        ]:

            submission.status = (
                VerdictClassifier.classify(
                    all_passed
                )
            )

        submission.runtime_ms = 120

        submission.memory_kb = 2048

        if (
            submission.is_judge
            and
            submission.status
            == SubmissionStatus.ACCEPTED
        ):

            accepted_counter.inc()

            leaderboard = (
                db.query(Leaderboard)
                .filter(
                    Leaderboard.user_id
                    == submission.user_id
                )
                .first()
            )

            existing_solve = (
                db.query(SolvedProblem)
                .filter(
                    SolvedProblem.user_id
                    == submission.user_id,

                    SolvedProblem.problem_id
                    == submission.problem_id,
                )
                .first()
            )

            if not existing_solve:

                solved_problem = SolvedProblem(
                    user_id=submission.user_id,

                    problem_id=submission.problem_id,

                    first_submission_id=(
                        submission.id
                    ),
                )

                db.add(solved_problem)

                leaderboard.accepted_count += 1

                leaderboard.total_score += 100

            if (
                leaderboard.best_runtime_ms
                is None
                or
                submission.runtime_ms
                <
                leaderboard.best_runtime_ms
            ):

                leaderboard.best_runtime_ms = (
                    submission.runtime_ms
                )

        execution_job.status = (
            ExecutionJobStatus.SUCCESS
        )

        execution_job.completed_at = (
            datetime.now(UTC)
        )

        db.commit()

        logger.info(
            f"Execution completed job={execution_job_id}"
        )

    except Exception as e:

        logger.exception(
            f"Execution failed={str(e)}"
        )

        if execution_job:

            execution_job.status = (
                ExecutionJobStatus.FAILED
            )

            execution_job.error_message = str(e)

            execution_job.completed_at = (
                datetime.now(UTC)
            )

            asyncio.run(
                manager.send_submission_update(
                    str(submission.id),

                    {
                        "status": (
                            submission.status
                        ),

                        "runtime_ms": (
                            submission.runtime_ms
                        ),

                        "memory_kb": (
                            submission.memory_kb
                        ),
                    },
                )
            )

            db.commit()

        raise

    finally:

        db.close()