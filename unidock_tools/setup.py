from setuptools import setup, find_packages

install_requires = []
setup(
    name="Uni-Dock Tools",
    version="0.0.1",
    author="DP Technology",
    author_email="zhengh@dp.tech",
    description=("Several docking-related applications based on Uni-Dock"),
    url="https://github.com/dptech-corp/Uni-Dock/tree/main/unidock_tools",
    license=None,
    keywords="Docking",
    install_requires=install_requires,
    packages=find_packages(),
    package_data={"": ["*.dat"]},
    zip_safe=False,
    entry_points={"console_scripts": []},
    include_package_data=True
)
