# Authentication System for django_blog

## Features
- User Registration
- Login and Logout
- Profile Management

## URL Patterns
- `/register`: Register a new user
- `/login`: Log in an existing user
- `/logout`: Log out the current user
- `/profile`: View and edit profile

## How to Test
1. Visit `/register` to create an account.
2. Log in at `/login`.
3. Update profile details at `/profile`.
4. Log out at `/logout`.

## Security Measures
- CSRF tokens included in all forms.
- Passwords securely hashed using Django's built-in algorithms.
