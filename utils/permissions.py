def has_admin_role(user):
    return any(role.permissions.administrator for role in user.roles)