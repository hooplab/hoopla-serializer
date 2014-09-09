from marshmallow import Serializer as MarshmallowSerializer, fields


class Embedded(fields.Nested):
    pass


class Linked(fields.Nested):
    pass


class Serializer(MarshmallowSerializer):
    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, fields.Nested)]


class BaseSerializer(Serializer):
    def _postprocess(self, data, obj):
        def add_links():
            _add_links_from_schema(self, data)

        def get_linked():
            linked = dict()
            _recur_schema(self, data, linked)
            for key, val in linked.items():
                linked[key] = val.values()
            return linked

        add_links()
        return {
            self.ROOT: data,
            "linked": get_linked()
        }

def _add_links_from_field(field, data):
    if not isinstance(field, Linked):
        return

    plural_name = field.schema.Meta.plural_name
    primary_key = field.schema.Meta.primary_key
    name = field.schema.Meta.name
    if field.many:
        links = {plural_name: [o[primary_key] for o in data[plural_name]]}
    else:
        links = {plural_name: data[name][primary_key]}
    if 'links' in data:
        data['links'].update(links)
    else:
        data['links'] = links


def _add_links_from_schema(schema, data):
    for field in schema.nested_fields:
        _add_links_from_field(field, data)

        name = field.name

        for _data in data[name] if field.many else [data[name]]:
            _add_links_from_schema(field.schema, _data)


def _get_data(schema, data):
    k = schema.Meta.primary_key
    n = schema.Meta.plural_name
    return {n: {data[k]: data}}


def _update_map(a, b):
    for k, v in b.items():
        if k in a:
            a[k].update(v)
        else:
            a[k] = v


def _recur_schema(schema, data, linked):
    for field in schema.nested_fields:
        _recur_field(field, data, linked)


def _recur_field(field, data, linked):
    name = field.name

    for _data in data[name] if field.many else [data[name]]:
        _recur_schema(field.schema, _data, linked)
        if isinstance(field, Linked):
            _update_map(linked, _get_data(field.schema, _data))

    if isinstance(field, Linked):
        del data[name]
