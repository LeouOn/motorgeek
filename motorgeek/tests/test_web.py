from motorgeek.web.app import app

def test_app_exists():
    assert app is not None
    assert hasattr(app, "routes")