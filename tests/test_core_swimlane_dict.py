from swimlane.core import SwimlaneDict


D = {
    "one": 1,
    "two": 2,
    "values": {
        "four": 4,
        "five": 5,
        "$type": "GARBAGE",
        "six": {
            "seven": 7,
            "$type": "MOREGARBAGE",
            "eight": 8,
            "nine": {
                "ten": 10,
                "$type": "EVENMOREGARBAGE"
            }
        }
    },
    "$type": "TOPLEVELGARBAGE"
}

def test_swimlane_dict():
    sd = SwimlaneDict(D)
    assert ("$type", "TOPLEVELGARBAGE") == sd.popitem(last=False)
    assert ("$type", "GARBAGE") == sd["values"].popitem(last=False)
    assert ("$type", "MOREGARBAGE") == sd["values"]["six"].popitem(last=False)
    assert ("$type", "EVENMOREGARBAGE") == sd["values"]["six"]["nine"].popitem(last=False)
