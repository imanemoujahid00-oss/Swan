"""Fictional layout fixtures. No catalogue, ingredient or ranking claims."""

from dataclasses import dataclass

from swan_ui.profile import Profile


@dataclass(frozen=True)
class ProductPreview:
    product_id: str
    name: str
    description: str


def get_mock_results(profile: Profile) -> tuple[ProductPreview, ...]:
    """Replace this adapter once the team approves the catalogue and ranker.

    The profile is accepted to establish the integration boundary. Fixtures
    deliberately remain identical for every profile: no personalization exists.
    """
    return (
        ProductPreview("demo-a", "Example moisturizer A", "A placeholder for a reviewed catalogue product."),
        ProductPreview("demo-b", "Example moisturizer B", "A second placeholder to compare the results layout."),
        ProductPreview("demo-c", "Example moisturizer C", "A third placeholder for the future recommendation list."),
    )
