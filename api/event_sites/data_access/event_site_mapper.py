from ... import zoo


def map_event_site_record( row ):
   return zoo.EventSite(
      name=row[ 'NAME' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_event_site_records( rows ):
   return [
      map_event_site_record( row )
      for row in rows
   ]
