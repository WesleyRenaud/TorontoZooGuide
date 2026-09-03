from __future__ import annotations

from api.itinerary.data_access.itinerary_transportation_input import ItineraryTransportationInput

def Test_FromWire_TestAttractionMode_ExpectParsedInput() -> None:
   wire = {
      'name': 'Zoomobile',
      'added_as_attraction': True,
   }

   parsed = ItineraryTransportationInput.from_wire( wire )

   assert parsed.name == 'Zoomobile'
   assert parsed.added_as_attraction is True

def Test_FromWires_TestEmpty_ExpectEmptyList() -> None:
   assert ItineraryTransportationInput.from_wires( None ) == []
