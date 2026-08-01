from adapters.sonoff_swv import SonoffSWVAdapter
def test_resolve():
    e=SonoffSWVAdapter().resolve_entities("switch.riego_huerto")
    assert e["battery"]=="sensor.riego_huerto_battery"
