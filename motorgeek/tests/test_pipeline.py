from motorgeek.core.pipeline import DimensionRouter

def test_dimension_router_classification():
    router = DimensionRouter()
    result = router.route("0-60 in 4.2 seconds, top speed 189 mph, quarter mile 12.1s")
    assert "performance" in result