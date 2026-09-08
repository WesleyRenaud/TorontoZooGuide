import assert from 'node:assert/strict';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';

test('Test_ItinerarySaveIssueItemType_TestConstants_ExpectValues', () => {
   assert.equal(ItinerarySaveIssueItemType.guardiansTalk, 'guardiansTalk');
   assert.equal(ItinerarySaveIssueItemType.wildEncounter, 'wildEncounter');
});
