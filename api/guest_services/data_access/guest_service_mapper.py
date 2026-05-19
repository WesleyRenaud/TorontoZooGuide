from ... import zoo


def map_guest_service_record( row ):
   return zoo.GuestService(
      service_type=row[ 'SERVICE_TYPE' ],
      x_coord=row[ 'X_COORD' ],
      y_coord=row[ 'Y_COORD' ] )



def map_guest_service_records( rows ):
   return [
      map_guest_service_record( row )
      for row in rows
   ]
