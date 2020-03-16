"""
Module to run tests on SpecObjs
"""
import os

import numpy as np
import pytest

from astropy.io import fits

from pypeit import msgs
from pypeit import specobjs
from pypeit import specobj
msgs.reset(verbosity=2)

def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'files')
    return os.path.join(data_dir, filename)

@pytest.fixture
def sobj1():
    return specobj.SpecObj('MultiSlit', 1, SLITID=0)
@pytest.fixture
def sobj2():
    return specobj.SpecObj('MultiSlit', 1, SLITID=1)
@pytest.fixture
def sobj3():
    return specobj.SpecObj('MultiSlit', 1, SLITID=2)


def test_init(sobj1, sobj2):
    """ Run the parameter setup script
    """
    # Null
    sobjs1 = specobjs.SpecObjs()

    # With a few objs
    sobjs2 = specobjs.SpecObjs([sobj1,sobj2])
    assert sobjs2.nobj == 2


def test_access(sobj1, sobj2):
    sobjs = specobjs.SpecObjs([sobj1,sobj2])
    #
    assert sobjs[0]['PYPELINE'] == 'MultiSlit'
    assert len(sobjs['PYPELINE']) == 2

def test_add_rm(sobj1, sobj2, sobj3):
    sobjs = specobjs.SpecObjs([sobj1,sobj2])
    sobjs.add_sobj(sobj3)
    assert sobjs.nobj == 3
    # Remove
    sobjs.remove_sobj(2)
    assert len(sobjs.specobjs) == 2

    # Numpy 18
    sobjs1 = specobjs.SpecObjs()
    sobjs2 = specobjs.SpecObjs()
    sobjs2.add_sobj(sobjs1)


def test_set(sobj1, sobj2, sobj3):
    sobjs = specobjs.SpecObjs([sobj1,sobj2,sobj3])
    # All
    sobjs.DET = 3
    assert np.all(sobjs[:].DET == np.array([3,3,3]))
    sobjs[:].DET = 4
    assert np.all(sobjs[:].DET == np.array([4,4,4]))
    # Slice
    sobjs[1:2].DET = 2
    assert sobjs.DET[1] == 2
    # With logic
    det2 = sobjs.DET == 2
    sobjs[det2].PYPELINE = 'BLAH'
    assert sobjs.PYPELINE[1] == 'BLAH'
    assert sobjs.PYPELINE[0] == 'MultiSlit'


def test_io(sobj1, sobj2, sobj3):
    sobjs = specobjs.SpecObjs([sobj1,sobj2,sobj3])
    sobjs[0]['BOX_WAVE'] = np.arange(1000).astype(float)
    sobjs[1]['BOX_WAVE'] = np.arange(1000).astype(float)
    sobjs[2]['BOX_WAVE'] = np.arange(1000).astype(float)
    # Write
    header = fits.PrimaryHDU().header
    ofile = data_path('tst_specobjs.fits')
    if os.path.isfile(ofile):
        os.remove(ofile)
    sobjs.write_to_fits(header, ofile, overwrite=False)
    # Read
    hdul = fits.open(ofile)
    assert len(hdul) == 4

