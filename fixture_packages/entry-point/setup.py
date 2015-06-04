from setuptools import setup, find_packages

setup(name='entry-point',
      version='0.1dev',
      description="Entry Point Test Fixture",
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      license="BSD",
      packages=find_packages(),
      zip_safe=False,
      install_requires=[
          'setuptools',
          'morepath'
      ],
      entry_points={
          'morepath': [
              'autoimport = entrypoint',
          ]
      })
