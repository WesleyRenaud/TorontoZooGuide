from __future__ import annotations

from tools.checks.viewing_alert_sentence_builder import ViewingAlertSentenceBuilder


def Test_Sentences_TestThreeSentences_ExpectFirstTwo() -> None:
   assert ViewingAlertSentenceBuilder.sentences( 'One. Two. Three.' ) == 'One. Two.'


def Test_Write_TestHeadlineClosure_ExpectSentenceAtExhibit() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Polar Bear',
      'Tundra Trek',
      False,
      '',
      'The Polar Bear Underwater Viewing Area Is Closed for Maintenance.',
      '',
      [],
      [],
   ).text

   assert text == (
      'The polar bear underwater viewing area at Tundra Trek '
      'is closed for maintenance.'
   )


def Test_Write_TestOnDisplay_ExpectClosureAndWhere() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Polar Bear',
      'Tundra Trek',
      False,
      '',
      'The polar bear underwater viewing area is closed.',
      'The pool is still open.',
      [],
      [],
   ).text

   assert text == (
      'The polar bear underwater viewing area at Tundra Trek is closed. '
      'The pool is still open.'
   )


def Test_Write_TestIndoorOffDisplay_ExpectViewableOutside() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      True,
      'Indoor',
      'Indo-Malaya Pavilion Construction',
      'The Sumatran orangutan indoor habitat and a portion of the '
      'Indo-Malaya Pavilion are closed due to construction. '
      'Both entrances remain open. '
      'Orangutans may not be viewable during this time.',
      [ 'Indoor', 'Outdoor' ],
      [ 'Indoor' ],
   ).text

   assert text == (
      'The Sumatran orangutan indoor habitat is closed due to construction. '
      'The Sumatran orangutans can be seen in the outdoor habitat.'
   )


def Test_Write_TestFormerHabitat_ExpectCurrentExhibit() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Red Panda',
      'Africa Savanna',
      False,
      '',
      'Eurasia Wilds Loop Pathway Closure',
      'A portion of the pathway between the former red panda habitat, '
      'currently under construction, and the camels is closed due to construction.',
      [],
      [],
   ).text

   assert text == (
      'The red pandas can be seen at Africa Savanna. '
      'The former red panda habitat is under construction.'
   )


def Test_Write_TestWholeAnimalOffDisplay_ExpectOffDisplay() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Polar Bear',
      'Tundra Trek',
      True,
      '',
      'The polar bear underwater viewing area is closed.',
      '',
      [],
      [],
   ).text

   assert text == (
      'The polar bear is temporarily off display at Tundra Trek. '
      'The polar bear underwater viewing area at Tundra Trek is closed.'
   )


def Test_Write_TestTwoOfThreeEnclosures_ExpectBothListed() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Polar Bear',
      'Tundra Trek',
      True,
      'Indoor',
      'Habitat work',
      'The polar bear habitats are closed due to maintenance.',
      [ 'Indoor', 'Outdoor', 'Cave' ],
      [ 'Indoor', 'Outdoor' ],
   ).text

   assert text == (
      'The polar bear indoor habitat and outdoor habitat are closed due to maintenance. '
      'The polar bears can be seen in the cave.'
   )


def Test_Write_TestEveryEnclosure_ExpectWholeAnimal() -> None:
   text = ViewingAlertSentenceBuilder.write(
      'Sumatran Orangutan',
      'Indo-Malaya Pavilion',
      True,
      'Indoor',
      'Indo-Malaya Pavilion Construction',
      'The Sumatran orangutan indoor habitat at Indo-Malaya Pavilion is closed due to construction.',
      [ 'Indoor', 'Outdoor' ],
      [ 'Indoor', 'Outdoor' ],
   ).text

   assert text == (
      'The Sumatran orangutan is temporarily off display at Indo-Malaya Pavilion. '
      'The Sumatran orangutan indoor habitat at Indo-Malaya Pavilion is closed due to construction.'
   )

