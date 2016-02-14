from distutils.core import setup
import py2exe
import matplotlib
import matplotlib.backends.backend_tkagg
import sys
import kivy.graphics.shader
import kivy
sys.path.append('C:\Python27\Lib')
sys.path.append('C:\Python27\Lib\site-packages\kivy\graphics')
setup(windows=['ThreadedGUI.py'], options = { "py2exe":{"includes": ["matplotlib.backends.backend_tkagg","FileDialog", "kivy.graphics.buffer","kivy.graphics.vertex","kivy.graphics.vbo","kivy.graphics.compiler","kivy.graphics.shader","kivy.graphics"]}})
