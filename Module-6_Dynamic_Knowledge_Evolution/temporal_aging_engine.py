"""
Module 6: Dynamic Knowledge Evolution
File: temporal_aging_engine.py
Purpose: Engine 4 - Manage time-aware knowledge metadata, freshness decay, and historical archiving.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

try:
    from .config import Module6Config
    from .models import KnowledgeClaim, ValidityStatus
    from .utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from .exceptions import TemporalAgingError
except (ImportError, ValueError):
    from config import Module6Config
    from models import KnowledgeClaim, ValidityStatus
    from utils import logger, calculate_days_elapsed, calculate_exponential_decay
    from exceptions import TemporalAgingError


class TemporalKnowledgeAgingEngine:
    """Engine 4: Computes temporal decay, manages validity statuses, and controls historical retrieval."""

    def __init__(
        self,
        lambda_decay: float = Module6Config.LAMBDA_DECAY,
        outdated_days: float = Module6Config.OUTDATED_THRESHOLD_DAYS,
        archive_days: float = Module6Config.ARCHIVE_THRESHOLD_DAYS
    ) -> None:
        """Initialize TemporalKnowledgeAgingEngine with configurable parameters."""
        self.lambda_decay = lambda_decay
        self.outdated_days = outdated_days
        self.archive_days = archive_days
        logger.info(
            f"TemporalKnowledgeAgingEngine initialized (lambda={self.lambda_decay}, "
            f"outdated_days={self.outdated_days}, archive_days={self.archive_days})"
        )

    def evaluate_temporal_status(self, claim: KnowledgeClaim) -> Dict[str, Any]:
        """Evaluate temporal age, decay score, and updated validity status for a claim.

        Args:
            claim (KnowledgeClaim): The target claim.

        Returns:
            Dict[str, Any]: Dictionary containing days_elapsed, freshness_score, updated_status, and action_recommended.
        """
        try:
            days_elapsed = calculate_days_elapsed(claim.timestamp)
            freshness_score = calculate_exponential_decay(days_elapsed, self.lambda_decay)

            current_status = claim.validity_status
            if isinstance(current_status, str):
                try:
                    current_status = ValidityStatus(current_status)
                except ValueError:
                    current_status = ValidityStatus.ACTIVE

            recommended_status = current_status
            action_recommended = "NO_CHANGE"

            # If already superseded or archived, keep status
            if current_status not in [ValidityStatus.SUPERSEDED, ValidityStatus.ARCHIVED]:
                if days_elapsed >= self.archive_days:
                    recommended_status = ValidityStatus.ARCHIVED
                    action_recommended = "ARCHIVE"
                elif days_elapsed >= self.outdated_days:
                    recommended_status = ValidityStatus.OUTDATED
                    action_recommended = "MARK_OUTDATED"

            return {
                "claim_id": claim.id,
                "created_at": claim.timestamp,
                "days_elapsed": round(days_elapsed, 2),
                "freshness_score": round(freshness_score, 4),
                "current_status": current_status.value if isinstance(current_status, ValidityStatus) else str(current_status),
                "recommended_status": recommended_status.value if isinstance(recommended_status, ValidityStatus) else str(recommended_status),
                "action_recommended": action_recommended
            }
        except Exception as e:
            logger.error(f"Temporal aging evaluation error for claim {claim.id}: {e}")
            raise TemporalAgingError(f"Temporal aging calculation failed: {e}") from e

    def apply_temporal_decay_to_items(
        self,
        items: List[Dict[str, Any]],
        include_historical: bool = False
    ) -> List[Dict[str, Any]]:
        """Filter and adjust retrieval scores of items based on temporal freshness.

        Args:
            items (List[Dict[str, Any]]): List of retrieval items with timestamps/metadata.
            include_historical (bool): Whether to include superseded/archived historical items.

        Returns:
            List[Dict[str, Any]]: Processed list of items with freshness scores and optional filtering.
        """
        processed_items = []
        for item in items:
            meta = item.get("metadata", {})
            ts = meta.get("timestamp") or meta.get("created_at") or item.get("timestamp")
            status = meta.get("validity_status") or item.get("validity_status") or "ACTIVE"

            if not include_historical and status in ["ARCHIVED", "SUPERSEDED"]:
                continue

            days = calculate_days_elapsed(str(ts)) if ts else 0.0
            freshness = calculate_exponential_decay(days, self.lambda_decay)

            # Copy item and update scores/metadata
            item_copy = dict(item)
            item_copy["freshness_score"] = round(freshness, 4)
            item_copy["days_old"] = round(days, 1)
            item_copy["validity_status"] = status
            processed_items.append(item_copy)

        return processed_items
