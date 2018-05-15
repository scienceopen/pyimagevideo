#!/usr/bin/env python
import tempfile
import numpy as np
import subprocess
from pathlib import Path
import imageio
#
import pyimagevideo as piv
R = Path(__file__).parents[1]


def test_rgbbgr():
    subprocess.check_call(['python','RGB_BGR_GBR_conv.py','--noshow'], cwd=R)

def test_tiff_multipage_rw():
    with tempfile.TemporaryDirectory() as d:
        d = Path(d).expanduser()

        piv.genimgseries(d)

        ofn = d/'mp.tif'
        piv.png2tiff(ofn, '[0-9].png')

        y = imageio.mimread(ofn)

    assert len(y) == 10

def test_wavelength2rgb():
    np.testing.assert_allclose(piv.wavelength2rgb(720),(146,0,0))

def test_cv2codec_read():
    try:
        import cv2
    except ImportError:
        return
        
    fn = R/'tests/star_collapse_out.avi'
    vid = cv2.VideoCapture(str(fn))

    ret,img = vid.read() #a 3-D Numpy array, last axis is BGR: blue,green,red
    vid.release()

    assert ret,'could not open video'
    assert img.shape == (480,720,3),'video not decoded properly'
    
    
#    cv2.imshow(fn.name, img)
 #   cv2.destroyAllWindows()
    
if __name__ == '__main__':
    np.testing.run_module_suite()
