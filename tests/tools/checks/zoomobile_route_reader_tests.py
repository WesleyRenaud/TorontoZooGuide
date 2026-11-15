from __future__ import annotations

from tools.checks.zoomobile_route_reader import ZoomobileRouteReader


SUMMER = '''
<p>The Zoomobile currently stops at the following stations:</p>
<ul>
<li>Main Station</li>
<li>Canadian Domain Station</li>
<li>African Savanna Station</li>
<li>Tundra Trek Station</li>
<li>Eurasia Wilds Station</li>
</ul>
'''
WINTER = '''
<p>The Zoomobile is currently operating on its winter route and stops at the following stations:</p>
<ul>
<li>Eurasia</li>
<li>Tundra Trek</li>
<li>Main Station (Currently located in Indo-Malaya)</li>
</ul>
'''


def Test_Parse_TestSummerStations_ExpectSummer() -> None:
   route = ZoomobileRouteReader.parse( SUMMER )

   assert route != None
   assert route.route == 'summer'


def Test_Parse_TestWinterRoute_ExpectWinter() -> None:
   route = ZoomobileRouteReader.parse( WINTER )

   assert route != None
   assert route.route == 'winter'
