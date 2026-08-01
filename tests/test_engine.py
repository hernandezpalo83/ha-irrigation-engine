from src.engine.engine import Engine

def test_start():
 assert Engine().start("huerto",10)["event"]=="start"
