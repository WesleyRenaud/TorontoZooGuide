from __future__ import annotations

from api.itinerary.domain.itinerary import build_itinerary
from api.itinerary.routing.itinerary_walk_route_completion import itinerary_has_unscheduled_guest_items
from api.itinerary.routing.itinerary_walk_route_completion import should_append_return_to_entrance_walk_route_leg
from api.models import Animal
from api.models import Attraction


def test_itinerary_has_unscheduled_guest_items_detects_unscheduled_animals_and_attractions() -> None:
   itinerary = build_itinerary(
      date='2026-06-20',
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:30 AM' ),
         Animal(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor' ),
      ],
      attractions=[
         Attraction( name='Conservation Carousel', free_with_admission=True ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   assert itinerary_has_unscheduled_guest_items( itinerary )


def test_itinerary_has_unscheduled_guest_items_is_false_when_guest_items_are_scheduled() -> None:
   itinerary = build_itinerary(
      date='2026-06-20',
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:30 AM' ),
      ],
      attractions=[
         Attraction(
            name='Conservation Carousel',
            free_with_admission=True,
            start_time='11:00 AM',
            end_time='11:20 AM' ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   assert not itinerary_has_unscheduled_guest_items( itinerary )


def test_should_append_return_to_entrance_only_when_all_guest_items_are_scheduled() -> None:
   partial_itinerary = build_itinerary(
      date='2026-06-20',
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:30 AM' ),
         Animal(
            species='Cheetah',
            exhibit='Indo-Malaya Outdoor' ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )
   complete_itinerary = build_itinerary(
      date='2026-06-20',
      animals=[
         Animal(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:30 AM' ),
      ],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
      arrival_time='9:30 AM',
      departure_time='5:00 PM' )

   assert not should_append_return_to_entrance_walk_route_leg( partial_itinerary )
   assert should_append_return_to_entrance_walk_route_leg( complete_itinerary )
