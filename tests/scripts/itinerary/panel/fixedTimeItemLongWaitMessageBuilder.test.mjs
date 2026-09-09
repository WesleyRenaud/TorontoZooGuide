import assert from 'node:assert/strict';
import test from 'node:test';

import { FixedTimeItemLongWaitMessageBuilder } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitMessageBuilder.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_ResolveItemTypeMeta_TestGuardiansTalk_ExpectMeta', () => {
   const meta = FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta({
      item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   });

   assert.equal(meta.itemType, ItinerarySaveIssueItemType.GUARDIANS_TALK);
   assert.equal(meta.typeLabel, Strings.entityLabels.guardiansTalk);
});

test('Test_ResolveItemTypeMeta_TestWildEncounter_ExpectMeta', () => {
   const meta = FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta({
      item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   });

   assert.equal(meta.itemType, ItinerarySaveIssueItemType.WILD_ENCOUNTER);
   assert.equal(meta.typePhrase, Strings.entityPhrases.wildEncounter);
});

test('Test_ResolveItemTypeMeta_TestUnsupported_ExpectThrows', () => {
   assert.throws(
      () => FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta({ item_type: 'animal' }),
      /Unsupported fixed-time long-wait item type/
   );
});

test('Test_FixedTimeItemLongWaitIssueType_TestSharedEnum_ExpectWireValue', () => {
   assert.equal(
      FixedTimeItemLongWaitMessageBuilder.fixedTimeItemLongWaitIssueType(),
      ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT
   );
});

test('Test_IsLongWaitIssue_TestType_ExpectBoolean', () => {
   assert.equal(
      FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue({
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      }),
      true
   );
   assert.equal(FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue({ type: 'OTHER' }), false);
});

test('Test_LongWaitItems_TestIssues_ExpectFlattened', () => {
   const items = FixedTimeItemLongWaitMessageBuilder.longWaitItems([
      {
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [{ itemName: 'Talk A' }, { itemName: 'Talk B' }],
      },
      { type: 'OTHER', items: [{ itemName: 'Skip' }] },
   ]);

   assert.deepEqual(items, [{ itemName: 'Talk A' }, { itemName: 'Talk B' }]);
});

test('Test_LongWaitConfirmMessage_TestWithAndWithoutTime_ExpectStrings', () => {
   const strings = {
      fixedTimeItemLongWaitMessage: (name, time, type) => `${name}@${time}:${type}`,
      fixedTimeItemLongWaitMessageWithoutTime: (name, type) => `${name}:${type}`,
   };

   assert.equal(
      FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage({
         itemName: 'Amur Tiger',
         itemTime: '11:00 AM',
         typePhrase: 'talk',
      }, strings),
      'Amur Tiger@11:00 AM:talk'
   );
   assert.equal(
      FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage({
         itemName: 'Amur Tiger',
         typePhrase: 'talk',
      }, strings),
      'Amur Tiger:talk'
   );
});
