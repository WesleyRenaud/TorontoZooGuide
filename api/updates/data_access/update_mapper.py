from ... import zoo


def map_update_record( row ):
   return zoo.Update(
      title=row[ 'TITLE' ],
      description=row[ 'DESCRIPTION' ],
      update_type=row[ 'UPDATE_TYPE' ],
      start_date=row[ 'START_DATE' ],
      end_date=row[ 'END_DATE' ] )



def map_update_records( rows ):
   return [
      map_update_record( row )
      for row in rows
   ]
