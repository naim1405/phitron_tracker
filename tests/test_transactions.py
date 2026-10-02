def test_get_all_transactions(client, auth_headers, sample_transaction):
    response = client.get("/transactions", headers=auth_headers)

    assert response.status_code == 200
    transactions = response.json()
    assert isinstance(transactions, list)
    assert len(transactions) == 1
    assert transactions[0]["title"] == "Groceries"


def test_get_transaction_by_id(client, auth_headers, sample_transaction):
    transaction_id = sample_transaction["id"]
    response = client.get(f"/transactions/{transaction_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert data["title"] == "Groceries"
    assert data["amount"] == 500.0


def test_create_transaction(client, auth_headers):
    response = client.post("/transactions", json={
        "title": "Salary",
        "amount": 50000.0,
        "type": "income",
        "category": "Work",
        "date": "2026-10-01",
    }, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Salary"
    assert data["amount"] == 50000.0
    assert data["type"] == "income"
    assert "id" in data


def test_update_transaction(client, auth_headers, sample_transaction):
    transaction_id = sample_transaction["id"]
    response = client.put(f"/transactions/{transaction_id}", json={
        "title": "Groceries Updated",
        "amount": 750.0,
    }, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Groceries Updated"
    assert data["amount"] == 750.0
    assert data["type"] == "expense"


def test_delete_transaction(client, auth_headers, sample_transaction):
    transaction_id = sample_transaction["id"]

    delete_response = client.delete(f"/transactions/{transaction_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Transaction deleted successfully"

    get_response = client.get(f"/transactions/{transaction_id}", headers=auth_headers)
    assert get_response.status_code == 404
