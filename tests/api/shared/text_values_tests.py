from __future__ import annotations

from api.shared.text_values import TextValues


def Test_NormalizeForMatching_TestMixedCaseAndWhitespace_ExpectLowercaseTrimmed() -> None:
   name = 'African Lion'
   value = f'  { name }  '

   normalized = TextValues.normalize_for_matching( value )

   assert normalized == name.lower()


def Test_NormalizeForMatching_TestNone_ExpectEmptyString() -> None:
   value = None

   normalized = TextValues.normalize_for_matching( value )

   assert normalized == ''


def Test_Spaced_TestKey_ExpectSpacesAroundKey() -> None:
   assert TextValues.spaced( 'polar bear' ) == ' polar bear '


def Test_Plural_TestKey_ExpectTrailingS() -> None:
   assert TextValues.plural( 'polar bear' ) == 'polar bears'


def Test_Beside_TestTwoStrings_ExpectSpaceBetween() -> None:
   assert TextValues.beside( 'polar bear', 'pool' ) == 'polar bear pool'
