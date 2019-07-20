
def main():

    from setuptools import setup, find_packages
    from setuptools.command.develop import develop
    from setuptools.command.install import install
    from subprocess import check_call

    import sys
    import os
    import pyloco
    from nctools.main import NcTools as mgr

    here = os.path.dirname(os.path.abspath(__file__))
    default_tasks = ("matplot", "ncread", "ncplot")

    class PostCommand(object):

        def _isinstalled(self, task):
            fout = open(os.devnull,"w"); ferr = open(os.devnull,"w")
            stdout = sys.stdout; stderr = sys.stderr
            sys.stdout = fout; sys.stderr = ferr;
            ret, _ =  pyloco.perform(task, "-h")
            sys.stdout = stdout; sys.stderr = stderr
            return ret == 0

        def _install_task(self, task):
            if not self._isinstalled(task):
                ret, _ = pyloco.perform("install", [task])
                if ret != 0:
                    print("'%s' is not installed" % task)

        def _pyloco_install(self):

            ret = 0

            try:
                for task in default_tasks:
                    self._install_task(task)

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
        name=mgr._name_,
        version=mgr._version_,
        description=mgr._description_,
        long_description=mgr._long_description_,
        author=mgr._author_,
        author_email=mgr._author_email_,
        license=mgr._license_,
        packages=find_packages(),
        test_suite="tests.nctools_unittest_suite",
        install_requires=["pyloco"],
        url=mgr._url_,
        entry_points={
            'console_scripts': [
                'nctools = nctools.__main__:main'
            ]
        },
        cmdclass={
            'develop': PostDevelopCommand,
            'install': PostInstallCommand,
        },
        classifiers=[
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Development Status :: 1 - Planning',
            'License :: OSI Approved :: %s' % mgr._license_,
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

