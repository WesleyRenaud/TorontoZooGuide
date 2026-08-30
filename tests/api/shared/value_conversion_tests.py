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
   assert ValueConversion.as_boolean( value ) is expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, '' ),
      ( '  Lion  ', 'Lion' ),
      ( 42, '42' ),
   ]
)
def Test_AsTrimmedString( value: Any, expected: str ) -> None:
   assert ValueConversion.as_trimmed_string( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, None ),
      ( '   ', None ),
      ( '  Lion  ', 'Lion' ),
   ]
)
def Test_AsNullableString( value: Any, expected: str | None ) -> None:
   assert ValueConversion.as_nullable_string( value ) == expected


@pytest.mark.parametrize(
   'value, expected',
   [
      ( None, [] ),
      ( 'Alert message.', [ 'Alert message.' ] ),
   ]
)
def Test_AsSingletonList( value: str | None, expected: list[ str ] ) -> None:
   assert ValueConversion.as_singleton_list( value ) == expected
