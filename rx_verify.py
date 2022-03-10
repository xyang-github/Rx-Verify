import os
from app import create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'development')


@app.cli.command()
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)