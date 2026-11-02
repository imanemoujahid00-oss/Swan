"""Draft questionnaire contract based on Loredana's exploration.

These checks define the demonstration's scope. They are not clinical triage.
The team must review this contract before connecting a real recommender.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    is_adult: bool
    concern: str
    blemish_level: int | None
    referral_flags: tuple[str, ...]
    skin_type: str
    reactivity: str
    avoid: tuple[str, ...]


def preview_route(profile: Profile) -> str:
    """Return a demo screen, never a diagnosis or suitability verdict."""
    if not profile.is_adult:
        return "outside_scope"
    if profile.concern in {"dryness_barrier", "sensitivity"}:
        return "coming_soon"
    if profile.concern != "acne_prone":
        return "outside_scope"
    if profile.referral_flags:
        return "professional_guidance"
    return "results"
