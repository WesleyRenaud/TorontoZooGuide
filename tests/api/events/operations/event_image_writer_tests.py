from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image
import pytest

from api.events.operations.event_image_writer import EventImageWriter
from tools.checks.website_page import WebsitePage


def image_bytes( kind: str ) -> bytes:
   source = BytesIO()
   Image.new( 'RGB', ( 2, 2 ), ( 12, 34, 56 ) ).save( source, format=kind )
   return source.getvalue()


def Test_Save_TestPlainImage_ExpectWritesPngForTheEventName(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( EventImageWriter, 'FOLDER', tmp_path )
   payload = base64.b64encode( image_bytes( 'WEBP' ) ).decode()

   EventImageWriter.save( 'Glow In The Wild', f'data:image/webp;base64,{ payload }' )

   saved = ( tmp_path / 'glow-in-the-wild.png' ).read_bytes()
   assert saved.startswith( b'\x89PNG' )


def Test_Save_TestUnusableImage_ExpectNothingStored(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( EventImageWriter, 'FOLDER', tmp_path )

   EventImageWriter.save( 'Glow', 'data:text/plain;base64,YQ==' )
   EventImageWriter.save( 'Glow', 'data:image/png' )
   EventImageWriter.save( 'Glow', 'data:image/png;base64,' )

   assert list( tmp_path.iterdir() ) == []


def Test_Save_TestWebsiteImage_ExpectWritesPng(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr( EventImageWriter, 'FOLDER', tmp_path )
   monkeypatch.setattr( WebsitePage, 'fetch_bytes', lambda url: image_bytes( 'JPEG' ) )

   EventImageWriter.save(
      'Glow In The Wild',
      'https://www.torontozoo.com/!/img/event/26/glowthumb1080n.webp',
   )

   saved = ( tmp_path / 'glow-in-the-wild.png' ).read_bytes()
   assert saved.startswith( b'\x89PNG' )
