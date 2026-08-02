"""#																			||
---  #																			||
<(META)>:  #																	||
        docid: '202520ac-28ad-4b1f-ac39-103a98d765b2'  #							||
        name: Nchantd Input#													||
        description: >  #															||
        expirary: <[expiration]>  #													||
        version: <[version]>  #														||
        authority: document|this  #													||
        security: sec|lvl2  #														||
        <(WT)>: -32  #																||
"""
import sys
import logging
from os.path import abspath, dirname, join
logger = logging.getLogger(__name__)
import datetime as dt
from kahndor import kahndor
from kahndor.logma import Logma
there = abspath(join(''))
here = join(dirname(__file__), '')
log = False
logma = Logma(__name__)

def leftClickSignalLog(signal, level=0) -> None:
    logma.info(f'leftClickSignalLog called')
    return self

def mousePressEventLog(event, level=0) -> None:
    """ """
    if level >= 0:
        logma.info(f'Event {event.__dir__()}')
        logma.info(f'button {event.button()}')
        logma.info(f'buttons {event.buttons()}')
        logma.info(f'buttons {event.buttons().__dir__()}')
        logma.info(f'flags {event.flags()}')
        logma.info(f'flags {event.flags().__dir__()}')
        logma.info(f'globalPos {event.globalPos()}')
        logma.info(f'globalX {event.globalX()}')
        logma.info(f'globalY {event.globalY()}')
        logma.info(f'localPos {event.localPos()}')
        logma.info(f'screenPos {event.screenPos()}')
        logma.info(f'pos {event.pos()}')
        logma.info(f'source {event.source()}')
        logma.info(f'windowPos {event.windowPos()}')
        logma.info(f'x {event.x()}')
        logma.info(f'y {event.y()}')
        logma.info(f'modifiers {event.modifiers()}')
        logma.info(f'setTimestamp {event.setTimestamp(int(dt.datetime.timestamp(dt.datetime.now())))}')
        logma.info(f'timestamp {event.timestamp()}')
    if level >= 1:
        logma.info(f'Type {event.Type()}')
        logma.info(f'accept {event.accept()}')
        logma.info(f'ignore {event.ignore()}')
        logma.info(f'isAccepted {event.isAccepted()}')
        logma.info(f'registerEventType {event.registerEventType()}')
        logma.info(f'setAccepted {event.setAccepted(False)}')
        logma.info(f'spontaneous {event.spontaneous()}')
        logma.info(f'type {event.type()}')
        logma.info(f'ActionAdded {event.ActionAdded}')
        logma.info(f'ActionChanged {event.ActionChanged}')
        logma.info(f'ActionRemoved {event.ActionRemoved}')
        logma.info(f'ActivationChange {event.ActivationChange}')
        logma.info(f'ApplicationActivate {event.ApplicationActivate}')
        logma.info(f'ApplicationActivated {event.ApplicationActivated}')