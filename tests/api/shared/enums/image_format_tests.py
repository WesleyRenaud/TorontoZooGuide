from __future__ import annotations

from api.shared.enums.image_format import ImageFormat
from api.shared.enums.shared_enum_values import SharedEnumValues


def Test_Extensions_TestSharedJson_ExpectSuffixes() -> None:
   members = SharedEnumValues.load_object_members( 'imageFormat.json' )
   expected = {
      extension
      for definition in members.values()
      for extension in definition[ 'extensions' ]
   }

   assert ImageFormat.extensions() == expected


def Test_SubtypeFor_TestKnownSuffix_ExpectKind() -> None:
   assert ImageFormat.subtype_for( 'photo.PNG' ) == ImageFormat.PNG.value
   assert ImageFormat.subtype_for( 'photo.jpg' ) == ImageFormat.JPEG.value
   assert ImageFormat.subtype_for( 'photo.jpeg' ) == ImageFormat.JPEG.value
   assert ImageFormat.subtype_for( 'photo.gif' ) == ImageFormat.GIF.value
   assert ImageFormat.subtype_for( 'photo.webp' ) == ImageFormat.WEBP.value


def Test_MatchesDataUrl_TestImageAndPlain_ExpectOnlyImages() -> None:
   assert ImageFormat.matches_data_url( 'data:image/webp;base64,abc' )
   assert not ImageFormat.matches_data_url( 'data:text/plain;base64,abc' )


def Test_SubtypeFor_TestUnknownSuffix_ExpectJpeg() -> None:
   assert ImageFormat.subtype_for( 'notes.txt' ) == ImageFormat.JPEG.value
