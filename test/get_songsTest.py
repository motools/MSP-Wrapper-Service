'''
Created on Jun 11, 2009

@author: kurtjx
'''
import unittest
from MasterTest import *
import mopy


class GetSongsTest(MasterTest):

    def setUp(self):
        self.short_url_artist = 'kurtisrandom'
        self.short_url_non = 'flexboogie'
        self.uid_non = '8840037'
        self.uid_artist = '30650288'

    def test_get_songs(self):
        # do the song getting
        M = Myspace(short_url = self.short_url_artist)
        M.get_page()
        M.get_uid()
        M.is_artist()
        M.get_songs()
        # verify rdf w/ sparql
        graph = mopy.exportRDFGraph(M.mi)
        titles =[]
        for row in graph.query('''SELECT ?titles WHERE { ?track a <http://purl.org/ontology/mo/Track> . ?track <http://purl.org/dc/elements/1.1/title> ?titles . } '''):
            #print row
            title = '%s' % row
            titles.append(title)
        titles.sort()
        assert titles==[u'A Big Idea short mix', u'Blue92', u'Just to Get a Remix', u'Know What You Want feat Albie', u'Out of mi head feat Raquelle', u'Time  addicted to junk mix'], 'wrong set of titles: '+str(titles)
        
        # TODO: add test for playcounts and available_as
#        for row in graph.query('''SELECT ?titles WHERE { ?track a <http://purl.org/ontology/mo/Track> . ?track <http://purl.org/dc/elements/1.1/title> ?titles . }'''):
#            pass
#        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()