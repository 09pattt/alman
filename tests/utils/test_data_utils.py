import pytest
from alman.utils import data_utils

@pytest.mark.parametrize('expected, target, template, update, remove', [
    # Add new key
    (
            {"name":"Napat", "age":16, "is_student":True},
            {"name":"Napat"},
            {"name":"Napat", "age":16, "is_student":True},
            True,
            True
    ),
    # Remove current key
    (
            {"name":"Napat"},
            {"name":"Napat", "age":16, "is_student":True},
            {"name":"Napat"},
            True,
            True
    ),
    # Add new key & keep current value
    (
            {"name":"Talay", "age":16, "is_student":True},
            {"name":"Talay"},
            {"name":"Napat", "age":16, "is_student":True},
            True,
            True
    ),
    # Add new key & Keep current value & Remove key
    (
            {"name":"Talay", "age":16, "is_student":True},
            {"name":"Talay", "student_id":"12345"},
            {"name":"Napat", "age":16, "is_student":True},
            True,
            True
    ),
    # Add nothing & Remove
    (
            {"name":"Napat"},
            {"name":"Napat", "age":16, "is_student":True},
            {"name":"Talay", "student_id":"12345"},
            False,
            True
    ),
    # Add & Remove nothing
    (
            {"name":"Talay", "student_id":"12345", "age":16, "is_student":True},
            {"name":"Talay", "student_id":"12345"},
            {"name":"Napat", "age":16, "is_student":True},
            True,
            False
    ),
    # Add nothing & Remove nothing
    (
            {"name":"Napat"},
            {"name":"Napat"},
            {"name":"Napat", "age":16, "is_student":True},
            False,
            False
    ),
])
def test_sync_dictionaries(expected, target, template, update, remove):
    data_utils.sync_dictionaries(template=template, target=target, add_new_key=update, remove_current_key=remove)
    assert target == expected