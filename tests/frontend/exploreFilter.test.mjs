import assert from 'node:assert/strict';
import test from 'node:test';

import { buildExploreSearchIncludeFlags } from '../../scripts/search/exploreFilter.js';

test('buildExploreSearchIncludeFlags maps selected explore types to search flags', () => {
   assert.deepEqual(
      buildExploreSearchIncludeFlags(['animal', 'restaurant', 'wildEncounter'], 'none'),
      {
         includeAnimals: true,
         includePavilions: false,
         includeRestaurants: true,
         includeRestrooms: false,
         includeGiftShops: false,
         includeAttractions: false,
         includeGuardiansTalks: false,
         includeWildEncounters: true,
         includeZoomobileStations: false,
      }
   );
});

test('buildExploreSearchIncludeFlags includes zoomobile stations when a route is selected', () => {
   assert.equal(
      buildExploreSearchIncludeFlags(['animal'], 'current').includeZoomobileStations,
      true
   );
});
