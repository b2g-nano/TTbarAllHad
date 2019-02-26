#!/usr/bin/env python

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--dir", dest="dir",
                          help="CRAB directory", metavar="DIR")
    (options, args) = parser.parse_args()

    import os
    import subprocess

    vals = os.walk( options.dir )
    for (dirname, subdirs, files) in vals:
        if '/results' in dirname and len(files) > 0:
            outname = dirname.split('/')[0] + '_' + ''.join( dirname.split('/')[1:-1] )
            outname += '.root'
            filenames = ' '.join( [dirname +'/' + str(f) for f in files] )
            s = ('hadd ' + outname + ' ' + filenames)
            subprocess.call( s, shell=True )
            print s

    return


if __name__ == "__main__":
    main()
