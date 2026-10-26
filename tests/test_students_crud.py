import datetime
from fastapi.testclient import TestClient

SAMPLE_STUDENT = {
    "name": "Arjun Kumar",
    "date_of_birth": "2004-06-15",
    "email": "arjun.kumar@example.com",
    "phone": "+91-9876543210",
    "course": "Computer Science",
    "address": "12 Tech Lane, Bengaluru",
    "enrollment_date": "2023-08-01"
}

def test_create_student_success(client: TestClient):
    response = client.post("/students", json=SAMPLE_STUDENT)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == SAMPLE_STUDENT["name"]
    assert data["email"] == SAMPLE_STUDENT["email"]
    assert data["course"] == SAMPLE_STUDENT["course"]

def test_create_student_duplicate_email(client: TestClient):
    client.post("/students", json=SAMPLE_STUDENT)
    # Second post with same email
    response = client.post("/students", json=SAMPLE_STUDENT)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_create_student_validation_errors(client: TestClient):
    # Invalid email
    invalid_data = dict(SAMPLE_STUDENT, email="not-an-email")
    response = client.post("/students", json=invalid_data)
    assert response.status_code == 422

    # Missing required field (name)
    invalid_data = dict(SAMPLE_STUDENT)
    del invalid_data["name"]
    response = client.post("/students", json=invalid_data)
    assert response.status_code == 422

def test_get_student_by_id(client: TestClient):
    post_res = client.post("/students", json=SAMPLE_STUDENT)
    student_id = post_res.json()["id"]

    get_res = client.get(f"/students/{student_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == SAMPLE_STUDENT["name"]

def test_get_student_not_found(client: TestClient):
    response = client.get("/students/99999")
    assert response.status_code == 404

def test_list_and_filter_students(client: TestClient):
    # Create 3 students
    s1 = dict(SAMPLE_STUDENT, email="s1@example.com", name="Alice Smith", course="Data Science", date_of_birth="2003-01-01")
    s2 = dict(SAMPLE_STUDENT, email="s2@example.com", name="Bob Jones", course="Computer Science", date_of_birth="2005-05-05")
    s3 = dict(SAMPLE_STUDENT, email="s3@example.com", name="Charlie Brown", course="Computer Science", date_of_birth="2006-09-09")
    client.post("/students", json=s1)
    client.post("/students", json=s2)
    client.post("/students", json=s3)

    # 1. List all
    res = client.get("/students")
    assert res.status_code == 200
    assert len(res.json()) == 3

    # 2. Filter by course
    res = client.get("/students?course=Computer Science")
    assert len(res.json()) == 2

    # 3. Search query
    res = client.get("/students?search=Alice")
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Alice Smith"

    # 4. Filter born after 2005-01-01
    res = client.get("/students?born_after=2005-01-01")
    assert len(res.json()) == 2

    # 5. Sorting
    res = client.get("/students?sort_by=name&order=asc")
    names = [s["name"] for s in res.json()]
    assert names == ["Alice Smith", "Bob Jones", "Charlie Brown"]

def test_update_student_put(client: TestClient):
    post_res = client.post("/students", json=SAMPLE_STUDENT)
    student_id = post_res.json()["id"]

    update_payload = {
        "name": "Arjun K. Updated",
        "date_of_birth": "2004-06-15",
        "email": "arjun.updated@example.com",
        "phone": "+91-1111122222",
        "course": "Artificial Intelligence",
        "address": "New Address",
        "enrollment_date": "2023-08-01"
    }

    put_res = client.put(f"/students/{student_id}", json=update_payload)
    assert put_res.status_code == 200
    updated_data = put_res.json()
    assert updated_data["name"] == "Arjun K. Updated"
    assert updated_data["course"] == "Artificial Intelligence"
    assert updated_data["email"] == "arjun.updated@example.com"

def test_patch_student_partial(client: TestClient):
    post_res = client.post("/students", json=SAMPLE_STUDENT)
    student_id = post_res.json()["id"]

    patch_res = client.patch(f"/students/{student_id}", json={"course": "Cyber Security"})
    assert patch_res.status_code == 200
    assert patch_res.json()["course"] == "Cyber Security"
    # Other fields remain intact
    assert patch_res.json()["name"] == SAMPLE_STUDENT["name"]

def test_delete_student(client: TestClient):
    post_res = client.post("/students", json=SAMPLE_STUDENT)
    student_id = post_res.json()["id"]

    del_res = client.delete(f"/students/{student_id}")
    assert del_res.status_code == 200
    assert del_res.json()["success"] is True

    # Verify student is now 404
    get_res = client.get(f"/students/{student_id}")
    assert get_res.status_code == 404

    # Second delete returns 404
    del_again = client.delete(f"/students/{student_id}")
    assert del_again.status_code == 404

def test_courses_and_stats(client: TestClient):
    client.post("/students", json=SAMPLE_STUDENT)
    client.post("/students", json=dict(SAMPLE_STUDENT, email="ds@example.com", course="Data Science"))

    courses_res = client.get("/students/courses/list")
    assert courses_res.status_code == 200
    assert "Computer Science" in courses_res.json()
    assert "Data Science" in courses_res.json()

    stats_res = client.get("/students/stats/summary")
    assert stats_res.status_code == 200
    assert stats_res.json()["total_students"] == 2
