from app.interaction.views import get_rxcui


def test_rxcui():
    """Test if an rxcui is returned given the medication name"""

    result1 = get_rxcui("Lisinopril(Oral Pill)")
    result2 = get_rxcui("Lithium carbonate XR (Oral Pill)")

    assert isinstance(result1, str)
    assert isinstance(result2, str)