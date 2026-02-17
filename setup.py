from setuptools import setup, find_packages

setup(
    name="db-sync-job",          # installable package name
    version="0.1.0",
    packages=find_packages(),    # automatically finds db_sync folder
    install_requires=[
        # Add dependencies here if needed
        "psycopg2-binary"
    ],
)
