# 🔐 SecureLogin Portal - Web CTF Challenge

## Challenge Description
Welcome to the SecureLogin Portal, an "enterprise-grade" security system that needs your expertise to test its defenses. Your mission is to find the hidden flag by exploiting vulnerabilities in this web application.

**Objective:** Find the flag in format `SECE{...}`

## Setup Instructions
1. Install Flask: `pip install flask`
2. Run the application: `python app.py`
3. Access the portal: `http://localhost:5000`

## Challenge Hints

### 🔍 Reconnaissance
- Always examine the source code of web pages
- Look for comments that developers might have left behind
- Check for hidden endpoints or debug information

### 🔑 Authentication
- Try common username/password combinations
- The system might have default accounts
- Sometimes the login logic isn't as secure as it appears

### 🛠️ Advanced Techniques
- Modern web applications often have debug modes
- HTTP headers can sometimes unlock special functionality
- User-Agent strings might be important for certain endpoints

### 💡 General Tips
- This is a multi-step challenge - one vulnerability leads to another
- Pay attention to error messages and responses
- The flag requires multiple techniques to obtain

## Known Users
The system documentation mentions these default accounts exist:
- `administrator` (admin role)
- `guest` (standard user)

## Flag Format
`SECE{...}`



Good luck, and happy hacking! 🚀

---