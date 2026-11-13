from __future__ import annotations

from html import escape
from pathlib import Path
import re

from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .category import Category
from .check_exit_code import CheckExitCode
from .check_report_parser import CheckReportParser
from .color_token import ColorToken
from .color_tokens import ColorTokens
from .count import Count
from .detail_item import DetailItem
from .email_image import EmailImage
from .email_template_renderer import EmailTemplateRenderer
from .embedded_html import EmbeddedHtml
from .exhibit_region_colors import ExhibitRegionColors
from .font_tokens import FontTokens
from .paths import Paths
from .report import Report
from .section import Section
from .status_copy import StatusCopy


class CheckEmailRenderer():
   @classmethod
   def markup( cls, name: str, **params: object ) -> str:
      values: dict[ str, object ] = {
         'font': FontTokens.font( 'font-family-email' ),
         'green': ColorTokens.color( ColorToken.BRAND_PRIMARY ),
         'green_dark': ColorTokens.color( ColorToken.BRAND_PRIMARY_DARK ),
         'green_muted': ColorTokens.color( ColorToken.BRAND_PRIMARY_MUTED ),
         'green_highlight': ColorTokens.color( ColorToken.BRAND_ACCENT ),
         'leaf_edge': ColorTokens.color( ColorToken.BORDER_LEAF ),
         'text': ColorTokens.color( ColorToken.TEXT_PRIMARY ),
         'panel': ColorTokens.color( ColorToken.SURFACE_PANEL ),
         'white': ColorTokens.color( ColorToken.WHITE ),
         'danger': ColorTokens.color( ColorToken.DANGER ),
         'danger_soft': ColorTokens.color( ColorToken.DANGER_SOFT ),
      }
      values.update( params )
      return EmailTemplateRenderer.render( name, **values )


   @classmethod
   def check_kind( cls, check: str ) -> str:
      return AppStringProvider.reports()[ check ][ 'kind' ]


   @classmethod
   def section_name( cls, kind: str ) -> str:
      titles = {
         report[ 'kind' ]: report.get( 'section', report[ 'kind' ] )
         for report in AppStringProvider.reports().values()
         if 'kind' in report
      }
      return titles.get( kind, kind )


   @classmethod
   def text( cls, value: str ) -> str:
      return escape( value, quote=True )


   @classmethod
   def status_copy(
         cls,
         exit_code: int,
         error_count: int | None,
         fixed_count: int ) -> StatusCopy:
      if exit_code == CheckExitCode.COULD_NOT_FINISH or error_count is None:
         return StatusCopy(
            headline_color=ColorTokens.color( ColorToken.DANGER ),
            headline=AppStringProvider.format( 'checks.status.couldNotFinish' ),
            summary=AppStringProvider.format( 'checks.status.didNotFinish' ),
         )

      if error_count == 0 and fixed_count == 0:
         return StatusCopy(
            headline_color=ColorTokens.color( ColorToken.BRAND_PRIMARY ),
            headline=AppStringProvider.format( 'checks.status.noneDetected' ),
            summary=AppStringProvider.format( 'checks.status.websiteMatches' ),
         )

      if error_count == 0:
         return StatusCopy(
            headline_color=ColorTokens.color( ColorToken.BRAND_PRIMARY ),
            headline=CheckReportParser.format_detected( fixed_count, fixed_count ),
            summary=AppStringProvider.format( 'checks.status.websiteMatches' ),
         )

      return StatusCopy(
         headline_color=ColorTokens.color( ColorToken.DANGER ),
         headline=CheckReportParser.format_detected( error_count + fixed_count, fixed_count ),
         summary=AppStringProvider.format( 'checks.status.differ' ),
      )


   @classmethod
   def count_kinds( cls ) -> dict[ str, list[ str ] ]:
      return {
         AppStringProvider.format( 'site.nav.animals' ): [
            cls.check_kind( 'animalList' ),
            cls.check_kind( 'closureOffDisplay' ),
            cls.check_kind( 'closureUpdate' ),
            cls.check_kind( 'viewingHours' ),
            cls.check_kind( 'seasonalOffDisplay' ),
            cls.check_kind( 'temporaryOffDisplay' ),
         ],
         AppStringProvider.format( 'checks.countNames.exhibits' ): [
            cls.check_kind( 'seasonalExhibit' ),
         ],
         AppStringProvider.format( 'site.nav.wildEncounters' ): [
            cls.check_kind( 'wildEncounter' ),
         ],
         AppStringProvider.format( 'reports.guardiansTalk.section' ): [
            cls.check_kind( 'guardiansTalk' ),
         ],
         AppStringProvider.format( 'map.filter.attractions' ): [
            cls.check_kind( 'seasonalAttraction' ),
            cls.check_kind( 'attractionList' ),
            cls.check_kind( 'attractionWindow' ),
         ],
         AppStringProvider.format( 'map.filterTypes.restaurant' ): [
            cls.check_kind( 'seasonalRestaurant' ),
            cls.check_kind( 'restaurantList' ),
            cls.check_kind( 'restaurantWindow' ),
         ],
         AppStringProvider.format( 'checks.countNames.giftShops' ): [
            cls.check_kind( 'seasonalGiftShop' ),
            cls.check_kind( 'giftShopList' ),
            cls.check_kind( 'giftShopWindow' ),
         ],
         AppStringProvider.format( 'checks.countNames.drinkingFountains' ): [
            cls.check_kind( 'seasonalDrinkingFountain' ),
         ],
         cls.check_kind( 'zooHours' ): [
            cls.check_kind( 'zooHours' ),
         ],
      }


   @classmethod
   def issue_total( cls, label: str, sections: list[ Section ] ) -> int:
      kinds = cls.count_kinds().get( label, [] )
      return sum(
         category.count
         for section in sections
         if section.kind in kinds
         for category in section.categories
      )


   @classmethod
   def count_total( cls, count: Count, sections: list[ Section ] ) -> int:
      return max( count.count, cls.issue_total( count.label, sections ) )


   @classmethod
   def count_cell( cls, label: str, count: int, all_fixed: bool ) -> str:
      clear = all_fixed
      return cls.markup(
         'count_cell',
         label=cls.text( label ),
         count=cls.text( str( count ) ),
         number_color=(
            ColorTokens.color( ColorToken.BRAND_PRIMARY )
            if clear
            else ColorTokens.color( ColorToken.DANGER )
         ),
         background=(
            ColorTokens.color( ColorToken.WHITE )
            if clear
            else ColorTokens.color( ColorToken.DANGER_SOFT )
         ),
         edge=(
            ColorTokens.color( ColorToken.BORDER_LEAF )
            if clear
            else ColorTokens.color( ColorToken.DANGER )
         ),
      )


   @classmethod
   def count_row( cls, counts: list[ Count ], sections: list[ Section ] ) -> str:
      cells = ''.join(
         cls.count_cell(
            count.label,
            cls.count_total( count, sections ),
            count.count == 0,
         )
         for count in counts
      )

      if len( counts ) < 2:
         cells += cls.markup( 'blank_count_cell' )

      return cls.markup( 'row', cells=cells )


   @classmethod
   def count_grid( cls, report: Report ) -> str:
      rows = []
      row: list[ Count ] = []

      for count in report.counts:
         row.append( count )

         if len( row ) < 2:
            continue

         rows.append( cls.count_row( row, report.sections ) )
         row = []

      if row:
         rows.append( cls.count_row( row, report.sections ) )

      return cls.markup( 'count_grid', rows=''.join( rows ) )


   @classmethod
   def detail_text( cls, detail: str ) -> str:
      label, separator, value = detail.partition( ': ' )

      if not separator:
         return cls.text( detail )

      return cls.markup(
         'detail_label',
         label=cls.text( label ),
         separator=separator,
         value=cls.text( value ),
      )


   @classmethod
   def exhibit_pill( cls, exhibit: str ) -> str:
      colors = ExhibitRegionColors.place_colors( exhibit )
      safe = cls.text( exhibit )
      return cls.markup(
         'exhibit_pill',
         exhibit=safe,
         background=colors.background,
         foreground=colors.foreground,
      )


   @classmethod
   def item_label( cls, title: str ) -> str:
      species, separator, exhibit = title.rpartition(
         AppStringProvider.format( 'format.middleDotJoin' )
      )

      if separator == '':
         return cls.text( title )

      colors = ExhibitRegionColors.place_colors( exhibit )
      name = f'<span style="color:{ colors.foreground };">{ cls.text( species ) }</span>'
      return f'{ name }{ separator }{ cls.exhibit_pill( exhibit ) }'


   @classmethod
   def detail_rows( cls, item: DetailItem ) -> str:
      rows = [
         cls.markup(
            'row',
            cells=cls.markup( 'item_title', label=cls.item_label( item.title ) ),
         )
      ]

      for detail in item.details:
         rows.append(
            cls.markup(
               'row',
               cells=cls.markup( 'detail_line', detail=cls.detail_text( detail ) ),
            )
         )

      return ''.join( rows )


   @classmethod
   def local_image( cls, photo: str ) -> Path:
      return Paths.ROOT / photo


   @classmethod
   def image_src( cls, photo: str ) -> str:
      if photo.startswith( 'http://' ) or photo.startswith( 'https://' ):
         return photo

      return cls.local_image( photo ).as_uri()


   @classmethod
   def embed_local_images( cls, html: str ) -> EmbeddedHtml:
      sources = re.findall( r'src="(file:[^"]+)"', html )
      images = [ EmailImage.from_file_uri( src ) for src in sources ]
      web_sources = re.findall( r'src="(https?://[^"]+)"', html )
      images.extend( EmailImage.from_url( src ) for src in web_sources )
      sources.extend( web_sources )

      for src, image in zip( sources, images, strict=True ):
         html = html.replace( f'src="{ src }"', f'src="{ image.src() }"', 1 )

      return EmbeddedHtml( html=html, images=images )


   @classmethod
   def photo_and_details( cls, details: list[ str ] ) -> tuple[ str, list[ str ] ]:
      prefix = AppStringProvider.format( 'checks.photo' )
      photo = ''
      rest: list[ str ] = []

      for detail in details:
         if photo == '' and detail.startswith( prefix ):
            photo = detail[ len( prefix ): ]
            continue

         rest.append( detail )

      return photo, rest


   @classmethod
   def photo_markup( cls, photo: str, alt: str, border: str ) -> str:
      values = {
         'src': cls.text( cls.image_src( photo ) ),
         'alt': cls.text( alt ),
      }
      name = 'animal_photo'

      if photo.startswith( ( 'images/details/exhibits/', 'images/details/regions/' ) ):
         name = 'detail_icon'
      else:
         values[ 'border' ] = border

      return cls.markup( name, **values )


   @classmethod
   def corrected_animal_rows( cls, item: DetailItem ) -> str:
      species, separator, exhibit = item.title.rpartition(
         AppStringProvider.format( 'format.middleDotJoin' )
      )

      if separator == '':
         alt = item.title
         border = ColorTokens.color( ColorToken.TEXT_PRIMARY )
      else:
         alt = species
         border = ExhibitRegionColors.place_colors( exhibit ).foreground

      label = cls.item_label( item.title )
      photo_url, details = cls.photo_and_details( item.details )
      photo = ''

      if photo_url != '':
         photo = cls.photo_markup( photo_url, alt, border )

      return cls.markup(
         'row',
         cells=cls.markup(
            'corrected_animal',
            photo=photo,
            label=label,
            details=''.join(
               cls.markup( 'corrected_detail', detail=cls.detail_text( detail ) )
               for detail in details
            ),
         ),
      )


   @classmethod
   def rows_for( cls, category_title: str, item: DetailItem ) -> str:
      photo, _details = cls.photo_and_details( item.details )

      if photo != '' or (
         AppStringProvider.format( 'format.middleDotJoin' ) in item.title
         and cls.fixed_category( category_title )
      ):
         return cls.corrected_animal_rows( item )

      return cls.detail_rows( item )


   @classmethod
   def fixed_category( cls, title: str ) -> bool:
      return title in (
         AppStringProvider.format( 'checks.closureOffDisplayReturningTomorrow' ),
         AppStringProvider.format( 'checks.offForSeasonWebsiteOnly' ),
         AppStringProvider.format( 'checks.offForSeasonAppOnly' ),
         AppStringProvider.format( 'checks.temporaryOffDisplayAppOnly' ),
         AppStringProvider.format( 'checks.temporaryOffDisplayWebsiteOnly' ),
      )


   @classmethod
   def recorded_fix( cls, category: Category ) -> bool:
      phrases = (
         AppStringProvider.format( 'checks.extendedClosedForSeasonThrough' ),
         AppStringProvider.format( 'checks.setClosedForSeasonFrom' ),
         AppStringProvider.format( 'checks.setOpenForSeason' ),
         AppStringProvider.format( 'checks.setOpenForSeasonFrom' ),
         AppStringProvider.format( 'checks.setScheduleFrom' ),
         AppStringProvider.format( 'checks.removedHours' ),
         AppStringProvider.format( 'checks.removedSchedule' ),
         AppStringProvider.format( 'checks.setHours' ),
         AppStringProvider.format( 'checks.updatedHours' ),
      )

      if category.items == []:
         return False

      return all(
         any( phrase in detail for phrase in phrases for detail in item.details )
         for item in category.items
      )


   @classmethod
   def category_is_fixed( cls, category: Category ) -> bool:
      return cls.fixed_category( category.title ) or cls.recorded_fix( category )


   @classmethod
   def category_block( cls, category: Category ) -> str:
      if category.count == 0:
         return ''

      number_color = ColorTokens.color( ColorToken.BRAND_PRIMARY )
      title_color = ColorTokens.color( ColorToken.BRAND_PRIMARY_DARK )

      if category.count > 0 and cls.category_is_fixed( category ):
         title_color = ColorTokens.color( ColorToken.BRAND_PRIMARY )
      elif category.count > 0:
         number_color = ColorTokens.color( ColorToken.DANGER )
         title_color = ColorTokens.color( ColorToken.DANGER )

      title_cell = cls.markup(
         'category_title',
         title=cls.text( category.title ),
         title_color=title_color,
      )
      count_badge = cls.markup(
         'category_count',
         number_color=number_color,
         count=cls.text( str( category.count ) ),
      )
      rows = [ cls.markup( 'row', cells=title_cell + count_badge ) ]
      rows.extend(
         cls.rows_for( category.title, item )
         for item in category.items
      )
      return ''.join( rows )


   @classmethod
   def section_card( cls, section: Section ) -> str:
      title = cls.markup(
         'section_title',
         title=cls.text( cls.section_name( section.kind ) ),
      )
      rows = [ cls.markup( 'row', cells=title ) ]

      if section.categories:
         rows.append(
            cls.markup(
               'section_categories',
               categories=''.join(
                  cls.category_block( category )
                  for category in section.categories
               ),
            )
         )

      return cls.markup( 'section_card', rows=''.join( rows ) )


   @classmethod
   def grouped_sections( cls, sections: list[ Section ], kinds: list[ str ] ) -> list[ Section ]:
      grouped: dict[ str, list[ Section ] ] = {
         kind: []
         for kind in kinds
      }

      for section in sections:
         if section.kind in grouped:
            grouped[ section.kind ].append( section )

      merged = []

      for kind in kinds:
         parts = grouped[ kind ]

         if parts == []:
            continue

         categories = [
            category
            for section in parts
            for category in section.categories
         ]
         merged.append( Section( kind, parts[ 0 ].day, parts[ 0 ].note, categories ) )

      return merged


   @classmethod
   def animal_sections( cls, sections: list[ Section ] ) -> list[ Section ]:
      return cls.grouped_sections( sections, [
         cls.check_kind( 'animalList' ),
         cls.check_kind( 'closureOffDisplay' ),
         cls.check_kind( 'seasonalOffDisplay' ),
         cls.check_kind( 'temporaryOffDisplay' ),
      ] )


   @classmethod
   def attraction_sections( cls, sections: list[ Section ] ) -> list[ Section ]:
      return cls.grouped_sections( sections, [
         cls.check_kind( 'seasonalAttraction' ),
         cls.check_kind( 'attractionList' ),
         cls.check_kind( 'attractionWindow' ),
      ] )


   @classmethod
   def restaurant_sections( cls, sections: list[ Section ] ) -> list[ Section ]:
      return cls.grouped_sections( sections, [
         cls.check_kind( 'seasonalRestaurant' ),
         cls.check_kind( 'restaurantList' ),
         cls.check_kind( 'restaurantWindow' ),
      ] )


   @classmethod
   def gift_shop_sections( cls, sections: list[ Section ] ) -> list[ Section ]:
      return cls.grouped_sections( sections, [
         cls.check_kind( 'seasonalGiftShop' ),
         cls.check_kind( 'giftShopList' ),
         cls.check_kind( 'giftShopWindow' ),
      ] )


   @classmethod
   def merged_categories( cls, categories: list[ Category ] ) -> list[ Category ]:
      merged: list[ Category ] = []
      by_title: dict[ str, Category ] = {}

      for category in categories:
         current = by_title.get( category.title )

         if current is None:
            current = Category( category.title, category.count, list( category.items ) )
            by_title[ category.title ] = current
            merged.append( current )
            continue

         current.count += category.count
         current.items.extend( category.items )

      return merged


   @classmethod
   def has_issue( cls, categories: list[ Category ] ) -> bool:
      return any( category.count > 0 for category in categories )


   @classmethod
   def combined_animals( cls, sections: list[ Section ] ) -> Section | None:
      sources = cls.animal_sections( sections )
      categories = [
         category
         for section in sources
         for category in section.categories
      ]

      if not cls.has_issue( categories ):
         return None

      return Section( AppStringProvider.format( 'site.nav.animals' ), sources[ 0 ].day, '', categories )


   @classmethod
   def combined_attractions( cls, sections: list[ Section ] ) -> Section | None:
      sources = cls.attraction_sections( sections )
      categories = [
         category
         for section in sources
         for category in section.categories
      ]

      if not cls.has_issue( categories ):
         return None

      return Section(
         AppStringProvider.format( 'map.filter.attractions' ),
         sources[ 0 ].day,
         '',
         categories,
      )


   @classmethod
   def combined_restaurants( cls, sections: list[ Section ] ) -> Section | None:
      sources = cls.restaurant_sections( sections )
      categories = cls.merged_categories( [
         category
         for section in sources
         for category in section.categories
      ] )

      if not cls.has_issue( categories ):
         return None

      return Section(
         AppStringProvider.format( 'map.filterTypes.restaurant' ),
         sources[ 0 ].day,
         '',
         categories,
      )


   @classmethod
   def combined_gift_shops( cls, sections: list[ Section ] ) -> Section | None:
      sources = cls.gift_shop_sections( sections )
      categories = cls.merged_categories( [
         category
         for section in sources
         for category in section.categories
      ] )

      if not cls.has_issue( categories ):
         return None

      return Section(
         AppStringProvider.format( 'checks.countNames.giftShops' ),
         sources[ 0 ].day,
         '',
         categories,
      )


   @classmethod
   def notable_sections( cls, report: Report ) -> list[ Section ]:
      sections = report.sections
      notable = []
      animals = cls.combined_animals( sections )
      attractions = cls.combined_attractions( sections )
      restaurants = cls.combined_restaurants( sections )
      gift_shops = cls.combined_gift_shops( sections )
      animals_placed = False
      attractions_placed = False
      restaurants_placed = False
      gift_shops_placed = False
      folded_animals = {
         section.kind
         for section in cls.animal_sections( sections )
      }
      folded_attractions = {
         section.kind
         for section in cls.attraction_sections( sections )
      }
      folded_restaurants = {
         section.kind
         for section in cls.restaurant_sections( sections )
      }
      folded_gift_shops = {
         section.kind
         for section in cls.gift_shop_sections( sections )
      }
      schedule_sections = {
         section.kind: section
         for section in cls.grouped_sections( sections, [
            cls.check_kind( 'wildEncounter' ),
            cls.check_kind( 'guardiansTalk' ),
         ] )
      }
      placed_schedules: set[ str ] = set()

      for section in sections:
         if section.kind in folded_animals:
            if animals is not None and not animals_placed:
               notable.append( animals )
               animals_placed = True

            continue

         if section.kind in folded_attractions:
            if attractions is not None and not attractions_placed:
               notable.append( attractions )
               attractions_placed = True

            continue

         if section.kind in folded_restaurants:
            if restaurants is not None and not restaurants_placed:
               notable.append( restaurants )
               restaurants_placed = True

            continue

         if section.kind in folded_gift_shops:
            if gift_shops is not None and not gift_shops_placed:
               notable.append( gift_shops )
               gift_shops_placed = True

            continue

         if section.kind in schedule_sections:
            if section.kind not in placed_schedules:
               placed_schedules.add( section.kind )
               card = schedule_sections[ section.kind ]

               if cls.has_issue( card.categories ):
                  notable.append( card )

            continue

         if cls.has_issue( section.categories ):
            notable.append( section )

      return notable


   @classmethod
   def render_html( cls, body: str, exit_code: int ) -> str:
      report = CheckReportParser.parse_report( body )
      day = report.sections[ 0 ].day
      status = cls.status_copy( exit_code, report.error_count, report.fixed_count )
      date_line = cls.markup( 'date_line', day=cls.text( DateValues.format_display_weekday( day ) ) )
      sections = cls.notable_sections( report )
      content = (
         cls.markup( 'header', title_padding='6px 24px 2px', date_line=date_line )
         + cls.markup(
            'status',
            headline_color=status.headline_color,
            headline=cls.text( status.headline ),
            summary=cls.text( status.summary ),
         )
         + cls.count_grid( report )
         + ''.join( cls.section_card( section ) for section in sections )
      )
      return cls.markup( 'document', content=content )
