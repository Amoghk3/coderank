from unittest.mock import MagicMock, AsyncMock, patch

from app.models.enums import (
    SubmissionStatus,
    ExecutionJobStatus,
)

from app.workers.execution_worker import (
    execute_submission_task,
)


@patch(
    "app.workers.execution_worker.asyncio.run"
)
@patch(
    "app.workers.execution_worker.manager.send_submission_update"
)
@patch(
    "app.workers.execution_worker.VerdictClassifier.classify"
)
@patch(
    "app.workers.execution_worker.VerdictClassifier.compare_outputs"
)
@patch(
    "app.workers.execution_worker.DockerRunner.run_code"
)
@patch(
    "app.workers.execution_worker.SessionLocal"
)
def test_accepted_submission(
    mock_session_local,
    mock_run_code,
    mock_compare_outputs,
    mock_classify,
    mock_send_update,
    mock_asyncio_run,
):
    db = MagicMock()

    mock_session_local.return_value = db

    execution_job = MagicMock()
    execution_job.submission_id = "submission-1"

    submission = MagicMock()
    submission.id = "submission-1"
    submission.user_id = "user-1"
    submission.problem_id = "problem-1"
    submission.language_id = "lang-1"
    submission.source_code = "print('0 1')"
    submission.is_judge = True

    leaderboard = MagicMock()
    leaderboard.accepted_count = 0
    leaderboard.total_submissions = 0
    leaderboard.total_score = 0
    leaderboard.best_runtime_ms = None

    language = MagicMock()
    language.name = "Python"

    testcase = MagicMock()
    testcase.id = "tc-1"
    testcase.input_data = "2 7 11 15\n9"
    testcase.expected_output = "0 1"

    query = MagicMock()

    query.filter.return_value = query

    query.first.side_effect = [
        execution_job,   # ExecutionJob
        submission,      # Submission
        leaderboard,     # Leaderboard
        language,        # Language
        leaderboard,     # Leaderboard again
        None,            # SolvedProblem
    ]

    query.all.return_value = [
        testcase
    ]

    db.query.return_value = query

    mock_run_code.return_value = {
        "stdout": "0 1",
        "stderr": "",
        "exit_code": 0,
        "timeout": False,
    }

    mock_compare_outputs.return_value = True

    mock_classify.return_value = (
        SubmissionStatus.ACCEPTED
    )

    execute_submission_task(
        "job-1"
    )

    assert (
        submission.status
        ==
        SubmissionStatus.ACCEPTED
    )

    assert (
        execution_job.status
        ==
        ExecutionJobStatus.SUCCESS
    )

    assert (
        leaderboard.accepted_count
        ==
        1
    )

    assert (
        leaderboard.total_score
        ==
        100
    )

    assert (
        submission.runtime_ms
        ==
        120
    )

    assert (
        submission.memory_kb
        ==
        2048
    )

@patch(
    "app.workers.execution_worker.asyncio.run"
)
@patch(
    "app.workers.execution_worker.manager.send_submission_update",
    new_callable=AsyncMock,
)
@patch(
    "app.workers.execution_worker.DockerRunner.run_code"
)
@patch(
    "app.workers.execution_worker.SessionLocal"
)
def test_runtime_error_submission(
    mock_session_local,
    mock_run_code,
    mock_send_update,
    mock_asyncio_run,
):
    db = MagicMock()

    mock_session_local.return_value = db

    execution_job = MagicMock()
    execution_job.submission_id = "submission-1"

    submission = MagicMock()
    submission.id = "submission-1"
    submission.problem_id = "problem-1"
    submission.language_id = "lang-1"
    submission.is_judge = False

    language = MagicMock()
    language.name = "Python"

    testcase = MagicMock()

    query = MagicMock()

    query.filter.return_value = query

    query.first.side_effect = [
        execution_job,
        submission,
        language,
    ]

    query.all.return_value = [
        testcase
    ]

    db.query.return_value = query

    mock_run_code.return_value = {
        "stdout": "",
        "stderr": "NameError",
        "exit_code": 1,
        "timeout": False,
    }

    execute_submission_task(
        "job-1"
    )

    assert (
        submission.status
        ==
        SubmissionStatus.RUNTIME_ERROR
    )

@patch(
    "app.workers.execution_worker.asyncio.run"
)
@patch(
    "app.workers.execution_worker.manager.send_submission_update",
    new_callable=AsyncMock,
)
@patch(
    "app.workers.execution_worker.DockerRunner.run_code"
)
@patch(
    "app.workers.execution_worker.SessionLocal"
)
def test_timeout_submission(
    mock_session_local,
    mock_run_code,
    mock_send_update,
    mock_asyncio_run,
):
    db = MagicMock()

    mock_session_local.return_value = db

    execution_job = MagicMock()
    execution_job.submission_id = "submission-1"

    submission = MagicMock()
    submission.id = "submission-1"
    submission.problem_id = "problem-1"
    submission.language_id = "lang-1"
    submission.is_judge = False

    language = MagicMock()
    language.name = "Python"

    testcase = MagicMock()

    query = MagicMock()

    query.filter.return_value = query

    query.first.side_effect = [
        execution_job,
        submission,
        language,
    ]

    query.all.return_value = [
        testcase
    ]

    db.query.return_value = query

    mock_run_code.return_value = {
        "stdout": "",
        "stderr": "",
        "exit_code": 0,
        "timeout": True,
    }

    execute_submission_task(
        "job-1"
    )

    assert (
        submission.status
        ==
        SubmissionStatus.TIME_LIMIT_EXCEEDED
    )

@patch(
    "app.workers.execution_worker.asyncio.run"
)
@patch(
    "app.workers.execution_worker.manager.send_submission_update",
    new_callable=AsyncMock,
)
@patch(
    "app.workers.execution_worker.VerdictClassifier.classify"
)
@patch(
    "app.workers.execution_worker.VerdictClassifier.compare_outputs"
)
@patch(
    "app.workers.execution_worker.DockerRunner.run_code"
)
@patch(
    "app.workers.execution_worker.SessionLocal"
)
def test_wrong_answer_submission(
    mock_session_local,
    mock_run_code,
    mock_compare,
    mock_classify,
    mock_send_update,
    mock_asyncio_run,
):
    db = MagicMock()

    mock_session_local.return_value = db

    execution_job = MagicMock()
    execution_job.submission_id = "submission-1"

    submission = MagicMock()
    submission.id = "submission-1"
    submission.problem_id = "problem-1"
    submission.language_id = "lang-1"
    submission.is_judge = False

    language = MagicMock()
    language.name = "Python"

    testcase = MagicMock()

    query = MagicMock()

    query.filter.return_value = query

    query.first.side_effect = [
        execution_job,
        submission,
        language,
    ]

    query.all.return_value = [
        testcase
    ]

    db.query.return_value = query

    mock_run_code.return_value = {
        "stdout": "999",
        "stderr": "",
        "exit_code": 0,
        "timeout": False,
    }

    mock_compare.return_value = False

    mock_classify.return_value = (
        SubmissionStatus.WRONG_ANSWER
    )

    execute_submission_task(
        "job-1"
    )

    assert (
        submission.status
        ==
        SubmissionStatus.WRONG_ANSWER
    )