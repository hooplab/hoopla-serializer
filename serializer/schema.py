from itertools import ifilter

from marshmallow import Schema as MSchema, SchemaOpts, fields, MarshalResult


class Link:
    def __init__(self, id):
        self.id = id


class Linked(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Linked, self).__init__(nested, default=default, **kwargs)


class Embedded(fields.Nested):
    def __init__(self, nested, default=None, **kwargs):
        super(Embedded, self).__init__(nested, default=default, **kwargs)


class NamespaceOpts(SchemaOpts):
    def __init__(self, meta):
        SchemaOpts.__init__(self, meta)
        self.primary_key = getattr(meta, 'primary_key')
        self.type = getattr(meta, 'type')


class Schema(MSchema):
    OPTIONS_CLASS = NamespaceOpts

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
            key = obj[self.opts.primary_key]
            type = self.opts.type
            if type not in self.context['visited']:
                self.context['visited'][type] = set()
            if key in self.context['visited'][type]:
                return MarshalResult(Link(key), [])
            self.context['visited'][type].add(key)

            return super(Schema, self).dump(obj, False, update_fields, **kwargs)

    @property
    def nested_fields(self):
        return [field for field in self.fields.values() if isinstance(field, fields.Nested)]

    def _extract_links(self, data):
        links = {}
        for field in self.nested_fields:
            links[self.opts.type + "." + field.name] = {
                'type': field.schema.opts.type
            }
            if field.many:
                _links = next(ifilter(lambda x: not isinstance(x, Link), data[field.name]), {'links': {}})['links']
            else:
                if isinstance(data[field.name], Link):
                    continue
                _links = data[field.name]['links']
            links.update(_links)
        return links

    def _extract_linked(self, data):
        linked = {}

        def add_to_linked(b):
            for key, val in b.items():
                if key not in linked:
                    linked[key] = val
                else:
                    linked[key].extend(val)

        def bubble_linked(link, type_, primary_key, field):
            if isinstance(link, Link):
                if 'links' not in data:
                    data['links'] = {}
                if field.many:
                    if field.name not in data['links']:
                        data['links'][field.name] = [link.id]
                    else:
                        data['links'][field.name].append(link.id)
                else:
                    data['links'][field.name] = link.id
                return
            linked_object = link[type_]
            bubbled_linked = link['linked']

            add_to_linked(bubbled_linked)

            if type_ in linked:
                linked[type_].append(linked_object)
            else:
                linked[type_] = [linked_object]
            if 'links' not in data:
                data['links'] = {}
            if field.many:
                if field.name not in data['links']:
                    data['links'][field.name] = [linked_object[primary_key]]
                else:
                    data['links'][field.name].append(linked_object[primary_key])
            else:
                data['links'][field.name] = linked_object[primary_key]

        for field in self.nested_fields:
            if isinstance(field, Linked):
                primary_key = field.schema.opts.primary_key
                type_ = field.schema.opts.type
                if field.many:
                    for linked_object in data[field.name]:
                        bubble_linked(linked_object, type_, primary_key, field)
                else:
                    bubble_linked(data[field.name], type_, primary_key, field)
                del data[field.name]

            elif isinstance(field, Embedded):
                raise NotImplementedError
        return linked

    def _postprocess(self, data, obj):
        # order is important here
        links = self._extract_links(data)
        linked = self._extract_linked(data)

        return {
            self.opts.type: data,
            'linked': linked,
            'links': links
        }
