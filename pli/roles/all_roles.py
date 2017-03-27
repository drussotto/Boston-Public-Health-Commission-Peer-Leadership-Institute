from flask_principal import Identity, AnonymousIdentity, identity_changed, RoleNeed, UserNeed, Permission

# String must not have spaces, as users can have multiple roles
# And this is accomplished by a space delimited string.
# For more information, see example data for MongoDB
ADMIN_ROLE = "admin"
PARTICIPANT_ROLE = "participant"
ORG_ROLE = "org"
EDITOR_ROLE = "editor"
PEERLEADER_ROLE = "peer_leader"

ADMIN_NEED = RoleNeed(ADMIN_ROLE)
PARTICIPANT_NEED = RoleNeed(PARTICIPANT_ROLE)
ORG_NEED = RoleNeed(ORG_ROLE)
EDITOR_NEED = RoleNeed(EDITOR_ROLE)
PEERLEADER_NEED = RoleNeed(PEERLEADER_ROLE)

ADMIN_PERM = Permission(ADMIN_NEED)
PARTICIPANT_PERM = Permission(PARTICIPANT_NEED)
ORG_PERM = Permission(ORG_NEED)
EDITOR_PERM = Permission(EDITOR_NEED)
PEERLEADER_PERM = Permission(PEERLEADER_NEED)


def all_roles():
    return [ADMIN_ROLE, PARTICIPANT_ROLE, ORG_ROLE, EDITOR_ROLE, PEERLEADER_ROLE]
