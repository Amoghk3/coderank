from prometheus_client import Counter
from prometheus_client import Histogram


submission_counter = Counter(
    "submission_total",
    "Total submissions processed",
)

accepted_counter = Counter(
    "accepted_total",
    "Accepted submissions",
)

execution_time_histogram = Histogram(
    "execution_runtime_seconds",
    "Execution runtime distribution",
)