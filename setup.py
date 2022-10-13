import setuptools

setuptools.setup(
        name="metamusic",
        version="0.0.1",
        packages=setuptools.find_packages(include="metamusic"),
        install_requires=["eyed3 ~= 0.9.6", "requests ~= 2.28.1"],
        # entry_points={},
        )
