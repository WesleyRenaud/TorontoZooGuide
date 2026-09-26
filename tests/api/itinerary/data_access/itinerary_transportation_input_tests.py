from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput
from api.shared.enums.transportation_name import TransportationName


def Test_FromWire_TestAttractionMode_ExpectParsedInput() -> None:
   name = TransportationName.ZOOMOBILE.value
   added_as_attraction = True
   wire = {
      'name': name,
      'added_as_attraction': added_as_attraction,
   }

   parsed = ItineraryTransportationInput.from_wire( wire )

   assert parsed.name == name
   assert parsed.added_as_attraction is added_as_attraction


def Test_FromWires_TestEmpty_ExpectEmptyList() -> None:
   value = None

   parsed = ItineraryTransportationInput.from_wires( value )

   assert parsed == []
