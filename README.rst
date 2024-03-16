==============================
 The Geometry of the Universe
==============================

Colin Rourke, University of Warwick

https://www.worldscientific.com/worldscibooks/10.1142/12195

This new book is to be published in July 2021.

I have created this little project as a place for a virtual guide to
the book, as I work my way through it.

Install
=======


::

   git clone https://github.com/swfiua/gotu

   python3 setup.py install --user


You may need blume from github too:::

   git clone https://github.com/swfiua/blume
   
   cd gotu

   python3 setup.py install --user

Running modules
===============

Many modules can be run from the command line, often using argparse to
parse options::

   python3 -m gotu.spiral --sky

   python3 -m gotu.gaia -h

Most of these use blume to provide a console and matplotlib plotting
environment.

It is a strange console where single character commands can have
interesting consequences.  

To start the show, type::

  magic.show()

This will pop up a magplotlib figure.

Type 'h' to see what does what.

Good luck on your adventure.


