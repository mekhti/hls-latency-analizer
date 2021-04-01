#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import m3u8
import argparse
import datetime
import re


def main():
    argParser = argparse.ArgumentParser(description="App for calculating of the HLS latency", prog="hla.py")
    argParser.add_argument('source_uri', type=str, help="Set HLS stream URL that points to the .m3u8 file")
    arguments = argParser.parse_args()
    sPlaylist = m3u8.load(arguments.source_uri)
    playlistObj = m3u8.loads(sPlaylist.dumps())

    for i in range(len(playlistObj.playlists)):
        print("For chunk: ", playlistObj.playlists[i].uri)
        variantPlaylist = m3u8.loads(m3u8.load(sPlaylist.base_uri + playlistObj.playlists[i].uri).dumps())
        for j in range(len(variantPlaylist.segments)):
            nextSegment = variantPlaylist.segments[j]
            segmentDateTime = str(nextSegment.current_program_date_time)
            segmentDateTime = re.compile('\W00:00$').sub('', segmentDateTime)
            print("For segment:", nextSegment.uri)
            print("\tCurrent time:", datetime.datetime.utcnow())
            print("\tCreation time:", segmentDateTime)
            latency = datetime.datetime.strptime(str(datetime.datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f').timestamp() \
                      - datetime.datetime.strptime(segmentDateTime, '%Y-%m-%d %H:%M:%S.%f').timestamp()
            print("\tPlaylist recieving latency: ", latency, end="\n\n")

if __name__ == '__main__':
    print("Current date and time:", datetime.datetime.utcnow())
    main()
