from __future__ import annotations

from collections.abc import Callable
from typing import Any
from typing import TypeVar

import pytest


TStub = TypeVar( 'TStub' )


def patch_coordinator_with_stub(
      monkeypatch: pytest.MonkeyPatch,
      coordinator_class: type,
      stub: TStub ) -> None:
   for method_name in dir( coordinator_class ):
      if method_name.startswith( '_' ) or not hasattr( stub, method_name ):
         continue

      stub_method = getattr( stub, method_name )

      if not callable( stub_method ):
         continue

      @classmethod
      def patched(
            cls: type,
            *args: Any,
            _stub_method: Callable[ ..., Any ] = stub_method,
            **kwargs: Any ) -> Any:
         return _stub_method( *args, **kwargs )

      monkeypatch.setattr( coordinator_class, method_name, patched )
