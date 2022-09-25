import pytest
import requests


class TestUserGender:
    url = 'https://hr-challenge.interactivestandard.com/api/test/users'

    @pytest.mark.parametrize("test_input, expected", [('male', 200), ('female', 200)])
    def test_positive_status_code(self, test_input, expected):
        response = requests.get(self.url, params={'gender': test_input})
        assert response.status_code == expected
    