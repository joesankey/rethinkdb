#!/usr/bin/env python

'''Dispatcher for interactive functions such as repl and backup'''

import os, sys
from . import utils_common, net

def startInterpreter(prog, argv):
    import code, readline, optparse
    
    connectOptions = {}
    replVariables = {'r':utils_common.r, 'rethinkdb':utils_common.r}
    banner = 'The RethinkDB driver has been imported as `r`.'
    
    # -- get host/port setup
    
    # - parse command line
    parser = utils_common.CommonOptionsParser(prog=prog, description='An interactive Python shell (repl) with the RethinkDB driver imported')
    options, args = parser.parse_args(argv)
    
    # -- open connection
    
    try:
        replVariables['conn'] = utils_common.getConnection()
        replVariables['conn'].repl()
        banner += '''
    A connection to %s:%d has been established as `conn`
    and can be used by calling `run()` on a query without any arguments.''' % (options.hostname, options.driver_port)
    except utils_common.r.ReqlDriverError as e:
        banner += '\nWarning: %s' % str(e)
    
    # -- start interpreter
    
    code.interact(banner=banner + '\n==========', local=replVariables)
    
if __name__ == '__main__':
    if __package__ is None:
        __package__ = 'rethinkdb'
    
    # -- figure out which mode we are in
    modes = ['dump', 'export', 'import', 'index_rebuild', 'repl', 'restore']
    
    if len(sys.argv) < 2 or sys.argv[1] not in modes:
        sys.exit('ERROR: Must be called with one of the following verbs: %s' % ', '.join(modes))
    
    verb = sys.argv[1]
    prog = 'python -m rethinkdb'
    if sys.version_info < (2, 7) or (sys.version_info >= (3, 0) and sys.version_info < (3, 2)):
        prog += '.__main__' # Python versions 2.6, 3.0, and 3.1 do not support running packages
    prog += ' ' + verb
    argv = sys.argv[2:]
    
    if verb == 'dump':
        from . import _dump
        exit(_dump.main(argv))
    elif verb == 'export':
        from . import _export
        exit(_export.main(argv))
    elif verb == 'import':
        from . import _import
        exit(_import.main(argv))
    elif verb == 'index_rebuild':
        from . import _index_rebuild
        exit(_index_rebuild.main(argv))
    elif verb == 'repl':
        startInterpreter(prog, argv)
    elif verb == 'restore':
        from . import _restore
        exit(_restore.main(argv))