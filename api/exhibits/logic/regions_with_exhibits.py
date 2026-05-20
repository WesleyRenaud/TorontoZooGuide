from ...models import RegionWithExhibits


def build_regions_with_exhibits( region_exhibit_records ):
   regions = []
   current_region = None

   for record in region_exhibit_records:
      region_name = record.region_name
      exhibit_name = record.exhibit_name

      if current_region == None or current_region.name != region_name:
         current_region = RegionWithExhibits(
            name=region_name,
            exhibits=[] )
         regions.append( current_region )

      if exhibit_name == None:
         continue

      current_region.exhibits.append( exhibit_name )

   return [
      region for region in regions
      if len( region.exhibits ) > 0
   ]
