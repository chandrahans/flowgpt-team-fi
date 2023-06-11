from setuptools import setup, find_packages

setup(
    name='rfq_bot',
    version='0.1.1',
    packages=find_packages(include=['rfq_bot', 'rfq_bot.*']),
    install_requires=[
        'python-telegram-bot',
        'beautifulsoup4',
        'requests',
        'openai',
        'pandas'
    ]
)