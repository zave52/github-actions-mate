import os
from unittest.mock import patch

import pytest

from app import app, db

os.environ.setdefault("DB_CONNECTION", "sqlite:///:memory:")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # Setup database
    with app.app_context():
        db.create_all()

    yield client

    # Teardown the database
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_home_page(client):
    """Test the home page access and counter increment."""
    response = client.get("/")
    assert b"Docker is Awesome!" in response.data
    assert b"Page reload count: 1" in response.data

    # Check if counter is increments
    second_response = client.get("/")
    assert b"Page reload count: 2" in second_response.data


def test_docker_logo(client):
    """Test the docker logo endpoint."""
    response = client.get("/logo")
    assert response.status_code == 200
    assert response.content_type == "image/png"


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.data == b"Healthy"


def test_readiness_check(client):
    """Test the readiness check."""
    with patch("app.time.time", return_value=0):
        response = client.get("/ready")
        assert response.status_code == 503


def test_external_call(client):
    """Test the external call endpoint."""
    with patch("app.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Success"
        response = client.get("/external-call")
        assert b"External call response: Success" in response.data
        assert response.status_code == 200
