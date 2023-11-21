import pytest, os, sys, re, logging
from pytest import MonkeyPatch


PROJECT_FOLDER = os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
            )
        )

sys.path.append(PROJECT_FOLDER)
    

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
TESTFILE_LOCATION = PROJECT_FOLDER + "/tests/inputs"



import main

def replace_input_and_run(test_input: str, func, args):
    test_input = re.split("[ \n]", test_input)
    monkeypatch = MonkeyPatch()

    def input_generator(test_input):
        for i in test_input:
            yield i

    gen = input_generator(test_input)
    monkeypatch.setattr("builtins.input", lambda: next(gen))
    ret = func(*args)
    monkeypatch.undo()
    return ret

def get_test_file(name):
    with open(TESTFILE_LOCATION + "/" + name, "r") as f:
        return f.read()



# В коде мы используем рандомизатор для получения вопросов.
# Чтобы вопрос всегда был один и тот же я заменил функцию выдающую случайные вопросы
@pytest.fixture()
def freeze_sample():
    monkeypatch = MonkeyPatch()
    monkeypatch.setattr(
                "random.sample", lambda lst, count: [
                {
                    "name": "Text question",
                    "text": "Choose",
                    "options": ["1.0", "0.0"],
                    "coefficients": [1.0, 0.0]
                } 
                for _ in range(count)])
    yield None
    monkeypatch.undo()


# TESTS START HERE


def test_checkTruth():
    ret = main.is_it_truth(12, 60, 5, 2)
    assert ret == True
    ret = main.is_it_truth(11, 59, 5, 2)
    assert ret == False
    ret = main.is_it_truth(12, 60, 4, 1)
    assert ret == False
    ret = main.is_it_truth(0, 0, 5, 2)
    assert ret == False

def test_check_input0():
    test_input = "1 2 7 4"
    try:
        ret = replace_input_and_run(test_input, main.get_int, (3, 6))
    except StopIteration:
        assert False
    assert ret == 4

def test_check_input1():
    test_input = "1 2 -3 -10"
    try:
        ret = replace_input_and_run(test_input, main.get_int, (-10, -4))
    except StopIteration:
        assert False
    assert ret == -10


def test_whole_program0(freeze_sample):
    """Check if programm work at all"""
    excpected = "He is not a robot"
    test_input = get_test_file("test0")
    ret = replace_input_and_run(test_input, main.print_survay, (PROJECT_FOLDER + "/questions.json", True))
    assert ret == excpected

def test_whole_program1(freeze_sample):
    excpected = "He is not a robot"
    test_input = get_test_file("test1")
    ret = replace_input_and_run(test_input, main.print_survay, (PROJECT_FOLDER + "/questions.json", False))
    assert ret == excpected

def test_whole_program2(freeze_sample):    
    excpected = "He is a robot"
    test_input = get_test_file("test2")
    ret = replace_input_and_run(test_input, main.print_survay, (PROJECT_FOLDER + "/questions.json", True))
    assert ret == excpected

def test_whole_program3(freeze_sample):    
    excpected = "He is not a robot"
    test_input = get_test_file("test3")
    ret = replace_input_and_run(test_input, main.print_survay, (PROJECT_FOLDER + "/questions.json", True))
    assert ret == excpected

def test_whole_program4(freeze_sample):
    """First 3 answer state he is a human,
    Next 3 answer is a lie (has 2 or more incorrect health state)
    Next 3 answer state he is a robot"""  
    excpected = "He is not a robot"
    test_input = get_test_file("test4")
    ret = replace_input_and_run(test_input, main.print_survay, (PROJECT_FOLDER + "/questions.json", True))
    assert ret == excpected
