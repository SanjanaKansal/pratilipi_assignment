class UserDoesNotExistException(Exception):
    error = 'UserDoesNotExistException'
    message = 'User does not exist'


class UsernameAlreadyExistException(Exception):
    error = 'UsernameAlreadyExistException'
    message = 'User with username already exists'

