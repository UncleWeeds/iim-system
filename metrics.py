# metrics.py
from datetime import datetime
from typing import List, Optional
from clients.base import Incident

def parse_iso(ts: Optional[str]) -> Optional[datetime]:
    return datetime.fromisoformat(ts) if ts else None

def compute_mtta(incidents: List[Incident]) -> float:
    """Mean Time To Acknowledge: created_at → acknowledged_at."""
    deltas = []
    for inc in incidents:
        t0 = parse_iso(inc.created_at)
        t1 = parse_iso(inc.acknowledged_at)
        if t0 and t1:
            deltas.append((t1 - t0).total_seconds())
    return sum(deltas) / len(deltas) if deltas else 0.0

def compute_mtbf(incidents: List[Incident]) -> float:
    """Mean Time Between Failures: resolution of one → creation of next."""
    # sort by creation time
    sorted_incs = sorted(incidents, key=lambda i: parse_iso(i.created_at))
    intervals = []
    for prev, curr in zip(sorted_incs, sorted_incs[1:]):
        end_prev = parse_iso(prev.resolved_at)
        start_curr = parse_iso(curr.created_at)
        if end_prev and start_curr:
            intervals.append((start_curr - end_prev).total_seconds())
    return sum(intervals) / len(intervals) if intervals else 0.0

def compute_mttd(incidents: List[Incident]) -> float:
    """Mean Time To Detect: from created_at to detected_at."""
    deltas = []
    for inc in incidents:
        t0 = parse_iso(inc.created_at)
        t1 = parse_iso(inc.detected_at)
        if t0 and t1:
            deltas.append((t1 - t0).total_seconds())
    return sum(deltas) / len(deltas) if deltas else 0.0

def compute_mttr(incidents: List[Incident]) -> float:
    """Mean Time To Resolve: from detected_at to resolved_at."""
    deltas = []
    for inc in incidents:
        t1 = parse_iso(inc.detected_at)
        t2 = parse_iso(inc.resolved_at)
        if t1 and t2:
            deltas.append((t2 - t1).total_seconds())
    return sum(deltas) / len(deltas) if deltas else 0.0
