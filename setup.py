def collect_taskattrs(filename, clsname):
    import ast

    attrs = {}

    with open(filename) as f:
        tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == clsname:
                for cnode in node.body:
                    if (isinstance(cnode, ast.Assign) and len(cnode.targets)==1
                            and cnode.targets[0].id.startswith("_")
                            and cnode.targets[0].id.endswith("_")):
                        if isinstance(cnode.value, ast.Str):
                            attrs[cnode.targets[0].id] = cnode.value.s
                        elif isinstance(cnode.value, ast.List):
                            l = []
                            for elt in cnode.value.elts:
                                l.append(elt.s)
                            attrs[cnode.targets[0].id] = l
                        else:
                            print("Warning: unsupported manager attribute "
                                  "type: %s" % cnode.value.__class__.__name__)
    return attrs


def main():

    import os
    from setuptools import setup, find_packages

    here = os.path.abspath(os.path.dirname(__file__))
    mgr = collect_taskattrs(os.path.join(here, "nctools", "main.py"), "NcTools")

    setup(
        name=mgr.get("_name_"),
        version=mgr.get("_version_"),
        description=mgr.get("_description_", None),
        long_description=mgr.get("_long_description_", None),
        author=mgr.get("_author_", None),
        author_email=mgr.get("_author_email_", None),
        license=mgr.get("_license_", None),
        packages=find_packages(),
        test_suite="tests.nctools_unittest_suite",
        install_requires=["pyloco", "numpy", "netCDF4", "matplotlib"],
        url=mgr.get("_url_", None),
        entry_points={
            'console_scripts': [
                'nctools = nctools:main'
            ]
        },
            #'License :: OSI Approved :: %s' % mgr.get("_license_", "N/A"),
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Development Status :: 1 - Planning',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Code Generators']
        )


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
