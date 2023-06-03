from argparse import ArgumentParser
from pydantic import validate_email
from backend.settings import APP_NAME
from backend.api.auth import hash_password
from backend.models.users import User
from backend.database import get_db


parser = ArgumentParser(APP_NAME)

parser.add_argument('--email', required=True, help='a valid email')
parser.add_argument('--password', required=True, help='at least 3 symbols')
parser.add_argument('--role', default='admin', help='intern, teacher or admin, default is admin')
parser.add_argument('--first-name', default='')
parser.add_argument('--last-name', default='')
parser.add_argument('--patronymic', default='')


args = parser.parse_args()

args.role = args.role.lower()
assert args.role in ('intern', 'teacher', 'admin'), (
    'role must be either "intern", "teacher" or "admin"'
)

validate_email(args.email)
assert len(args.password) >= 3, 'password is too short (min length is 3)'

user = User(
    first_name=args.first_name,
    last_name=args.last_name,
    patronymic=args.patronymic,
    email=args.email,
    password=hash_password(args.password),
    is_admin=args.role == 'admin',
    is_teacher=args.role == 'teacher',
)

db = next(get_db())

db.add(user)
db.commit()
db.close()

print('User successfully created.')
