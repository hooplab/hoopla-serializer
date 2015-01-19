from marshmallow import Schema as MSchema, SchemaOpts, fields


class Linked(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Linked, self).__init__(nested, default=default, **kwargs)


class Embedded(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Embedded, self).__init__(nested, default=default, **kwargs)


class NamespaceOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.name = getattr(meta, 'name')
        self.primary_key = getattr(meta, 'primary_key')
        self.plural_name = getattr(meta, 'plural_name', self.name)


class Schema(MSchema):
    OPTIONS_CLASS = NamespaceOpts

    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, fields.Nested)]

    def _postprocess(self, data, obj):
        def bubble_linked(data, linked):
            links = {}
            for field in self.nested_fields:
                plural_name = field.schema.opts.plural_name
                primary_key = field.schema.opts.primary_key

                linked_object = data[field.name][plural_name]
                linked_object_list = linked_object if field.many else [linked_object]

                _update_linked(linked, data[field.name]['linked'])
                del data[field.name]

                if plural_name in linked:
                    linked[plural_name].extend(linked_object_list)
                else:
                    linked[plural_name] = linked_object_list

                if field.many:
                    links[field.name] = [o[primary_key] for o in linked_object]
                else:
                    links[field.name] = linked_object[primary_key]

            if links:
                data['links'] = links

        # Bubble links
        links = {}
        for field in self.nested_fields:
            if self.many and len(data) == 0:
                continue
            _links = data[0][field.name]['links'] if self.many else data[field.name]['links']
            for link, type_dict in _links.items():
                links[link.replace(field.schema.opts.plural_name, self.opts.plural_name+"."+field.name)] = type_dict
            links[self.opts.plural_name+"."+field.name] = {
                'type': field.schema.opts.plural_name
            }

        linked = {}
        if not self.many:
            bubble_linked(data, linked)
        else:
            for d in data:
                bubble_linked(d, linked)


        return {
            self.opts.plural_name: data,
            'linked': linked,
            'links': links
        }


def _get_data(schema, data):
    key = schema.opts.primary_key
    name = schema.opts.plural_name

    # If we want 'id' instead of '<type>_id'
    # data['id'] = data[key]
    # del data[key]
    # return {name: {data['id']: data}}

    return {name: {data[key]: data}}


def _update_linked(a, b):
    for k, v in b.items():
        if k in a:
            a[k].update(v)
        else:
            a[k] = v
