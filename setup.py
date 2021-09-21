""" Installer script """

from setuptools import setup, find_packages


def main() -> None:
    """Install module"""

    setup(
        name="attr-tracers",
        version="1.0.0",
        packages=["tracers"],
        license="MIT",
        description="Easily debug and trace attribute changes in your classes",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        install_requires=["pytermgui"],
        url="https://github.com/bczsalba/tracer",
        author="BcZsalba",
        author_email="bczsalba@gmail.com",
    )


if __name__ == "__main__":
    main()
