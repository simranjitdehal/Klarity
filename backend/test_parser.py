from parser import parse_log
from models import ParsedLog


def test_normal_log():
    result = parse_log("ERROR database not failed")
    assert result == ParsedLog(level="ERROR", message="database not failed")


def test_single_word_log():
    result = parse_log("INFO")
    assert result == ParsedLog(level="INFO", message="")


def test_empty_log():
    result = parse_log("")
    assert result == ParsedLog(level="UNKNOWN", message="")
