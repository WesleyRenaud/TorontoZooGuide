from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.attractions.data_access.attraction_info_link_mapper import AttractionInfoLinkMapper
from api.attractions.domain.attraction_info_link import AttractionInfoLink


NAME = 'Splash Island'
INFO_LINK = 'https://www.torontozoo.com/tz/splash'


def Test_MapRecord_TestRow_ExpectNameAndInfoLink() -> None:
   row = make_row( {
      'NAME': NAME,
      'INFO_LINK': INFO_LINK,
   } )

   attraction = AttractionInfoLinkMapper.map_record( row )

   assert attraction == AttractionInfoLink( name=NAME, info_link=INFO_LINK )
