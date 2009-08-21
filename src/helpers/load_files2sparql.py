'''
Created on Jul 15, 2009

loads a directory of RDF files into the SPARQL endpoint

@author: kurtjx
'''


import sys
import getopt
import os

sys.path.append('..')

from ODBC import ODBC
os.chdir('..')

help_message = '''
utility to dump a directory of files into a store
-p     --path     <path to directory of files to dump in store>
-g     --graph    <graph to add files to>
note only files ending with '.rdf' will be added
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def go_thru_files(path, graph, cursor):
    files = os.listdir(path)
    for f in files:
        if f.endswith('.rdf'):
            print 'adding %s to graph %s' % (f,graph)
            cursor.execute("DB.DBA.RDF_LOAD_RDFXML_MT (file_to_string('"+ os.path.join(path,f)+"'), 'junk', '"+graph+"')")

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:vp:g:", ["help", "output=", "path=", "graph="])
        except getopt.error, msg:
            raise Usage(msg)

        path = ''
        graph = 'http://dbtune.org/myspace/'

        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
            if option in ("-p", "--path"):
                path = value
            if option in ("-g", "--graph"):
                graph = value


        if path=='':
            raise Usage('must supply a path')
        else:
            DB = ODBC()
            con = DB.connect()
            cur = con.cursor()
            go_thru_files(path, graph, cur)
            cur.close()
            con.close()

    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())