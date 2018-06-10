from setuptools import setup
import cryptorocket

setup(name='cryptorocket',
      version=cryptorocket.__version__,
      description='Daily and weekly analysis of the top 100 cryptocurrencies from coinmarketcap',
      url='https://github.com/mauryaland/crypto-analysis',
	license='MIT License',
      author='Amaury Fouret',
	author_email='amaury@fouret.org',
      packages=['cryptorocket'],
	install_requires=[
	  'pandas>=0.23.0',
        'numpy>=1.14.3',
        'urllib3>=1.22',
        'ijson>=2.3',
        'msgpack>=0.5.6'],
      zip_safe=False)
