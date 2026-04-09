from .tables import static_tables


def seed_static_data( cursor ):
   for table in static_tables:
      table.insert_rows( cursor )
