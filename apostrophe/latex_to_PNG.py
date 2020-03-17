# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
"""
Based on latex2png.py from Stuart Rackham

AUTHOR
    Written by Stuart Rackham, <srackham@gmail.com>
    The code was inspired by Kjell Magne Fauske"s code:
    http://fauskes.net/nb/htmleqII/

    See also:
    http://www.amk.ca/python/code/mt-math
    http://code.google.com/p/latexmath2png/

COPYING
    Copyright (C) 2010 Stuart Rackham. Free use of this software is
    granted under the terms of the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
"""

import os
import subprocess
import tempfile


class LatexToPNG:
    TEX_HEADER = r"""\documentclass{article}
    \usepackage{amsmath}
    \usepackage{amsthm}
    \usepackage{amssymb}
    \usepackage{bm}
    \newcommand{\mx}[1]{\mathbf{\bm{#1}}} % Matrix command
    \newcommand{\vc}[1]{\mathbf{\bm{#1}}} % Vector command
    \newcommand{\T}{\text{T}}			 % Transpose
    \pagestyle{empty}
    \begin{document}"""

    TEX_FOOTER = r"""\end{document}"""

    def __init__(self):
        self.temp_result = tempfile.NamedTemporaryFile(suffix=".png")

    def latex2png(self, tex, outfile, dpi, modified):
        """Convert LaTeX input file infile to PNG file named outfile."""
        outfile = os.path.abspath(outfile)
        outdir = os.path.dirname(outfile)
        texfile = tempfile.mktemp(suffix=".tex", dir=os.path.dirname(outfile))
        basefile = os.path.splitext(texfile)[0]
        dvifile = basefile + ".dvi"
        temps = [basefile + ext for ext in (".tex", ".dvi", ".aux", ".log")]
        skip = False

        tex = "{}\n{}\n{}\n".format(self.TEX_HEADER, tex.strip(), self.TEX_FOOTER)

        open(texfile, "w").write(tex)
        saved_pwd = os.getcwd()

        os.chdir(outdir)

        args = ["latex", "-halt-on-error", texfile]
        p = subprocess.Popen(args,
                             stderr=subprocess.STDOUT,
                             stdout=subprocess.PIPE)

        output = p.stdout
        output_lines = output.readlines()
        if os.path.isfile(dvifile):  # DVI File exists
            # Convert DVI file to PNG.
            args = ["dvipng",
                    "-D", str(dpi),
                    "-T", "tight",
                    "-x", "1000",
                    "-z", "9",
                    "-bg", "Transparent",
                    "-o", outfile,
                    dvifile]

            p = subprocess.Popen(args)
            p.communicate()

        else:
            self.clean_up(temps)
            """
            Errors in Latex output start with "! "
            Stripping exclamation marks and superflous newlines
            and telling the user what he"s done wrong.
            """
            i = []
            error = ""
            for line in output_lines:
                line = line.decode("utf-8")
                if line.startswith("!"):
                    error += line[2:]  # removing "! "
            if error.endswith("\n"):
                error = error[:-1]
            raise Exception(error)

    def generatepng(self, formula):
        try:
            self.temp_result = tempfile.NamedTemporaryFile(suffix=".png")
            formula = "$" + formula + "$"
            self.latex2png(formula, self.temp_result.name, 300, False)
            return True, self.temp_result.name

        except Exception as e:
            self.temp_result.close()
            return False, e.args[0]

    def clean_up(self, files):
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
