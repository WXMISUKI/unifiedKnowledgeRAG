import json
from datetime import UTC, datetime
from pathlib import Path

from app.config import Settings
from app.models.contracts import IndexLifecycleJob, IndexStatusResponse


class IndexLifecycleStore:
    def __init__(self, settings: Settings):
        self.root = settings.rag_index_dir
        self.jobs_path = self.root / "jobs.jsonl"
        self.sources_path = self.root / "sources.json"

    def append_job(self, job: IndexLifecycleJob) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        with self.jobs_path.open("a", encoding="utf-8") as file:
            file.write(job.model_dump_json(exclude_none=True))
            file.write("\n")

    def read_jobs(self) -> list[IndexLifecycleJob]:
        if not self.jobs_path.exists():
            return []

        jobs: list[IndexLifecycleJob] = []
        for line in self.jobs_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                jobs.append(IndexLifecycleJob.model_validate_json(line))
        return jobs

    def list_jobs(
        self,
        source_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[IndexLifecycleJob]:
        jobs = self.list_latest_jobs(source_id=source_id, status=status)
        return jobs[offset:offset + limit]

    def count_jobs(
        self,
        source_id: str | None = None,
        status: str | None = None,
    ) -> int:
        return len(self.list_latest_jobs(source_id=source_id, status=status))

    def list_latest_jobs(
        self,
        source_id: str | None = None,
        status: str | None = None,
    ) -> list[IndexLifecycleJob]:
        latest_by_id: dict[str, IndexLifecycleJob] = {}
        for job in self.read_jobs():
            latest_by_id[job.job_id] = job

        jobs = sorted(
            latest_by_id.values(),
            key=lambda job: job.requested_at,
            reverse=True,
        )
        if source_id is not None:
            jobs = [job for job in jobs if job.source_id == source_id]
        if status is not None:
            jobs = [job for job in jobs if job.status == status]
        return jobs

    def get_job(self, job_id: str) -> IndexLifecycleJob | None:
        return next(
            (job for job in reversed(self.read_jobs()) if job.job_id == job_id),
            None,
        )

    def latest_job_for_source(self, source_id: str) -> IndexLifecycleJob | None:
        return next(
            (
                job
                for job in self.list_latest_jobs()
                if job.source_id == source_id
            ),
            None,
        )

    def compact_jobs(self, keep_latest: int) -> tuple[int, int, int]:
        before_count = len(self.list_latest_jobs())
        kept_jobs = self.list_latest_jobs()[:keep_latest]
        self._atomic_write_jsonl(self.jobs_path, kept_jobs)
        after_count = len(kept_jobs)
        return before_count, after_count, max(before_count - after_count, 0)

    def stale_running_jobs(self, max_age_seconds: int, now: datetime | None = None) -> list[IndexLifecycleJob]:
        now = now or datetime.now(UTC)
        stale_jobs: list[IndexLifecycleJob] = []
        for job in self.list_latest_jobs(status="running"):
            requested_at = _parse_timestamp(job.requested_at)
            if (now - requested_at).total_seconds() >= max_age_seconds:
                stale_jobs.append(job)
        return stale_jobs

    def write_source_status(self, status: IndexStatusResponse) -> None:
        sources = self.read_source_statuses()
        sources[status.source_id] = status
        payload = {
            source_id: source_status.model_dump(exclude_none=True)
            for source_id, source_status in sorted(sources.items())
        }
        self._atomic_write_json(self.sources_path, payload)

    def read_source_status(self, source_id: str) -> IndexStatusResponse | None:
        return self.read_source_statuses().get(source_id)

    def read_source_statuses(self) -> dict[str, IndexStatusResponse]:
        if not self.sources_path.exists():
            return {}
        payload = json.loads(self.sources_path.read_text(encoding="utf-8"))
        return {
            source_id: IndexStatusResponse.model_validate(source_status)
            for source_id, source_status in payload.items()
        }

    def clear_for_tests(self) -> None:
        if self.jobs_path.exists():
            self.jobs_path.unlink()
        if self.sources_path.exists():
            self.sources_path.unlink()

    def _atomic_write_json(self, path: Path, payload: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        tmp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp_path.replace(path)

    def _atomic_write_jsonl(self, path: Path, jobs: list[IndexLifecycleJob]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        tmp_path = path.with_suffix(f"{path.suffix}.tmp")
        tmp_path.write_text(
            "".join(f"{job.model_dump_json(exclude_none=True)}\n" for job in jobs),
            encoding="utf-8",
        )
        tmp_path.replace(path)


def _parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)
