from __future__ import annotations

from api.app_string_provider import AppStringProvider
from tools.checks.category import Category
from tools.checks.check_email_renderer import CheckEmailRenderer
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
