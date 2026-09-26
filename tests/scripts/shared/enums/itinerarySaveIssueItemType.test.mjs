import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import itinerarySaveIssueItemTypeValues from '../../../../shared/enums/itinerarySaveIssueItemType.json' with { type: 'json' };

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');


test('Test_ItinerarySaveIssueItemType_TestSharedJson_ExpectSingleSourceOfTruth', () => {
   const diskValues = JSON.parse(
      readFileSync(path.join(root, 'shared/enums/itinerarySaveIssueItemType.json'), 'utf8')
   );

   const mapped = Object.fromEntries(
      Object.keys(itinerarySaveIssueItemTypeValues).map((key) => [key, ItinerarySaveIssueItemType[key]])
   );

   assert.deepEqual(mapped, itinerarySaveIssueItemTypeValues);
   assert.deepEqual(itinerarySaveIssueItemTypeValues, diskValues);
});
