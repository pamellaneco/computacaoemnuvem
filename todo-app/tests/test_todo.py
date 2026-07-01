import pytest
from unittest.mock import patch, MagicMock
import app as todo_app

@pytest.fixture
def client():
    todo_app.app.config["TESTING"] = True
    with todo_app.app.test_client() as client:
        yield client

def make_mock_conn(rows=None):
    mock_cur = MagicMock()
    mock_cur.fetchall.return_value = rows or []
    mock_conn = MagicMock()
    mock_conn.cursor.return_value = mock_cur
    return mock_conn

def test_index_get(client):
    with patch("app.get_db", return_value=make_mock_conn()):
        response = client.get("/")
    assert response.status_code == 200
    assert "Lista de Tarefas".encode() in response.data

def test_adicionar_tarefa(client):
    with patch("app.get_db", return_value=make_mock_conn()):
        response = client.post("/", data={"descricao": "Estudar DevOps"})
    assert response.status_code == 302

def test_concluir_tarefa(client):
    with patch("app.get_db", return_value=make_mock_conn()):
        response = client.get("/concluir/1")
    assert response.status_code == 302