from distutils.core import setup
import py2exe

setup(console=[
    'winapp.py',
    'outlook/calendar.py',
    'outlook/subjects.py',
    'edookit/scraper.py',
    'edookit/gradeaverage.py'
    ]
)