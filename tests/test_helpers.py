import pytest
from app import mood_to_number, number_to_mood

def test_mood_to_number():
    assert mood_to_number('Sleepy') == 1
    assert mood_to_number('Tired') == 2
    assert mood_to_number('Okay') == 3
    assert mood_to_number('Alive') == 4
    assert mood_to_number('Energized') == 5
    assert mood_to_number('invalid') == 3  # Default case

def test_number_to_mood():
    assert number_to_mood(1) == 'Sleepy'
    assert number_to_mood(2) == 'Tired'
    assert number_to_mood(3) == 'Okay'
    assert number_to_mood(4) == 'Alive'
    assert number_to_mood(5) == 'Energized'
    assert number_to_mood(6) == 'Okay'  # Default case
    assert number_to_mood(0) == 'Okay'  # Default case
    assert number_to_mood(-1) == 'Okay'  # Default case 