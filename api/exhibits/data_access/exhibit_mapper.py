from .region_exhibit_record import RegionExhibitRecord


def map_region_exhibit_row( row ):
   return RegionExhibitRecord(
      region_name=row[ 'REGION_NAME' ],
      exhibit_name=row[ 'EXHIBIT_NAME' ] )


def map_region_exhibit_rows( rows ):
   return [
      map_region_exhibit_row( row )
      for row in rows
   ]
