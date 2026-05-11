"""Pydantic handoff schemas. Importing from here is the canonical surface."""

from matchmaker.schemas.critique import Critique, CritiqueHistory, CritiqueSeverity
from matchmaker.schemas.hypothesis import Hypothesis, RefinedHypothesis
from matchmaker.schemas.matrix import (
    DIMS,
    ConnectionCell,
    ConnectionType,
    CrossFactorialMatrix,
)
from matchmaker.schemas.prompt import ResearcherPrompt
from matchmaker.schemas.publication import (
    Publication,
    PublicationSource,
    ResearcherProfile,
)
from matchmaker.schemas.ranking import RankedHypothesis, Ranking
from matchmaker.schemas.state import PipelineState
from matchmaker.schemas.summary import (
    Dim,
    DimensionalSummary,
    ResearcherBackground,
    SummaryItem,
)

__all__ = [
    "DIMS",
    "ConnectionCell",
    "ConnectionType",
    "CrossFactorialMatrix",
    "Critique",
    "CritiqueHistory",
    "CritiqueSeverity",
    "Dim",
    "DimensionalSummary",
    "Hypothesis",
    "PipelineState",
    "Publication",
    "PublicationSource",
    "RankedHypothesis",
    "Ranking",
    "RefinedHypothesis",
    "ResearcherBackground",
    "ResearcherProfile",
    "ResearcherPrompt",
    "SummaryItem",
]
