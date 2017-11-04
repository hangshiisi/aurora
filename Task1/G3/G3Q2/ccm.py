#!/usr/bin/env python

from cmd import Cmd

class MyPrompt(Cmd):
    counter = 0 

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        #print "length is %d %s " % (len(args), args)
        if len(args) < 1:
        	return 
            
        name = args
        print "Helllo, %s" % name
    	return False

    def do_select(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) < 1:
        	return 
        ss1 = """
      forigin |    fto     |  fdate     |  arrival  | scarrier | departure_time | flight_num
--------------+------------+------------+----------+-----------+---------+----------------+------------
          SLC |    BFL     | 2008-01-06 |   16:20   |      2O3 |          11:40 |       3755

(1 rows)
        """
        
        ss2 = """
      forigin |    fto     |  fdate      | arrival   | scarrier | departure_time | flight_num
--------------+------------+------------+----------+-----------+---------+----------------+------------
          JAX |    DFW     |  2008-09-09 |   14:55   |      845 |          07:25 |       3627

(1 rows)
        """


        if self.counter == 0: 
        	print ss1 
        else: 
        	print ss2 

        self.counter += 1 

        return 

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit

    def emptyline(self):
         pass

    def do_describe(self, args): 
    	ss = """
CREATE TABLE test.g3q2 (
    fdate text,
    forigin text,
    fto text,
    sto text,
    arrival text,
    carrier text,
    depart text,
    flight int,
    number int,
    scarrier text,
    PRIMARY KEY (fdate, forigin, fto, sto)
) WITH CLUSTERING ORDER BY (forigin ASC, fto ASC, sto ASC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';

""" 
        print ss 

if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = 'cqlsh> '
    prompt.cmdloop('Connecting to cqlsh...')


