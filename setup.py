from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))  # pylint: disable=invalid-name
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()  # pylint: disable=invalid-name

setup(name='firefox_secure_proxy',
      version='1.0.2',
      description='Standalone wrapper for Firefox Secure Proxy',
      url='https://github.com/Snawoot/firefox-secure-proxy',
      author='Vladislav Yarmak',
      author_email='vladislav-ex-src@vm-0.com',
      license='MIT',
      packages=['firefox_secure_proxy'],
      python_requires='>=3.5',
      setup_requires=[
          'wheel',
      ],
      install_requires=[
          'oic',
      ],
      entry_points={
          'console_scripts': [
              'fxsp-login=firefox_secure_proxy.login:main',
              'fxsp-getproxytoken=firefox_secure_proxy.getproxytoken:main',
          ],
      },
      classifiers=[
          "Programming Language :: Python :: 3.5",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: Other Audience",
          "Operating System :: OS Independent",
          "Natural Language :: English",
          "Topic :: Internet",
          "Topic :: Internet :: Proxy Servers",
          "Topic :: Utilities",
      ],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=True)
