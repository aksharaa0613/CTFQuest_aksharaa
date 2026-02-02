# Web CTF Challenge Walkthrough

## Challenge Overview
This is a multi-step web security challenge with SQL injection and authentication bypass vulnerabilities.

**Flag Format:** `SECE{...}`

## Solution Steps

### Step 1: Initial Reconnaissance
1. Visit the login page at `http://localhost:5000`
2. Examine the page source for hints
3. Notice HTML comments mentioning debug endpoint

### Step 2: SQL Injection Authentication Bypass
Try SQL injection payloads in the username field:
```
Username: admin' OR '1'='1' --
Password: anything
```

This bypasses authentication due to vulnerable SQL query construction.

### Step 3: Access Debug Endpoint
1. From HTML comments, find debug endpoint: `/debug/info`
2. Access with required header:
```bash
curl -H "X-Debug-Token: dev_mode_2024" http://localhost:5000/debug/info
```

Response reveals:
- Session information
- Flag hint about admin panel source code
- Secret endpoint path

### Step 4: Examine Admin Panel Source
1. Login as admin using SQL injection
2. View page source of admin panel
3. Find HTML comment with final requirements:
   - Proper authentication bypass ✓
   - User-Agent containing 'ctf'
   - Access to secret endpoint

### Step 5: Get Final Flag
Access secret endpoint with proper User-Agent:
```bash
curl -H "User-Agent: ctf-solver" \
     -H "Cookie: session=<your_session_cookie>" \
     http://localhost:5000/s3cr3t_fl4g_3ndp01nt
```

**Final Flag:** `SECE{sql_1nj3ct10n_4nd_4uth_byp4ss_m4st3r}`

## Vulnerabilities Exploited
1. **SQL Injection** - Unparameterized query allows authentication bypass
2. **Information Disclosure** - Debug endpoint leaks sensitive information
3. **Weak Authentication** - Multiple bypass methods available
4. **Source Code Disclosure** - HTML comments reveal attack paths

## Alternative Solutions
- Use default credentials: `administrator:admin123` or `guest:password`
- Various SQL injection payloads work due to vulnerable query structure