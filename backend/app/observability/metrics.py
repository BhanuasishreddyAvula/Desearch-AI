"""Lightweight in-memory metric collector interface."""

from collections import defaultdict
from typing import Any


class MetricsCollector:
    """In-memory metrics collector storing counters, durations, and gauges."""

    def __init__(self) -> None:
        self._counters: dict[str, int] = defaultdict(int)
        self._durations: dict[str, list[float]] = defaultdict(list)
        self._gauges: dict[str, float] = {}

    def increment_counter(
        self, name: str, value: int = 1, labels: dict[str, str] | None = None
    ) -> None:
        """Increment a counter metric."""
        key = self._format_key(name, labels)
        self._counters[key] += value

    def record_duration(
        self,
        name: str,
        duration_ms: float,
        labels: dict[str, str] | None = None,
    ) -> None:
        """Record execution duration metric in milliseconds."""
        key = self._format_key(name, labels)
        self._durations[key].append(duration_ms)

    def record_gauge(self, name: str, value: float, labels: dict[str, str] | None = None) -> None:
        """Record a gauge value metric."""
        key = self._format_key(name, labels)
        self._gauges[key] = value

    def _format_key(self, name: str, labels: dict[str, str] | None = None) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_metrics_summary(self) -> dict[str, Any]:
        """Return a snapshot dictionary summary of all recorded metrics."""
        summary: dict[str, Any] = {
            "counters": dict(self._counters),
            "gauges": dict(self._gauges),
            "durations": {},
        }
        for key, values in self._durations.items():
            if values:
                summary["durations"][key] = {
                    "count": len(values),
                    "total_ms": round(sum(values), 2),
                    "avg_ms": round(sum(values) / len(values), 2),
                    "max_ms": round(max(values), 2),
                    "min_ms": round(min(values), 2),
                }
        return summary


metrics = MetricsCollector()
