from fastapi.testclient import TestClient

def test_ai_status_endpoint(client: TestClient):
    response = client.get("/ai/status")
    assert response.status_code == 200
    data = response.json()
    assert "ollama_online" in data
    assert "configured_model" in data
    assert data["configured_model"] == "llama3.2:1b"

def test_ai_ask_how_many_students(client: TestClient):
    # Add 2 students
    client.post("/students", json={
        "name": "Student A",
        "date_of_birth": "2004-01-01",
        "email": "a@example.com",
        "phone": "+91-9999911111",
        "course": "Computer Science"
    })
    client.post("/students", json={
        "name": "Student B",
        "date_of_birth": "2006-02-02",
        "email": "b@example.com",
        "phone": "+91-9999922222",
        "course": "Mechanical Engineering"
    })

    response = client.post("/ai/ask", json={"question": "How many students are there?"})
    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "How many students are there?"
    assert data["grounded_records_count"] == 2
    assert "2 student(s)" in data["answer"]

def test_ai_ask_born_after_filter(client: TestClient):
    client.post("/students", json={
        "name": "Young Student",
        "date_of_birth": "2006-05-15",
        "email": "young@example.com",
        "phone": "+91-9876543210",
        "course": "Data Science"
    })
    client.post("/students", json={
        "name": "Senior Student",
        "date_of_birth": "2002-01-01",
        "email": "senior@example.com",
        "phone": "+91-9876543211",
        "course": "Data Science"
    })

    response = client.post("/ai/ask", json={"question": "List students born after 2005."})
    assert response.status_code == 200
    data = response.json()
    assert "Young Student" in data["answer"]
    assert "Senior Student" not in data["answer"].split("[System Note:")[0]

def test_ai_ask_course_breakdown(client: TestClient):
    client.post("/students", json={
        "name": "CS Student",
        "date_of_birth": "2005-01-01",
        "email": "cs@example.com",
        "phone": "+91-9876543212",
        "course": "Computer Science"
    })

    response = client.post("/ai/ask", json={"question": "How many students are in Computer Science?"})
    assert response.status_code == 200
    data = response.json()
    assert "Computer Science" in data["answer"]
