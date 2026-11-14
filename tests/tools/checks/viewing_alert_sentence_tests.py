from __future__ import annotations

from tools.checks.viewing_alert_sentence import ViewingAlertSentence


def Test_Sentences_TestThreeSentences_ExpectFirstTwo() -> None:
   assert ViewingAlertSentence.sentences( 'One. Two. Three.' ) == 'One. Two.'


def Test_Write_TestHeadlineClosure_ExpectSentenceAtExhibit() -> None:
   text = ViewingAlertSentence.write(
      'Polar Bear',
      'Tundra Trek',
      False,
      '',
      'The Polar Bear Underwater Viewing Area Is Closed for Maintenance.',
      '',
   )

   assert text == (
      'The polar bear underwater viewing area at Tundra Trek '
      'is closed for maintenance.'
   )


def Test_Write_TestOnDisplay_ExpectClosureAndWhere() -> None:
   text = ViewingAlertSentence.write(
      'Polar Bear',
      'Tundra Trek',
      False,
      '',
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
   )

   assert text == (
      'The polar bear underwater viewing area at Tundra Trek is closed. '
      'The pool is still open.'
   )


def Test_Write_TestIndoorOffDisplay_ExpectViewableOutside() -> None:
   text = ViewingAlertSentence.write(
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      True,
      'Indoor',
      'Indo-Malaya Pavilion Construction',
      'The Sumatran orangutan indoor habitat and a portion of the '
      'Indo-Malaya Pavilion are closed due to construction. '
      'Both entrances remain open. '
      'Orangutans may not be viewable during this time.',
   )

   assert text == (
      'The Sumatran orangutan indoor habitat and a portion of the '
      'Indo-Malaya Pavilion are closed due to construction. '
      'The Sumatran orangutans can be seen outside.'
   )


def Test_Write_TestFormerHabitat_ExpectCurrentExhibit() -> None:
   text = ViewingAlertSentence.write(
      'Red Panda',
      'Africa Savanna',
      False,
      '',
      'Eurasia Wilds Loop Pathway Closure',
      'A portion of the pathway between the former red panda habitat, '
      'currently under construction, and the camels is closed due to construction.',
   )

   assert text == (
      'The red pandas can be seen at Africa Savanna. '
      'The former red panda habitat is under construction.'
   )


def Test_Write_TestWholeAnimalOffDisplay_ExpectOffDisplay() -> None:
   text = ViewingAlertSentence.write(
      'Polar Bear',
      'Tundra Trek',
      True,
      '',
      'The polar bear underwater viewing area is closed.',
      '',
   )

   assert text == (
      'The polar bear is temporarily off display at Tundra Trek. '
      'The polar bear underwater viewing area at Tundra Trek is closed.'
   )
