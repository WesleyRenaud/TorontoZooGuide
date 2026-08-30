from __future__ import annotations

from api.shared.text_values import TextValues


def Test_NormalizeForMatching_TestMixedCaseAndWhitespace_ExpectLowercaseTrimmed() -> None:
   assert TextValues.normalize_for_matching( '  African Lion  ' ) == 'african lion'


def Test_NormalizeForMatching_TestNone_ExpectEmptyString() -> None:
   assert TextValues.normalize_for_matching( None ) == ''
