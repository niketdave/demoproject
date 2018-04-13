APP_USER_TYPE = (
    ('employee', 'Employee'),
    ('shipper', 'Shipper'),
    ('carrier', 'Carrier'),
    ('driver', 'Driver'),
    ('subadmin', 'Subadmin'),
    ('admin', 'Admin'))

PASSWORD_SPECIAL_CHARACTER_SYNTAX = '!@#$%&_='
PASSSWORD_MIN_LENGTH = 8
PASSWORD_DIGIT_ERROR = 'Password must contain at least 1 digit.'
PASSWORD_LENGTH_ERROR = 'Password must be at least 8 characters long.'
PASSWORD_LETTER_ERROR = 'Password must contain at least 1 letter.'
PASSWORD_SYMBOL_ERROR = 'Password must contain at least 1 special symbol.'
PASSWORD_WHITESPACE_ERROR = 'Password should not contain white space.'
RESET_PASSWORD_LINK_ERROR = 'The link seems to be no longer valid. Please make a new request to reset your password.'
RESET_PASSWORD_CONFIRM_ERROR = 'Password and confirm password do not match.'
RESET_PASSWORD_SUCCESS_MSG = 'Password changed successfully.'
ACCOUNT_REMOVED_MESSAGE = 'Your account has been removed from the application, please contact admin.'
ACCOUNT_INACTIVE_MESSAGE = 'You account is inactive. Please contact admin to activate.'
ACCOUNT_ACTIVE_MESSAGE = 'Your account has been activated by admin now you can login with your old credentials.'
ACCOUNT_DELETED_MESSAGE = 'your account has been deleted by admin,Please Contact admin'
ACCOUNT_CREDENTIAL_MESSAGE = 'Invalid username and/or password.'
ACCOUNT_ALREADY_REGISTERED_MESSAGE = 'You are already registered with us. Please log into your account.'
RECORD_NOT_FOUND_ERROR = "No Record Found For This user Type"
USER_NOT_FOUND_ERROR = "User Not Found"
WORD_SET_OF_PASSWORD = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
