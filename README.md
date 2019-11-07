# libterm-git
This is an implementation of the Git CLI in pure Python. I am creating this to [provide Git support in the LibTerm app on iOS](https://github.com/ColdGrub1384/LibTerm/issues/21). It must be able to work around these limitations of LibTerm:

  * No CPython, therefore C extensions are not supported
  * No curses support
