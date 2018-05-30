from setuptools import setup

setup(name='cryptorocket',
      version=cryptorocket.__version__,
      description='Daily and weekly analysis of the top 100 cryptocurrencies from coinmarketcap',
      url='https://github.com/mauryaland/crypto-analysis',
	  license='MIT License',
      author='Amaury Fouret',
	  author_email='amaury@fouret.org',
      packages=['cryptorocket'],
	  install_requires=[
	  'pandas>=0.23.0'],
      zip_safe=False)
