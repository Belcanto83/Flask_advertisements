from flask.views import MethodView
from flask import jsonify, request
from validators import generate_validator


class ItemAPI(MethodView):
    def __init__(self, model):
        self.model = model
        self.validator = generate_validator(model)

    def _get_item(self, item_id):
        return self.model.query.get_or_404(item_id)

    def get(self, item_id):
        item = self._get_item(item_id)
        return jsonify(item.to_json())

    def patch(self, item_id):
        item = self._get_item(item_id)
        errors = self.validator.validate(request.json)
        if errors:
            return jsonify(errors), 400
        item.update_from_json(request.json)
        return jsonify(item.to_json())

    def delete(self, item_id):
        item = self._get_item(item_id)
        item.delete_item()
        return jsonify({'status': f'item {item_id} was deleted'})


class GroupAPI(MethodView):
    def __init__(self, model):
        self.model = model
        self.validator = generate_validator(model, create=True)

    def get(self):
        items = self.model.query.all()
        return jsonify([item.to_json() for item in items])

    def post(self):
        validation_errors = self.validator.validate(request.json)
        if validation_errors:
            return jsonify(validation_errors), 400
        item = self.model(**request.json)
        db_errors = item.create_from_json()
        if db_errors:
            return jsonify(db_errors), 400
        return jsonify(item.to_json())
