from __future__ import annotations

from functools import lru_cache

from .data_access.paths import VIEWING_SPOT_ROUTING_OVERRIDES_DIR
from .domain.bulk_schedule_visit_before_rule import BulkScheduleVisitBeforeRule
from .domain.viewing_spot_name_key import ViewingSpotNameKey
from .domain.viewing_spot_routing_override import viewing_spot_routing_override_from_json
from .domain.viewing_spot_routing_override import ViewingSpotRoutingOverride


def viewing_spot_routing_override_for(
      species: str,
      exhibit: str,
      enclosure_name: str | None ) -> ViewingSpotRoutingOverride | None:
   return viewing_spot_routing_overrides_by_key().get(
      ( species, exhibit, enclosure_name ) )


def bulk_schedule_visit_before_rules() -> tuple[ BulkScheduleVisitBeforeRule, ... ]:
   rules: list[ BulkScheduleVisitBeforeRule ] = []

   for override in viewing_spot_routing_overrides():
      if not override.visit_before:
         continue

      rules.append(
         BulkScheduleVisitBeforeRule(
            visit_first=override.viewing_spot,
            visit_before=override.visit_before ) )

   return tuple( rules )


@lru_cache( maxsize=1 )
def viewing_spot_routing_overrides() -> tuple[ ViewingSpotRoutingOverride, ... ]:
   if not VIEWING_SPOT_ROUTING_OVERRIDES_DIR.is_dir():
      return ()

   overrides: list[ ViewingSpotRoutingOverride ] = []

   for path in sorted( VIEWING_SPOT_ROUTING_OVERRIDES_DIR.glob( '*.json' ) ):
      overrides.append( viewing_spot_routing_override_from_json( path ) )

   return tuple( overrides )


@lru_cache( maxsize=1 )
def viewing_spot_routing_overrides_by_key() -> dict[
      ViewingSpotNameKey,
      ViewingSpotRoutingOverride,
   ]:
   return {
      override.viewing_spot.key(): override
      for override in viewing_spot_routing_overrides()
   }
