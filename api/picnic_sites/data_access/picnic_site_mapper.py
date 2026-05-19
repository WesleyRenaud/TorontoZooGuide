from ... import zoo


def map_picnic_site_record( row ):
   return zoo.PicnicSite(
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_picnic_site_records( rows ):
   return [
      map_picnic_site_record( row )
      for row in rows
   ]
