from ..models import Region


def build_region_options( region_exhibit_rows ):
   exhibits_by_region = {}

   for region_exhibit in region_exhibit_rows:
      region_name = region_exhibit.region_name
      exhibit_name = region_exhibit.exhibit_name

      if region_name not in exhibits_by_region:
         exhibits_by_region[ region_name ] = []

      if exhibit_name != None:
         exhibits_by_region[ region_name ].append( exhibit_name )

   return [
      Region(
         name=region_name,
         has_exhibits=not (
            len( exhibits ) == 1
            and exhibits[ 0 ] == region_name
         ) )
      for region_name, exhibits in exhibits_by_region.items()
      if len( exhibits ) > 0
   ]
