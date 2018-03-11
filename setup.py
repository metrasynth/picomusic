import io
import os
import re
import sys

from setuptools import find_packages, setup

SETUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(SETUP_DIR)
import picomusic  # NOQA isort:skip


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


dependencies = read('requirements/base.txt').splitlines()


setup(
    name='PicoMusic',
    version=picomusic.__version__,
    url='https://github.com/metrasynth/picomusic',
    license='MIT',
    author='Matthew Scott',
    author_email='matt@11craft.com',
    description=__doc__,
    long_description='%s\n%s' % (
        re.compile(r'^\.\.\s+start-badges.*^\.\.\s+end-badges', re.M | re.S).
            sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'picomusic=picomusic.scripts.picomusic:main.start',
        ],
    },
    keywords='music sunvox learning',
    project_urls={
        'Documentation': 'https://picomusic.readthedocs.io/en/latest/',
        'Funding': 'https://www.patreon.com/queries',
        'Source': 'https://github.com/metrasynth/picomusic',
        'Tracker': 'https://github.com/metrasynth/picomusic/issues',
    },
    python_requires='~=3.6',
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Framework :: IPython',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Artistic Software',
        'Topic :: Education',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
    ]
)
