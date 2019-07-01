#!/usr/bin/env python

# webkit2png - makes screenshots of webpages
# http://www.paulhammond.org/webkit2png

# modified and updated version by @somas95 (Manuel Genovés)

__version__=''
    # Copyright (c) 2009 Paul Hammond
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy
    # of this software and associated documentation files (the "Software"), to deal
    # in the Software without restriction, including without limitation the rights
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    # copies of the Software, and to permit persons to whom the Software is
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in
    # all copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    # THE SOFTWARE.
    #

import optparse
import sys
import os

try:
    import gi
    gi.require_version('WebKit2', '4.0')
    gi.require_version('Gtk', '3.0')
    from gi.repository import GObject as gobject
    from gi.repository import Gtk as gtk
    from gi.repository import Pango as pango
    from gi.repository import WebKit2 as webkit
    mode = "pygtk"
except ImportError:
    print("Cannot find python-webkit library files.  Are you sure they're installed?")
    sys.exit()

class PyGTKBrowser:

    def _save_image(self, webview, res, data):
        try:
            original_surface = webview.get_snapshot_finish(res)

            import cairo
            new_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1024, 768)
            ctx = cairo.Context(new_surface)
            ctx.set_source_surface(original_surface, 0, 0)
            ctx.paint()

            new_surface.write_to_png("test.png")

            self.thumbnail = os.path.abspath("test.png")
            #return new_surface
        except Exception as e:
            print("Could not draw thumbnail for %s: %s" % (self.title, str(e)))

    def _view_load_finished_cb(self, view, event):
        print(event)
        if event == webkit.LoadEvent.FINISHED:
            pixmap = view.get_snapshot(webkit.SnapshotRegion(1),
                                        webkit.SnapshotOptions(0), 
                                        None, self._save_image, None)
            #size = get_size()

            URL = view.get_main_frame().get_uri()
            filename = makeFilename(URL, self.options)

            pixbuf = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, size[0], size[1])
            pixbuf.get_from_drawable(pixmap, pixmap.get_colormap(),0,0,0,0,-1,-1)
            if self.options.fullsize:
                pixbuf.save(filename + "-full.png", "png")

            if self.options.thumb or self.options.clipped:
                thumbWidth = int(size[0] * self.options.scale)
                thumbHeight = int(size[1] * self.options.scale)

                thumbbuf = pixbuf.scale_simple(thumbWidth, thumbHeight, gtk.gdk.INTERP_BILINEAR)
                if self.options.thumb:
                    thumbbuf.save(filename + "-thumb.png", "png")

                if self.options.clipped:
                    clipbuf = thumbbuf.subpixbuf(0,thumbHeight-int(self.options.clipheight),
                                                    int(self.options.clipwidth), 
                                                    int(self.options.clipheight))
                    clipbuf.save(filename + "-clip.png", "png")

            gtk.main_quit()

    def __init__(self, options, args):
        self.options = options

        if options.delay:
            print("--delay is only supported on Mac OS X (for now). Sorry!")

        gobject.threads_init()
        window = gtk.Window()
        window.resize(int(options.initWidth),int(options.initHeight))
        self.view = webkit.WebView()

        settings = self.view.get_settings()
        settings.set_property("auto-load-images", not options.noimages)
        self.view.set_settings(settings)

        self.view.connect("load_changed", self._view_load_finished_cb)

        # window.add(self.view)
        # window.show_all()
        self.view.load_uri(args[0])
        # go go go
        gtk.main()



def main():

    # parse the command line
    usage = """%prog [options] [http://example.net/ ...]
examples:
%prog http://google.com/            # screengrab google
%prog -W 1000 -H 1000 http://google.com/ # bigger screengrab of google
%prog -T http://google.com/         # just the thumbnail screengrab
%prog -TF http://google.com/        # just thumbnail and fullsize grab
%prog -o foo http://google.com/     # save images as "foo-thumb.png" etc
%prog -                             # screengrab urls from stdin
%prog -h | less                     # full documentation"""

    cmdparser = optparse.OptionParser(usage,version=("webkit2png "+__version__))
    # TODO: add quiet/verbose options
    cmdparser.add_option("-W", "--width",type="float",default=800.0,
        help="initial (and minimum) width of browser (default: 800)")
    cmdparser.add_option("-H", "--height",type="float",default=600.0,
        help="initial (and minimum) height of browser (default: 600)")
    cmdparser.add_option("--clipwidth",type="float",default=200.0,
        help="width of clipped thumbnail (default: 200)",
        metavar="WIDTH")
    cmdparser.add_option("--clipheight",type="float",default=150.0,
        help="height of clipped thumbnail (default: 150)",
        metavar="HEIGHT")
    cmdparser.add_option("-s", "--scale",type="float",default=0.25,
        help="scale factor for thumbnails (default: 0.25)")
    cmdparser.add_option("-m", "--md5", action="store_true",
        help="use md5 hash for filename (like del.icio.us)")
    cmdparser.add_option("-o", "--filename", type="string",default="",
        metavar="NAME", help="save images as NAME-full.png,NAME-thumb.png etc")
    cmdparser.add_option("-F", "--fullsize", action="store_true",
        help="only create fullsize screenshot")
    cmdparser.add_option("-T", "--thumb", action="store_true",
        help="only create thumbnail sreenshot")
    cmdparser.add_option("-C", "--clipped", action="store_true",
        help="only create clipped thumbnail screenshot")
    cmdparser.add_option("-d", "--datestamp", action="store_true",
        help="include date in filename")
    cmdparser.add_option("-D", "--dir",type="string",default="./",
        help="directory to place images into")
    cmdparser.add_option("--delay",type="float",default=0,
        help="delay between page load finishing and screenshot")
    cmdparser.add_option("--noimages", action="store_true",
        help="don't load images")
    cmdparser.add_option("--debug", action="store_true",
        help=optparse.SUPPRESS_HELP)
    (options, args) = cmdparser.parse_args()
    if len(args) == 0:
        cmdparser.print_usage()
        return
    if options.filename:
        if len(args) != 1 or args[0] == "-":
            print("--filename option requires exactly one url")
            return
    if options.scale == 0:
        cmdparser.error("scale cannot be zero")
    # make sure we're outputing something
    if not (options.fullsize or options.thumb or options.clipped):
        options.fullsize = True
        options.thumb = True
        options.clipped = True
    # work out the initial size of the browser window
    #  (this might need to be larger so clipped image is right size)
    options.initWidth = (options.clipwidth / options.scale)
    options.initHeight = (options.clipheight / options.scale)
    if options.width>options.initWidth:
        options.initWidth = options.width
    if options.height>options.initHeight:
        options.initHeight = options.height

    PyGTKBrowser(options, args)

def makeFilename(self, URL, options):
    # make the filename
    if options.filename:
        filename = options.filename
    elif options.md5:
        try:
                import md5
        except ImportError:
                print("--md5 requires python md5 library")
        filename = md5.new(URL).hexdigest()
    else:
        import re
        filename = re.sub('\W','',URL)
        filename = re.sub('^http','',filename)
    if options.datestamp:
        import time
        now = time.strftime("%Y%m%d")
        filename = now + "-" + filename
    import os
    dir = os.path.abspath(os.path.expanduser(options.dir))
    return os.path.join(dir,filename)


if __name__ == "__main__": main()
