"""
Test all files in this directory.
"""

import pytest
from glob import glob
import time


def main():
    print('Starting tests...')
    start = time.time()
    for f in glob('day*.py'):
        retcode = pytest.main([f])
        
    print('Ran all tests in {time.time() - start}s.')


if __name__ == '__main__':
    main()