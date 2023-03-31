from distutils.core import setup
import py2exe
import shutil,os,sys

sys.argv.append("py2exe")

#setup(console=["main.py"])
setup(windows=["main.py"])
shutil.copy("17monipdb.dat",os.path.join("dist","17monipdb.dat"))