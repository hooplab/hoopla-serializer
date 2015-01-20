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
            type_ = self.opts.type
            if type_ not in self.context['visited']:
                self.context['visited'][type_] = set()
            if key in self.context['visited'][type_]:
                return MarshalResult(Link(key), [])
            self.context['visited'][type_].add(key)

            return super(Schema, self).dump(obj, False, update_fields, **kwargs)

    @property
    def linked_fields(self):
        return [field for field in self.fields.values() if isinstance(field, Linked)]

    def _extract_root_links(self, data):
        links = {}
        for field in self.linked_fields:
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

    def _add_links(self, data):
        links = {}

        def add_to_links(id_, field_name, many):
            if many:
                if field_name not in links:
                    links[field_name] = [id_]
                else:
                    links[field_name].append(id_)
            else:
                links[field_name] = id_

        for field in self.linked_fields:
            primary_key = field.schema.opts.primary_key
            type_ = field.schema.opts.type
            link_list = data[field.name] if field.many else [data[field.name]]
            for link in link_list:
                id_ = link.id if isinstance(link, Link) else link[type_][primary_key]
                add_to_links(id_, field.name, field.many)

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

        for field in self.linked_fields:
            type_ = field.schema.opts.type

            linked_list = data[field.name] if field.many else [data[field.name]]

            for linked_ in linked_list:
                if isinstance(linked_, Link):
                    continue
                add_to_linked(linked_['linked'])
                add_to_linked({type_: [linked_[type_]]})

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
