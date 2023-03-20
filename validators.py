import pydantic
from typing import Optional

from models import User
from errors import ForeignKeyError


class CreateUserValidationModel(pydantic.BaseModel):
    username: pydantic.constr(max_length=50)
    password: pydantic.constr(max_length=100)

    @pydantic.validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password length must be at least 8 simbols!')
        return value


class PatchUserValidationModel(CreateUserValidationModel):
    username: Optional[pydantic.constr(max_length=50)]
    password: Optional[pydantic.constr(max_length=100)]


class CreateAdvValidationModel(pydantic.BaseModel):
    title: pydantic.constr(max_length=200)
    owner_id: int


class PatchAdvValidationModel(pydantic.BaseModel):
    title: Optional[pydantic.constr(max_length=200)]
    description: Optional[str]


class UserValidator:
    def __init__(self, create: bool):
        self.create = create

    def get_validation_model(self):
        # POST
        if self.create:
            return CreateUserValidationModel
        # PATCH
        else:
            return PatchUserValidationModel

    def validate(self, json_data):
        validation_model = self.get_validation_model()
        try:
            validation_model(**json_data)
        except pydantic.ValidationError as err:
            return err.errors()


class AdvValidator:
    def __init__(self, create: bool):
        self.create = create

    @staticmethod
    def check_fk_constraints(json_data):
        users = User.query.all()
        user_ids = [user.id for user in users]
        if (u_id := json_data.get('owner_id')) not in user_ids:
            raise ForeignKeyError(400, f'user with id={u_id} is not registered')

    def get_validation_model(self):
        # POST
        if self.create:
            return CreateAdvValidationModel
        # PATCH
        else:
            return PatchAdvValidationModel

    def validate(self, json_data):
        validation_model = self.get_validation_model()
        try:
            # уровень-1 - проверка pydantic
            validation_model(**json_data)
            # уровень-2 - проверка службы:
            # Проверяем ограничение внешнего ключа (owner_id)
            if self.create:
                self.check_fk_constraints(json_data)
        except pydantic.ValidationError as err:
            return err.errors()
        except ForeignKeyError as err:
            return {'status_code': err.status_code, 'message': err.message}


# class PatchValidator:
#     def __init__(self, model):
#         self.model = model
#
#     @staticmethod
#     def validate(instance, json_data):
#         errors = []
#         for field in json_data:
#             if field not in instance.__dict__.keys():
#                 error = {'status': 'attribute error', 'message': f'attribute "{field}" is not correct'}
#                 errors.append(error)
#
#         return errors


def generate_validator(model, create=False):
    if model.__name__ == 'User':
        return UserValidator(create)
    return AdvValidator(create)
