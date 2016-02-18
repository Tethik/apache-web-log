from setuptools import setup, find_packages

setup(
    name         = 'apache-web-log',
    version      = '0.1',
    packages     = find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'Flask',
        'Flask-SQLAlchemy',
        'SQLAlchemy',
        'Flask-Bower',
        'python-geoip-geolite2',
        'passlib',
        'werkzeug',
        'python-geoip'
    ]
    # test_suite   = "burn.tests",
)
