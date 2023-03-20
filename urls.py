from views import ItemAPI, GroupAPI


def register_api(app, model, name):
    item = ItemAPI.as_view(f'{name}-item', model)
    app.add_url_rule(f'/{name}/<int:item_id>', view_func=item)
    group = GroupAPI.as_view(f'{name}-group', model)
    app.add_url_rule(f'/{name}/', view_func=group)
