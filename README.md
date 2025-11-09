# Flask API with Security Vulnerabilities

A simple Flask API with intentional security vulnerabilities for demonstration purposes.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints

- `GET /` - Welcome message and available endpoints
- `GET /user/<username>` - Get user information by username
- `GET /ping?host=<host>` - Ping a host

## Known Vulnerabilities

### 1. SQL Injection (Line 34)
**Location:** `/user/<username>` endpoint

**Vulnerable Code:**
```python
query = "SELECT * FROM users WHERE username = '%s'" % username
cursor.execute(query)
```

**Fix (one line change):**
```python
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### 2. Command Injection (Line 44)
**Location:** `/ping` endpoint

**Vulnerable Code:**
```python
result = os.system(f"ping -c 1 {host}")
```

**Fix (one line change):**
```python
result = subprocess.run(["ping", "-c", "1", host], capture_output=True)
```

## Testing

Try these exploits to verify the vulnerabilities:

### SQL Injection:
```bash
curl http://localhost:5000/user/alice%27%20OR%20%271%27=%271
```

### Command Injection:
```bash
curl "http://localhost:5000/ping?host=127.0.0.1;cat%20/etc/passwd"
```

