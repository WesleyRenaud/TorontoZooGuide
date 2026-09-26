from __future__ import annotations

from typing import Any

import pytest

from api.shared.value_conversion import ValueConversion


@pytest.mark.parametrize(
   'value, expected',
   [
      ( True, True ),
      ( False, False ),
      ( 1, True ),
      ( 0, False ),
      ( None, False ),
      ( 'true', False )
   ]
)
def Test_AsBoolean( value: Any, expected: bool ) -> None:
   flag = ValueConversion.as_boolean( value )

   assert flag is expected


def Test_AsTrimmedString_TestNone_ExpectEmpty() -> None:
   value = None

   trimmed = ValueConversion.as_trimmed_string( value )

   assert trimmed == ''


def Test_AsTrimmedString_TestWhitespace_ExpectTrimmed() -> None:
   name = 'Lion'
   value = f'  { name }  '

   trimmed = ValueConversion.as_trimmed_string( value )

   assert trimmed == name


def Test_AsTrimmedString_TestNumber_ExpectCoerced() -> None:
   value = 42

   trimmed = ValueConversion.as_trimmed_string( value )

   assert trimmed == str( value )


def Test_AsNullableString_TestNone_ExpectNone() -> None:
   value = None

   trimmed = ValueConversion.as_nullable_string( value )

   assert trimmed is None


def Test_AsNullableString_TestBlank_ExpectNone() -> None:
   value = '   '

   trimmed = ValueConversion.as_nullable_string( value )

   assert trimmed is None


def Test_AsNullableString_TestWhitespace_ExpectTrimmed() -> None:
   name = 'Lion'
   value = f'  { name }  '

   trimmed = ValueConversion.as_nullable_string( value )

   assert trimmed == name


def Test_AsSingletonList_TestNone_ExpectEmpty() -> None:
   value = None

   result = ValueConversion.as_singleton_list( value )

   assert result == []


def Test_AsSingletonList_TestMessage_ExpectList() -> None:
   message = 'Alert message.'

   result = ValueConversion.as_singleton_list( message )

   assert result == [ message ]


def Test_AsNullableBoolean_TestNone_ExpectNone() -> None:
   value = None

   flag = ValueConversion.as_nullable_boolean( value )

   assert flag is None
