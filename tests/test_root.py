"""Tests for GET / (root) endpoint using AAA pattern"""


def test_root_redirects_to_static_index_html(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to / with follow_redirects=False
    Assert: Response status is a redirect (307 or 302) and Location header points to /static/index.html
    """
    # Arrange
    expected_redirect_codes = [301, 302, 303, 307, 308]

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in expected_redirect_codes
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_with_follow_redirects_returns_html(client):
    """
    Arrange: TestClient is ready
    Act: Make GET request to / with follow_redirects=True
    Assert: Final response is HTML content (from index.html)
    """
    # Arrange
    # (nothing to arrange, following redirects means TestClient will handle the redirect)

    # Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
