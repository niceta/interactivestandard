import pytest
import requests


class TestUserId:
    url = 'https://hr-challenge.interactivestandard.com/api/test/user/'

    @pytest.mark.parametrize('user_id', ['5', '10', '15'])
    def test_positive_status_code(self, user_id):
        response = requests.get(self.url + user_id)
        assert response.status_code == 200
