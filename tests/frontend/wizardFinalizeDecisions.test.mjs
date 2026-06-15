import assert from 'node:assert/strict';
import test from 'node:test';

import {
   shouldBlockEmptyFinish,
   shouldShowSaveIssuesPopup,
} from '../../scripts/itinerary/wizard/wizardFinalizeDecisions.js';

test('shouldBlockEmptyFinish blocks empty itineraries unless allowEmpty is true', () => {
   const isEmpty = (itinerary) => itinerary.empty;

   assert.equal(
      shouldBlockEmptyFinish({ empty: true }, false, isEmpty),
      true
   );
   assert.equal(
      shouldBlockEmptyFinish({ empty: true }, true, isEmpty),
      false
   );
   assert.equal(
      shouldBlockEmptyFinish({ empty: false }, false, isEmpty),
      false
   );
});

test('shouldShowSaveIssuesPopup detects save issue arrays', () => {
   assert.equal(shouldShowSaveIssuesPopup({ saveIssues: [{ type: 'conflict' }] }), true);
   assert.equal(shouldShowSaveIssuesPopup({ saveIssues: [] }), false);
   assert.equal(shouldShowSaveIssuesPopup({}), false);
   assert.equal(shouldShowSaveIssuesPopup(null), false);
});
