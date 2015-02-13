from itertools import ifilter

from marshmallow import Schema as MSchema, SchemaOpts, fields, MarshalResult, utils


class Link:
    def __init__(self, id):
        self.id = id


class Nested(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Nested, self).__init__(nested, default=default, **kwargs)


class Linked(Nested):
    pass


class Embedded(Nested):
    pass

class NamespaceOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.primary_key = getattr(meta, 'primary_key')
        self.type = getattr(meta, 'type')


class Schema(MSchema):
    OPTIONS_CLASS = NamespaceOpts

    def serialize(self, obj, many=False, update_fields=True, **kwargs):

        data = self.dump(obj, many, update_fields, **kwargs).data

        if many:
            objects = []
            linked = {}
            links = data[0]['links']
            for obj in data:
                for field_type in obj['linked'].keys():
                    if field_type in obj['linked']:
                        if field_type in linked:
                            linked[field_type].extend(obj['linked'][field_type])
                        else:
                            linked[field_type] = obj['linked'][field_type]
                        del obj['linked'][field_type]
                objects.append(obj[self.opts.type])
            return {
                self.opts.type: objects,
                'linked': linked,
                'links': links
            }
        return data

    def dump(self, obj, many=False, update_fields=True, **kwargs):
        many = self.many if many is None else bool(many)
        if many:
            self.many = False
            results = []
            errors = []
            for o in obj:
                result, error = self.dump(o, False, update_fields, **kwargs)
                results.append(result)
                errors.append(error)

            return MarshalResult(results, errors)
        else:
            if 'visited' not in self.context:
                self.context['visited'] = dict()
            key = self.fields[self.opts.primary_key].get_value(self.opts.primary_key, obj)
            type_ = self.opts.type
            if type_ not in self.context['visited']:
                self.context['visited'][type_] = set()
            if key in self.context['visited'][type_]:
                return MarshalResult(Link(key), [])
            self.context['visited'][type_].add(key)

            return super(Schema, self).dump(obj, False, update_fields, **kwargs)

    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, Nested)]

    @property
    def linked_fields(self):
        return [field for field in self.fields.values() if isinstance(field, Linked)]

    @property
    def embedded_fields(self):
        return [field for field in self.fields.values() if isinstance(field, Embedded)]

    def _extract_root_links(self, data):
        links = {}
        for field in self.nested_fields:
            links[self.opts.type + "." + field.name] = {
                'type': field.schema.opts.type
            }
            if field.many:
                links_ = next(ifilter(lambda x: not isinstance(x, Link), data[field.name]), {'links': {}})['links']
            else:
                if isinstance(data[field.name], Link):
                    continue
                links_ = data[field.name]['links']
            if isinstance(field, Embedded):
                for link, type_dict in links_.items():
                    links[link.replace(field.schema.opts.type, self.opts.type + "." + field.name)] = type_dict
            else:
                links.update(links_)
        return links

    def _add_links(self, data):
        links = {}

        def get_id(link, type_, primary_key):
            return link.id if isinstance(link, Link) else link[type_][primary_key]

        for field in self.linked_fields:
            primary_key = field.schema.opts.primary_key
            type_ = field.schema.opts.type
            if field.many:
                links[field.name] = [get_id(link, type_, primary_key) for link in data[field.name]]
            else:
                links[field.name] = get_id(data[field.name], type_, primary_key)

        if links:
            data['links'] = links

    def _extract_linked(self, data):
        linked = {}

        def add_to_linked(b):
            for key, val in b.items():
                if key not in linked:
                    linked[key] = val
                else:
                    linked[key].extend(val)

        for field in self.nested_fields:
            type_ = field.schema.opts.type

            linked_list = data[field.name] if field.many else [data[field.name]]
            for linked_ in linked_list:
                if isinstance(linked_, Link):
                    continue
                add_to_linked(linked_['linked'])
                if isinstance(field, Linked):
                    add_to_linked({type_: [linked_[type_]]})

        for field in self.embedded_fields:
            type_ = field.schema.opts.type
            if isinstance(field, Embedded):
                if field.many:
                    data[field.name] = [linked_[type_] for linked_ in data[field.name]]
                else:
                    data[field.name] = data[field.name][type_]

        for field in self.linked_fields:
            del data[field.name]

        return linked

    def _postprocess(self, data, obj):
        # order is important here
        self._add_links(data)
        links = self._extract_root_links(data)
        linked = self._extract_linked(data)

        return {
            self.opts.type: data,
            'linked': linked,
            'links': links
        }


def _recur_find(keys, obj, default):
    first_key = keys[0]
    next_obj = utils.get_value(first_key, obj, default)
    if len(keys) == 1:
        return next_obj
    if isinstance(next_obj, list):
        return [_recur_find(keys[1:], o, default) for o in next_obj]
    else:
        return _recur_find(keys[1:], next_obj, default)

@Schema.accessor
def find_many_to_one(schema, key, obj, default=None):
    return _recur_find(key.split('.'), obj, default)
