from marshmallow import Schema, SchemaOpts, fields


class Linked(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Linked, self).__init__(nested, default=default, **kwargs)


class NamespaceOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.name = getattr(meta, 'name')
        self.primary_key = getattr(meta, 'primary_key')
        self.plural_name = getattr(meta, 'plural_name', self.name)


class NameSpacedSchema(Schema):
    OPTIONS_CLASS = NamespaceOpts

    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, fields.Nested)]


class BaseSchema(NameSpacedSchema):
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
            self.opts.plural_name: data,
            'linked': get_linked()
        }


def _add_links_from_field(field, data):
    if not isinstance(field, Linked):
        return

    plural_name = field.schema.opts.plural_name
    primary_key = field.schema.opts.primary_key
    name = field.schema.opts.name

    if field.many:
        links = {plural_name: [o[primary_key] for o in data[plural_name]]}
    else:
        if not data[name]:
            links = {name: field.parent.obj[primary_key]}
        else:
            links = {name: data[name][primary_key]}

        if primary_key in data:
            del data[primary_key]

    if links:
        if 'links' in data:
            data['links'].update(links)
        else:
            data['links'] = links


def _add_links_from_schema(schema, data):
    for field in schema.nested_fields:
        _add_links_from_field(field, data)

        name = field.name

        nested_field_data = data[name] if field.many else [data[name]]
        for field_data in nested_field_data:
            if not field_data:
                continue

            _add_links_from_schema(field.schema, field_data)


def _get_data(schema, data):
    key = schema.opts.primary_key
    name = schema.opts.plural_name
    return {name: {data[key]: data}}


def _update_linked(a, b):
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

    nested_field_data = data[name] if field.many else [data[name]]
    for field_data in nested_field_data:
        if not field_data:
            continue

        _recur_schema(field.schema, field_data, linked)
        if isinstance(field, Linked):
            _update_linked(linked, _get_data(field.schema, field_data))

    if isinstance(field, Linked):
        del data[name]