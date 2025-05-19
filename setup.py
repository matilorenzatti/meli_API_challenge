from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='meli_project',
      version="0.0.03",
      description="Challenge tecnico para MELI - Data Analyst",
      license="MIT",
      author="Lorenzatti Matias",
      author_email="matilorenzatti99@gmail.com",
      url="https://github.com/matilorenzatti/meli_API_challenge",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
