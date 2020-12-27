from unittest.mock import ANY

import pytest
from flask_resty.testing import assert_response

from crossword_backend import models

# -----------------------------------------------------------------------------


def test_get_list_ok(client, game, game_id):
    response = client.get(f"/games/-/squares/?game_id={game_id}")
    assert_response(response, 200, [ANY] * (game.size ** 2))


def test_post_not_allowed(client):
    response = client.post("/games/-/squares/", data={})
    assert_response(response, 405)


def test_get_by_id_ok(client, game_id):
    response = client.get(f"/games/{game_id}/squares/0;0/")
    assert_response(response, 200, ANY)


@pytest.mark.parametrize(
    ("update_data", "expected_is_writeable"),
    (
        ({"char": None}, True),
        ({"char": "A"}, True),
        ({"char": "A", "clue_number": 11}, True),
        ({"char": models.Square.BLACK}, False),
    ),
)
def test_update_square_ok(client, expected_is_writeable, game_id, update_data):
    response = client.patch(f"/games/{game_id}/squares/0;0/", data=update_data)
    assert_response(
        response,
        200,
        {
            "row": 0,
            "col": 0,
            "writeable": expected_is_writeable,
            "char": None,
            **update_data,
        },
    )


@pytest.mark.parametrize(
    "update_data",
    ({"writeable": False, "char": "A"}, {"row": 5}, {"col": 5}),
)
def test_update_invalid(client, game_id, update_data):
    response = client.patch(f"/games/{game_id}/squares/0;0/", data=update_data)
    assert_response(response, 422)


def test_delete_not_allowed(client, game_id):
    response = client.delete(f"/games/{game_id}/squares/0;0/")
    assert_response(response, 405)
