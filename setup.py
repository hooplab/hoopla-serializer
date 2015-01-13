from setuptools import setup


setup(
    name = 'hoopla-serializer',
    version = '0.1',
    license = 'MIT',
    packages = ['serializer'],
    include_package_data=True,
    author = 'Hoopla',
    author_email = 'team@hoopla.no',
    url = 'http://www.hoopla.no',
    description = 'Hoopla serializer',
    zip_safe=False,

    install_requires = [
        'marshmallow==1.0.0'
    ]
)
