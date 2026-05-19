def zoomobile_station_name_key( zoomobile_station ):
   return ( zoomobile_station.name or '' ).strip().lower()


def filter_zoomobile_stations_matching_query( zoomobile_stations, query ):
   if not query:
      return list( zoomobile_stations )

   query_lower = query.strip().lower()
   return [
      zoomobile_station for zoomobile_station in zoomobile_stations
      if query_lower in zoomobile_station_name_key( zoomobile_station )
   ]


def build_zoomobile_stations_matching_query( zoomobile_stations, query ):
   return filter_zoomobile_stations_matching_query(
      zoomobile_stations,
      query )
