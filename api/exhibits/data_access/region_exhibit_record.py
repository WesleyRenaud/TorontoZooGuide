from dataclasses import dataclass


@dataclass( frozen=True )
class RegionExhibitRecord:
   region_name: str
   exhibit_name: str | None
