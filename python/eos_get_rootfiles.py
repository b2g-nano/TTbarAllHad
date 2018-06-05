#!/usr/bin/env python
###
### Scrambled from https://github.com/xrootd/xrootd-python/tree/master/examples
###

from XRootD import client
from XRootD.client.flags import DirListFlags

def eos_get_rootfiles( path, xrdstr = "root://cmseos.fnal.gov/" ):

    from XRootD.client.flags import OpenFlags

    myclient = client.FileSystem(xrdstr)
    istatus, ilisting = myclient.dirlist(path, DirListFlags.STAT)

    rootfiles = []
    toks = path.split("/")
    
    outfile = toks[-1] + '.root'
    for ientry in ilisting:
        jstatus, jlisting = myclient.dirlist(path + '/' + ientry.name, DirListFlags.STAT)
        for jentry in jlisting:
            kstatus, klisting = myclient.dirlist(path + '/' + ientry.name + '/' + jentry.name, DirListFlags.STAT)
            for kentry in klisting :
                s = xrdstr + path + '/' + ientry.name + '/' + jentry.name + '/' + kentry.name
                if '.root' in s:
                    rootfiles.append(s)

    return rootfiles
