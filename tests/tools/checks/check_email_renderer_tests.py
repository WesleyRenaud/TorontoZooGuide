from __future__ import annotations

from api.app_string_provider import AppStringProvider
from tools.checks.category import Category
from tools.checks.check_email_renderer import CheckEmailRenderer
from tools.checks.color_token import ColorToken
from tools.checks.color_tokens import ColorTokens
from tools.checks.detail_item import DetailItem


def Test_CategoryIsFixed_TestExtendedViewingAlert_ExpectFixed() -> None:
   detail = (
      AppStringProvider.format( 'checks.extendedViewingAlertThrough' )
      + 'December 14, 2026'
      + AppStringProvider.format( 'checks.period' )
   )
   category = Category(
      AppStringProvider.format( 'checks.animalAlerts' ),
      1,
      [
         DetailItem(
            'Polar Bear · Tundra Trek',
            [ detail ],
         ),
      ],
   )

   assert CheckEmailRenderer.category_is_fixed( category ) == True


def Test_CategoryIsFixed_TestExtendedClosureUpdate_ExpectFixed() -> None:
   detail = (
      AppStringProvider.format( 'checks.extendedUpdateThrough' )
      + 'December 14, 2026'
      + AppStringProvider.format( 'checks.period' )
   )
   category = Category(
      'Windows which do not align',
      1,
      [
         DetailItem(
            'Indo-Malaya Pavilion Construction',
            [ detail ],
         ),
      ],
   )

   assert CheckEmailRenderer.category_is_fixed( category ) == True


def Test_CategoryIsFixed_TestSetClosureUpdate_ExpectFixed() -> None:
   phrases = (
      'checks.setUpdateFor',
      'checks.setUpdateFrom',
      'checks.endedUpdate',
   )
   category = Category(
      AppStringProvider.format( 'checks.websiteOnly' ),
      len( phrases ),
      [
         DetailItem( 'Tuesday, November 17', [ AppStringProvider.format( phrase ) ] )
         for phrase in phrases
      ],
   )

   assert CheckEmailRenderer.category_is_fixed( category ) == True


def Test_CategoryIsFixed_TestViewingHours_ExpectFixed() -> None:
   phrases = (
      'checks.setViewingHoursFrom',
      'checks.removedViewingHours',
      'checks.extendedViewingHoursThrough',
      'checks.trimmedViewingHoursThrough',
   )
   category = Category(
      'Windows which do not align',
      len( phrases ),
      [
         DetailItem( 'Otter · Americas Pavilion', [ AppStringProvider.format( phrase ) ] )
         for phrase in phrases
      ],
   )

   assert CheckEmailRenderer.category_is_fixed( category ) == True


def Test_CorrectedAnimalRows_TestZooEvent_ExpectDescriptionThenAction() -> None:
   action = AppStringProvider.format( 'checks.addedZooEvent' )
   description = 'Journey through the lanterns.'
   title = (
      'Glow In The Wild'
      + AppStringProvider.format( 'format.subtitleSeparator' )
      + description
   )
   item = DetailItem(
      title,
      [
         AppStringProvider.format( 'checks.photo' ) + 'https://example.com/glow.jpg',
         action,
      ],
   )

   html = CheckEmailRenderer.corrected_animal_rows( item )
   muted = ColorTokens.color( ColorToken.BRAND_PRIMARY_MUTED )

   assert html.index( description ) < html.index( action )
   assert 'font-weight:400' in html
   assert f'color:{ muted }' in html
   assert html.index( 'font-weight:400' ) < html.index( action )
