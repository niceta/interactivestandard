import pytest
import requests
from pytest_schema import schema


class TestUserGender:
    url = 'https://hr-challenge.interactivestandard.com/api/test/users'

    @pytest.mark.parametrize("gender, expected", [('male', 200), ('female', 200)])
    def test_positive_status_code(self, gender, expected):
        response = requests.get(self.url, params={'gender': gender})
        assert response.status_code == expected

    @pytest.mark.parametrize('gender', ['male', 'female'])
    def test_response_schema(self, gender):
        expected_schema = {
            "success": bool,
            "errorCode": int,
            "errorMessage": str,
            "result": list
        }
        response_json = requests.get(self.url, params={'gender': gender}).json()
        assert schema(expected_schema) == response_json

    @pytest.mark.parametrize('gender, param_for_check, expected',
                             [('male', 'success', True), ('male', 'errorCode', 0), ('male', 'errorMessage', None),
                              ('female', 'success', True), ('female', 'errorCode', 0), ('female', 'errorMessage', None)])
    def test_positive_response_content_except_result(self, gender,  param_for_check, expected):
        response = requests.get(self.url, params={'gender': gender})
        assert response.json().get(param_for_check) == expected

    @pytest.mark.parametrize('gender', ['male', 'female'])
    def test_positive_response_result(self, gender):
        response = requests.get(self.url, params={'gender': gender})
        all([isinstance(i, int) for i in response.json().get('result')])

    @pytest.mark.parametrize('gender', ['male', 'female'])
    def test_content_type(self, gender):
        response = requests.get(self.url, params={'gender': gender})
        assert response.headers.get('content-type') == 'application/json;charset=UTF-8'

    @pytest.mark.parametrize('wrong_gender', ['0', '1', 'true', 'false', 'magic', 'McCloud'])
    def test_negative_input(self, wrong_gender):
        response = requests.get(self.url, params={'gender': wrong_gender})
        # it should be not None, depends on documentation
        # but there is no info about such behaviour in the doc =)
        assert response.json().get('errorMessage') is not None

    # this test might be flaky in case of huge number of registration,
    # but probability of this case is extremely low
    @pytest.mark.parametrize('gender', ['male', 'female'])
    def test_idempotence(self, gender):
        first_response = requests.get(self.url, params={'gender': gender})
        second_response = requests.get(self.url, params={'gender': gender})
        assert first_response.json() == second_response.json()

    def test_result_for_male_and_female_should_be_different(self):
        male_response = requests.get(self.url, params={'gender': 'male'})
        female_response = requests.get(self.url, params={'gender': 'female'})
        male_result = set(male_response.json().get('result'))
        female_result = set(female_response.json().get('result'))
        assert len(male_result & female_result) == 0
