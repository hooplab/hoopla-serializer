from setuptools import setup


setup(
    name = 'hooplaserializer',
    author = 'Hoopla',
    author_email = 'team@hoopla.no',
    url = 'http://www.hoopla.no',
    description = 'Hoopla serializer',
    zip_safe=False,

    install_requires = [
        'marshmallow==0.7.0'
    ]
)
