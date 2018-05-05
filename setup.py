import re
from setuptools import setup, find_packages


def get_version():
    with open('relayer/__init__.py', 'r') as f:
        version_regex = r'^__version__\s*=\s*[\'"](.+)[\'"]'
        return re.search(version_regex, f.read(), re.MULTILINE).group(1)


setup(
    name='relayer',
    version=get_version(),
    url='https://github.com/wizeline/relayer',
    author='Wizeline',
    author_email='engineering@wizeline.com',
    description='Relayer is a library to emit kafka messages and group logs to relay them to kafka for log aggregation.',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,
    keywords=['relayer', 'log', 'kafka'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'kafka-python>=1.3.4',
        'structlog>=17.2.0',
    ]
)
