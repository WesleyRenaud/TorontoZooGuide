from __future__ import annotations

import subprocess
from typing import Any

import pytest

import api.html_strings as html_strings
from api.html_strings import clear_html_string_cache
from api.html_strings import get_html_string_values


def test_get_html_string_values_reuses_cache_until_sources_change(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   clear_html_string_cache()
   call_count = 0
   original_run = html_strings.subprocess.run

   def counting_run(
         *args: Any,
         **kwargs: Any ) -> subprocess.CompletedProcess[ str ]:
      nonlocal call_count
      call_count += 1
      return original_run( *args, **kwargs )

   monkeypatch.setattr( html_strings.subprocess, 'run', counting_run )

   first = get_html_string_values()
   second = get_html_string_values()

   assert first is second
   assert call_count == 1
