from __future__ import annotations

from dataclasses import dataclass

from .email_image import EmailImage


@dataclass
class EmbeddedHtml:
   html: str
   images: list[ EmailImage ]
