# session.py
_session_data = {}

# This will act like a global session store
_logged_in_user = {
    "account_number": None,
    "name": None,
    "account_type": None,
    "branch": None,
    "role": "user"
}


def set_session(account_number, name, account_type, branch, role):
    global _session_data
    # Set session information in the global store
    _session_data["account_number"] = account_number
    _session_data["name"] = name
    _session_data["account_type"] = account_type
    _session_data["branch"] = branch
    _session_data["role"] = role

    # Simultaneously update the logged-in user data
    _logged_in_user["account_number"] = account_number
    _logged_in_user["name"] = name
    _logged_in_user["account_type"] = account_type
    _logged_in_user["branch"] = branch
    _logged_in_user["role"] = role


def get_session():
    # Return the session data from the global store
    return _session_data


def get_logged_in_account():
    # Get the account number of the logged-in user
    return _logged_in_user.get("account_number")


def logout():
    global _session_data, _logged_in_user
    # Clear both session and logged-in user data when logging out
    _session_data = {}
    _logged_in_user = {
        "account_number": None,
        "name": None,
        "account_type": None,
        "branch": None,
        "role": "user"
    }
