import re

from setuptools import setup, find_packages

try:  # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements


def requirements(filename):
    reqs = parse_requirements(filename, session=False)
    return [str(r.req) for r in reqs]

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
    packages=find_packages(exclude=['tests']),
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
    install_requires=requirements('requirements.txt')
)
