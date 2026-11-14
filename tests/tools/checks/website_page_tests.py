from __future__ import annotations

from pathlib import Path
from subprocess import CompletedProcess

import pytest

from tools.checks.website_page import WebsitePage


def Test_Read_TestGonePage_ExpectStatusAndBody( monkeypatch: pytest.MonkeyPatch ) -> None:
   body = '<!DOCTYPE html><title>410 Not found</title>'

   def run( command: list[ str ], check: bool, capture_output: bool ) -> CompletedProcess[ bytes ]:
      Path( command[ command.index( '-o' ) + 1 ] ).write_text( body )
      return CompletedProcess( command, 0, b'410', b'' )

   monkeypatch.setattr( 'tools.checks.website_page.subprocess.run', run )

   assert WebsitePage.read( 'https://www.torontozoo.com/events/veteran' ) == ( 410, body )
