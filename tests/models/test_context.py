import pytest
from almora.models.context import UserContext

@pytest.mark.parametrize("is_logged_in, user_id, username", [
    (None, None, None),
    (False, None, None),
    (True, None, None),
    (True, "USER123", "somyod_ja"),
    (True, "USER001", "por_ka"),
    (False, "USER123", "somyod_ja"),
    (False, 123, "ABC"),
    (True, 123, "ABC"),
    (True, "Hello", True),
    (True, 3.14, None),
])
def test_dataclass_user_context_datatype(is_logged_in, user_id, username):
    user = UserContext()

    if type(is_logged_in) is bool:
        user.is_logged_in = is_logged_in
        if is_logged_in:
            assert user.is_logged_in == True

            if type(username) is str:
                user.username = username
                assert user.username == username
            else:
                with pytest.raises(TypeError):
                    user.username = username
            if type(user_id) is str:
                user.user_id = user_id
                assert user.user_id == user_id
            else:
                with pytest.raises(TypeError):
                    user.user_id = user_id
        else:
            assert user.is_logged_in == False
            assert user.user_id is None
            assert user.username is None

            if type(username) is str:
                with pytest.raises(AttributeError):
                    user.username = username
            else:
                with pytest.raises(TypeError):
                    user.username = username
            if type(user_id) is str:
                with pytest.raises(AttributeError):
                    user.user_id = user_id
            else:
                with pytest.raises(TypeError):
                    user.user_id = user_id
    else:
        with pytest.raises(TypeError):
            user.is_logged_in = is_logged_in

def test_dataclass_user_context_input():
    user = UserContext()
    user.is_logged_in = True
    user.user_id = "123"
    user.username = "Cat"
    with pytest.raises(AttributeError):
        user.user_id = "456"
    with pytest.raises(AttributeError):
        user.username = "Dog"