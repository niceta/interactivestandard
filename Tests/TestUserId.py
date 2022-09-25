import pytest
import requests
from pytest_schema import schema


class TestUserId:
    url = 'https://hr-challenge.interactivestandard.com/api/test/user/'

    @pytest.mark.parametrize('user_id', ['5', '10', '15'])
    def test_positive_status_code(self, user_id):
        response = requests.get(self.url + user_id)
        assert response.status_code == 200

    def test_response_schema(self):
        expected_schema = {
            "success": bool,
            "errorCode": int,
            "errorMessage": str,
            "result":
            {
                "id": str,
                "name": str,
                "gender": str,
                "age": int,
                "city": str,
                "registrationDate": str
            }
        }
        existing_user_id = '5'
        response = requests.get(self.url + existing_user_id)
        assert schema(expected_schema) == response.json()

    @pytest.mark.parametrize('user_id', ['-5', '0', 'qwe', '!@#$'])
    def test_negative_input(self, user_id):
        response = requests.get(self.url + user_id)
        # it should be not None, depends on documentation
        # but there is no info about such behaviour in the doc =)
        assert response.json().get('errorMessage') is not None

    def test_idempotence(self):
        existing_user_id = '5'
        first_response = requests.get(self.url + existing_user_id)
        second_response = requests.get(self.url + existing_user_id)
        assert first_response.json() == second_response.json()

    def test_content_type(self):
        existing_user_id = '5'
        response = requests.get(self.url + existing_user_id)
        assert response.headers.get('content-type') == 'application/json;charset=UTF-8'
