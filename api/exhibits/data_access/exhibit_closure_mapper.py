from .exhibit_closure_record import ExhibitClosureRecord


def map_exhibit_closure_record( row ):
   return ExhibitClosureRecord(
      exhibit=row[ 'EXHIBIT' ],
      closed_start=row[ 'CLOSED_START' ],
      closed_end=row[ 'CLOSED_END' ] )



def map_exhibit_closure_records( rows ):
   return [
      map_exhibit_closure_record( row )
      for row in rows
   ]
