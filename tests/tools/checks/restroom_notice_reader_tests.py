from __future__ import annotations

from tools.checks.restroom_notice_reader import RestroomNoticeReader


def page( boxes: list[ str ] ) -> str:
   body = ''.join( f'<div class="box">{ box }</div>' for box in boxes )
   return f'<h2 id="notices">Notices</h2>{ body }<h2 id="animals">Animals</h2>'


def notices( boxes: list[ str ] ) -> list[ tuple[ str, bool ] ]:
   return [
      ( notice.restroom, notice.closure )
      for notice in RestroomNoticeReader.read( page( boxes ) )
   ]


def Test_Read_TestRainforestClosure_ExpectClosedRestroomOnly() -> None:
   found = notices( [
      (
         '<p><strong>Africa Savanna Loop Detour</strong> '
         'The washrooms, pathway in front of the African Rainforest Pavilion, '
         'and Multi-Faith Prayer and Spiritual Space are closed due to construction. '
         'The nearest accessible washroom is by the Africa Restaurant.</p>'
      ),
   ] )

   assert found == [ ( 'African Rainforest Restroom', True ) ]


def Test_Read_TestRestaurantClosure_ExpectOpenMentionsLeftOut() -> None:
   found = notices( [
      (
         '<p><strong>Africa Savanna Loop Closure Due to Paving</strong> '
         'The Africa Restaurant and associated washrooms will be closed. '
         'The nearest accessible washrooms are located at Simba Safari Restaurant. '
         'The African Rainforest Pavilion and its washrooms will remain open.</p>'
      ),
   ] )

   assert found == [ ( 'Africa Restaurant Restroom', True ) ]


def Test_Read_TestWeekdayWashroom_ExpectAlert() -> None:
   found = notices( [
      (
         '<p><strong>Now Through Friday, September 4</strong> '
         'Washrooms in the Zootique/Learning and Engagement building will be '
         'unavailable Monday to Friday due to Zoo Camp requirements. '
         'The nearest accessible washroom is located in the Discovery Zone, '
         'near the entrance to Splash Island.</p>'
      ),
   ] )

   assert found == [ ( 'Zootique Restroom', False ) ]


def Test_Read_TestOpenLate_ExpectAlert() -> None:
   found = notices( [
      (
         '<p><strong>Zootique</strong> '
         'The washroom in the Zootique/Learning and Engagement Building '
         'will open late due to maintenance.</p>'
      ),
   ] )

   assert found == [ ( 'Zootique Restroom', False ) ]


def Test_Read_TestFrontEntrance_ExpectClosure() -> None:
   found = notices( [
      (
         '<p><strong>Front entrance</strong> '
         'The women\'s washroom located at the front entrance will be closed '
         'for maintenance.</p>'
      ),
   ] )

   assert found == [ ( 'Entrance Restroom', True ) ]


def Test_Read_TestUnnamedWashroom_ExpectNothing() -> None:
   found = notices( [
      (
         '<p><strong>Discovery Zone Washroom Closure</strong> '
         'Due to maintenance, these washrooms are temporarily unavailable. '
         'Accessible alternate washrooms are located at the Zootique Gift Shop.</p>'
      ),
      (
         '<p><strong>Trail</strong> '
         'The First Nations Traditional Knowledge Trail, located in the '
         'Canadian Domain, is currently closed for maintenance.</p>'
      ),
   ] )

   assert found == []


def Test_Read_TestZoomobileAndDomain_ExpectBothClosures() -> None:
   found = notices( [
      (
         '<p><strong>Stops</strong> '
         'The washrooms at the Canadian Domain Zoomobile Stop are closed. '
         'The Canadian Domain washrooms are closed too.</p>'
      ),
   ] )

   assert found == [
      ( 'Canadian Domain Zoomobile Stop Restroom', True ),
      ( 'Canadian Domain Restroom', True ),
   ]
