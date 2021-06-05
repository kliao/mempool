#!/bin/bash

DESTDIR=/Users/kevinliao/github/mempool/web/queue #/dev/shm/mempool-btc
BITCOINCLI="/usr/local/bin/bitcoin-cli"
MEMPOOLHOME=/Users/kevinliao/github/mempool/
TMPFILE=$DESTDIR/rawdump.txt
export DESTDIR MEMPOOLHOME

cd $MEMPOOLHOME

# create ram-disk directory if it does not exists
if [ ! -e $DESTDIR ]; then
    mkdir -p $DESTDIR/LOCK
    # read mempool.log once sequentially to quickly load it in buffers
    cat mempool.log > /dev/null
    ./mkdata.sh
    rmdir $DESTDIR/LOCK
fi

# create mempool statistics, protected by LOCK
if ! mkdir $DESTDIR/LOCK 2>/dev/null; then
    exit
fi
#$BITCOINCLI getrawmempool true > $TMPFILE
#python3 mempool_sql.py < $TMPFILE
python3 mempool_sql.py < mempool_test_data.json
rmdir $DESTDIR/LOCK

# update ram-disk directory, protected by DATALOCK
if ! mkdir $DESTDIR/DATALOCK 2>/dev/null; then
    exit
fi
./updatedata.sh
rmdir $DESTDIR/DATALOCK
