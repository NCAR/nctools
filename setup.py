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
                            and cnode.targets[0].id.endswith("_")
                            and isinstance(cnode.value, ast.Str)):
                        attrs[cnode.targets[0].id] = cnode.value.s
    return attrs


def main():

    from setuptools import setup, find_packages
    from setuptools.command.develop import develop
    from setuptools.command.install import install

    import sys
    import os

    here = os.path.abspath(os.path.dirname(__file__))
    mgr = collect_taskattrs(os.path.join(here, "nctools", "main.py"), "NcTools")
    default_tasks = {
            "matplot": None,
            "ncread" : os.path.join(here, "nctools", "ncread.py"),
            "ncplot" : os.path.join(here, "nctools", "ncplot.py"),
            "ncdump" : os.path.join(here, "nctools", "ncdump.py"),
            "nccalc" : os.path.join(here, "nctools", "nccalc.py"),
    }

    class PostCommand(object):

        def _isinstalled(self, task):
            import pyloco
            fout = open(os.devnull,"w"); ferr = open(os.devnull,"w")
            stdout = sys.stdout; stderr = sys.stderr

            try:
                sys.stdout = fout; sys.stderr = ferr;
                ret, _ =  pyloco.perform(task, "-h")
                return ret

            except:
                return -1

            finally:
                sys.stdout = stdout; sys.stderr = stderr


        def _install_task(self, name, path):
            import pyloco

            if self._isinstalled(name) != 0:

                if path is None:
                    print("Installing '%s' task from a remote index." % name)
                    ret, _ = pyloco.perform("install", [name])

                else:
                    print("Installing '%s' task from a local file." % name)
                    ret, _ = pyloco.perform("install", [path])

                if ret != 0:
                    print("'%s' is not installed" % task)

            else:
                print("'%s' task is already installed." % name)

        def _pyloco_install(self):

            try:
                for name, path in default_tasks.items():
                    self._install_task(name, path)

            except Exception as err:
                print("nctools installation failed: %s" % str(err))

    class PostDevelopCommand(PostCommand, develop):

        def run(self):
            develop.run(self)
            self._pyloco_install()

    class PostInstallCommand(PostCommand, install):

        def run(self):
            install.run(self)
            self._pyloco_install()

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
        install_requires=["pyloco", "numpy", "netCDF4", "matplotlib"] + list(default_tasks.keys()),
        url=mgr.get("_url_", None),
        entry_points={
            'console_scripts': [
                'nctools = nctools.__main__:main'
            ]
        },
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
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

