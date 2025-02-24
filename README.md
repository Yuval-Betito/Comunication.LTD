# 🔐 Cyber Security Final Project

## 📌 Introduction
This project integrates web development knowledge with core cybersecurity principles to create a secure, web-based information system using a relational database.

## 🛡️ Project Overview
The project simulates an information system for a fictional telecommunications company called **Comunication_LTD**. This company markets internet service packages and maintains a database containing customer information, internet packages, and sectors to which products are marketed.

## 🗃️ Technical Requirements
- **Relational Database**: MySQL or SQL Express.
- **Programming Language**: Python with Django framework.
- **Security Principles**: Implementation of secure development practices.

## 🎯 Implemented Features

### 1. User Registration
- Define new users.
- Complex password policy managed via configuration file.
- Secure password storage using HMAC + Salt hashing.
- Email definition for user verification.

### 2. Password Change
- Verification of the existing password.
- Input of a new password complying with complexity requirements.

### 3. Login Screen
- Username and password input.
- User validation with appropriate feedback.

### 4. Customer Management
- Adding new customer information.
- Displaying newly added customer details.

### 5. Forgot Password
- Generating a random token sent via email (SHA-1 secured).
- User inputs the received token to access the password reset screen.

## 🛠️ Security Measures and Code Protection

### ✅ Access Control
- Sensitive views (`user_home`, `create_customer`, `change_password`) protected by `@login_required`.

### ✅ Django ORM Usage
- All database interactions managed through Django's ORM to prevent SQL Injection.

### ✅ Input Validation
- Validation of user inputs and password checks using Django forms.

### ✅ Messages Framework
- Clear and secure user notifications via Django's built-in messages system.

### ✅ CSRF Protection
- Forms protected with `{% csrf_token %}` against Cross-Site Request Forgery attacks.

## 🔒 Detailed Security Implementation

### 1. Prevention of XSS (Cross-Site Scripting)
- Data sanitization through Django’s autoescaping mechanism:
```html
{{ message|escape }}
```

### 2. Prevention of SQL Injection
- Secure database interaction through Django ORM:
```python
user = User.objects.get(username=username)
form.save()
```

### 3. CSRF Protection
- Inclusion of `{% csrf_token %}` in all POST request forms.

### 4. Secure Password Management
- Password hashing using HMAC + Salt:
```python
def hash_password(raw_password):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac('sha256', raw_password.encode('utf-8'), salt, 100000)
    return salt + hashed_password
```

### 5. Password Complexity Enforcement
- Password policy defined in configuration file (`PASSWORD_CONFIG`):
```python
PASSWORD_CONFIG = {
    'min_length': 10,
    'complexity': {
        'uppercase': True,
        'lowercase': True,
        'digits': True,
        'special_characters': True,
    },
    'history_limit': 3,
    'dictionary_check': True,
    'max_login_attempts': 3,
    'lock_duration_minutes': 10
}
```

### 6. Login Attempt Restrictions
- Limiting login attempts to prevent brute-force attacks (maximum of 3 failed attempts).

## 🗂️ Project Structure
```
CyberProject/
├── README.md
├── docs/
│   ├── security_explanation.pdf
│   └── project_requirements.pdf
├── src/
│   ├── views.py
│   ├── models.py
│   └── forms.py
└── templates/
    ├── login.html
    ├── register.html
    ├── change_password.html
    └── forgot_password.html
```

## 🚀 Getting Started
```bash
git clone <repository-url>
cd CyberProject
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📞 Contact
- Yuval Betito
- Email: yuval36811@gmail.com




   
