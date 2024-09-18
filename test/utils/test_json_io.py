import tempfile

from wellbelog.utils.json_io import read_json, write_json, is_jsonable, check_dict_jsonable


def test_read_json():
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write('[{"name": "John", "age": 30, "city": "New York"}]')
    assert read_json(f.name) == [{'name': 'John', 'age': 30, 'city': 'New York'}]


def test_write_json():
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        write_json(f.name, [{'name': 'John', 'age': 30, 'city': 'New York'}])
    assert read_json(f.name) == [{'name': 'John', 'age': 30, 'city': 'New York'}]


def test_is_jsonable():
    json_test_pass = {'name': 'John', 'age': 30, 'city': 'New York'}
    json_test_fail = {'name': 'John', 'age': 30, 'city': 'New York', 'set': set()}
    assert is_jsonable(json_test_pass) is True
    assert is_jsonable(json_test_fail) is False


def test_check_dict_json():
    json_test = {'name': 'John', 'age': 30, 'city': 'New York', 'set': set()}
    assert check_dict_jsonable(json_test) == {'name': 'John', 'age': 30, 'city': 'New York', 'set': 'set()'}
