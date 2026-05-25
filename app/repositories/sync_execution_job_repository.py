from app.models.execution_job import (
    ExecutionJob,
)


class SyncExecutionJobRepository:

    @staticmethod
    def get_by_id(
        db,
        execution_job_id: str,
    ):
        return (
            db.query(ExecutionJob)
            .filter(
                ExecutionJob.id == execution_job_id
            )
            .first()
        )

    @staticmethod
    def update(
        db,
        execution_job: ExecutionJob,
    ):
        db.commit()
        db.refresh(execution_job)

        return execution_job