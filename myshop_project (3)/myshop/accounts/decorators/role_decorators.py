from django.contrib.auth.decorators import user_passes_test

def role_required(role):
    def check(user):
        return user.is_authenticated and user.role == role
    return user_passes_test(check)

def roles_required(*roles):
    def check(user):
        return user.is_authenticated and user.role in roles
    return user_passes_test(check)
