#!/usr/bin/env python

# canScan - CANopen discovery/scanning tool
#
# https://github.com/dankamongmen/canscan

from __future__ import print_function
import node
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Probe and listen for CANopen')
    parser.add_argument('device', help='link/can network device')
    parser.add_argument('--scansdo', help='comma-delimited list of nodes to scan',
                        type=lambda x: x.split(','))
    args = parser.parse_args()
    node.Node(args.device)
    scanNodes = []
    scanSet = set(scanNodes)
    if args.scansdo:
        for noderange in args.scansdo:
            try:
                node = int(noderange)
                if node < 0 or node > 0x7f:
                    raise SystemExit('Invalid node ID: %d' % node)
                scanSet.add(node)
            except ValueError:
                rlist = ([int(n) for n in noderange.split('-')])
                if len(rlist) != 2:
                    raise SystemExit('Invalid node ID range: %s' % noderange)
                if rlist[0] < 0 or rlist[1] < 0:
                    raise SystemExit('Invalid node ID range: %s' % noderange)
                if rlist[0] > 0x7f or rlist[1] > 0x7f:
                    raise SystemExit('Invalid node ID range: %s' % noderange)
                if rlist[0] > rlist[1]:
                    raise SystemExit('Invalid node ID range: %s' % noderange)
                r = set(range(rlist[0], rlist[1] + 1))
                scanSet.update(r)
        scanNodes = list(scanSet)
    print('Node scan list:', scanNodes)