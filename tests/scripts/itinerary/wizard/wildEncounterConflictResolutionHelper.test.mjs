import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterConflictResolutionHelper } from '../../../../scripts/itinerary/wizard/wildEncounterConflictResolutionHelper.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';

test('Test_ToConflictResolutionDraftItem_TestGuardiansAndWild_ExpectShape', () => {
   assert.deepEqual(
      WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem({
         item_type: ItinerarySaveIssueItemType.guardiansTalk,
         name: 'Lion Talk',
         location: 'Theatre',
      }),
      { name: 'Lion Talk', location: 'Theatre' }
   );
   assert.deepEqual(
      WildEncounterConflictResolutionHelper.toConflictResolutionDraftItem({
         name: 'Red Panda',
         meeting_spot: 'Pavilion',
      }),
      { name: 'Red Panda', meeting_spot: 'Pavilion' }
   );
});

test('Test_GetDraftItemName_TestInputs_ExpectName', () => {
   assert.equal(WildEncounterConflictResolutionHelper.getDraftItemName('Carousel'), 'Carousel');
   assert.equal(WildEncounterConflictResolutionHelper.getDraftItemName({ name: 'Zoomobile' }), 'Zoomobile');
   assert.equal(WildEncounterConflictResolutionHelper.getDraftItemName({}), '');
});
