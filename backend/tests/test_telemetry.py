def test_telemetry_disabled_in_tests(monkeypatch):
    import threading

    import app.telemetry as t

    monkeypatch.setenv("TELEMETRY_DISABLED", "1")
    before = threading.active_count()
    t.start_telemetry()
    assert threading.active_count() == before
