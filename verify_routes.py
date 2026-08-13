import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = 'http://127.0.0.1:5000'

# Create a cookie handler to persist session cookies (needed for flash messages)
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

def run_tests():
    print("--- Starting Task Manager Backend Verification Tests ---")

    # 1. GET / - Verify homepage loads and shows sample tasks
    print("\n1. Testing GET / (Homepage)...")
    try:
        response = urllib.request.urlopen(BASE_URL)
        html = response.read().decode('utf-8')
        assert response.status == 200, f"Expected 200 OK, got {response.status}"
        assert 'Task Manager' in html, "Homepage does not contain 'Task Manager'"
        assert 'Complete Backend Fundamentals Project' in html, "Homepage does not contain sample task"
        print("   [PASS] Homepage loaded successfully.")
    except Exception as e:
        print(f"   [FAIL] Homepage failed: {e}")
        return

    # 2. POST /add - Add a new student task
    print("\n2. Testing POST /add (Create Task)...")
    add_data = urllib.parse.urlencode({
        'title': 'Prepare chemistry lab report',
        'description': 'Conduct data analysis on titration parameters.',
        'due_date': '2026-08-18'
    }).encode('utf-8')

    try:
        req = urllib.request.Request(f"{BASE_URL}/add", data=add_data, method='POST')
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        assert response.status == 200, f"Expected 200 OK, got {response.status}"
        assert 'Task added successfully!' in html, "Success flash message not found"
        assert 'Prepare chemistry lab report' in html, "New task not displayed on dashboard"
        print("   [PASS] Task created successfully.")
    except Exception as e:
        print(f"   [FAIL] Task creation failed: {e}")
        return

    # Find the id of the newly created task from HTML
    match = re.search(r'/edit/(\d+)', html)
    if not match:
        print("   [FAIL] Could not retrieve new task ID for Edit/Delete testing.")
        return
    task_id = match.group(1)
    print(f"   [INFO] Found created task ID: {task_id}")

    # 3. POST /complete/<id> - Toggle completion
    print(f"\n3. Testing POST /complete/{task_id} (Toggle Completion)...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/complete/{task_id}", data=b'', method='POST')
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        assert response.status == 200, f"Expected 200 OK"
        assert 'marked active' in html or 'completed' in html, "Completion toggle flash message not found"
        print("   [PASS] Task completion toggled successfully.")
    except Exception as e:
        print(f"   [FAIL] Task completion toggle failed: {e}")

    # 4. POST /edit/<id> - Edit task
    print(f"\n4. Testing POST /edit/{task_id} (Update Task)...")
    edit_data = urllib.parse.urlencode({
        'title': 'Prepare chemistry lab report (Updated)',
        'description': 'Revised titration calculations and analysis.',
        'due_date': '2026-08-19',
        'completed': 'on'  # Checkbox ticked
    }).encode('utf-8')

    try:
        req = urllib.request.Request(f"{BASE_URL}/edit/{task_id}", data=edit_data, method='POST')
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        assert response.status == 200, f"Expected 200 OK"
        assert 'Task updated successfully!' in html, "Update flash message not found"
        assert 'Prepare chemistry lab report (Updated)' in html, "Updated title not found"
        print("   [PASS] Task updated successfully.")
    except Exception as e:
        print(f"   [FAIL] Task update failed: {e}")
        return

    # 5. POST /delete/<id> - Delete task
    print(f"\n5. Testing POST /delete/{task_id} (Delete Task)...")
    try:
        req = urllib.request.Request(f"{BASE_URL}/delete/{task_id}", data=b'', method='POST')
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')
        assert response.status == 200, f"Expected 200 OK"
        assert 'Task deleted successfully!' in html, "Delete flash message not found"
        assert 'Prepare chemistry lab report (Updated)' not in html, "Deleted task still displays"
        print("   [PASS] Task deleted successfully.")
    except Exception as e:
        print(f"   [FAIL] Task deletion failed: {e}")
        return

    print("\n--- All Student Task Manager Verification Tests PASSED ---")

if __name__ == '__main__':
    run_tests()
