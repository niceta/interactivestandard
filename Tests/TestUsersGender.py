import pytest
import requests


class TestUserGender:
    url = 'https://hr-challenge.interactivestandard.com/api/test/users'

    @pytest.mark.parametrize("gender, expected", [('male', 200), ('female', 200)])
    def test_positive_status_code(self, gender, expected):
        response = requests.get(self.url, params={'gender': gender})
        assert response.status_code == expected
        