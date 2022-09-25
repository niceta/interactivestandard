import pytest
import requests


class TestUserGender:
    url = 'https://hr-challenge.interactivestandard.com/api/test/users'

    @pytest.mark.parametrize("gender, expected", [('male', 200), ('female', 200)])
    def test_positive_status_code(self, gender, expected):
        response = requests.get(self.url, params={'gender': gender})
        assert response.status_code == expected
            @pytest.mark.parametrize('gender, param_for_check, expected',
                             [('male', 'success', True), ('male', 'errorCode', 0), ('male', 'errorMessage', None),
                              ('female', 'success', True), ('female', 'errorCode', 0), ('female', 'errorMessage', None)])
    def test_positive_response_content_except_result(self, gender,  param_for_check, expected):
        response = requests.get(self.url, params={'gender': gender})
        assert response.json().get(param_for_check) == expected
