from app.analytics import (
    get_total_revenue,
    get_top_product,
    get_monthly_revenue,
    get_top_region,
    compare_months
)


def test_total_revenue():
    assert get_total_revenue() == 1439200.0


def test_top_product():
    result = get_top_product()

    assert result["product"] == "Monitor"
    assert result["revenue"] == 473000.0


def test_monthly_revenue():
    result = get_monthly_revenue()

    assert len(result) == 6
    assert result[0]["month"] == "01-2026"
    assert result[0]["revenue"] == 210250.0


def test_top_region():
    result = get_top_region()

    assert result["region"] == "South"
    assert result["revenue"] == 411200.0


def test_compare_months():
    result = compare_months("01-2026", "02-2026")

    assert result["revenue1"] == 210250.0
    assert result["revenue2"] == 234600.0
    assert result["difference"] == 24350.0
