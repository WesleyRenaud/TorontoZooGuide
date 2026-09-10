import assert from 'node:assert/strict';
import test from 'node:test';

import { ExploreFragment } from '../../../scripts/updates/exploreFragment.js';
import { ExploreUpdatesHelper } from '../../../scripts/updates/exploreUpdatesHelper.js';

test('Test_BuildDatePayload_TestContext_ExpectFields', () => {
   assert.deepEqual(
      ExploreUpdatesHelper.buildDatePayload({ month: 9, day: 8, year: 2026 }),
      { month: 9, day: 8, year: 2026 }
   );
});

test('Test_BuildTodayDatePayload_TestFixedDate_ExpectLocalCalendarFields', () => {
   assert.deepEqual(
      ExploreUpdatesHelper.buildTodayDatePayload(new Date(2026, 8, 10, 12, 0, 0)),
      { month: 'SEP', day: 10, year: 2026 }
   );
});

test('Test_ResolveActiveTab_TestEmptyCollections_ExpectFallbackTab', () => {
   assert.equal(
      ExploreUpdatesHelper.resolveActiveTab(
         ExploreFragment.EXPLORE_TAB.UPDATES,
         [],
         [{ id: 1 }]
      ),
      ExploreFragment.EXPLORE_TAB.EVENTS
   );
   assert.equal(
      ExploreUpdatesHelper.resolveActiveTab(
         ExploreFragment.EXPLORE_TAB.EVENTS,
         [{ id: 1 }],
         []
      ),
      ExploreFragment.EXPLORE_TAB.UPDATES
   );
   assert.equal(
      ExploreUpdatesHelper.resolveActiveTab(
         ExploreFragment.EXPLORE_TAB.UPDATES,
         [{ id: 1 }],
         []
      ),
      ExploreFragment.EXPLORE_TAB.UPDATES
   );
});
