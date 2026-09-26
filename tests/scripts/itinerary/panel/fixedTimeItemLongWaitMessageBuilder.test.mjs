import assert from 'node:assert/strict';
import test from 'node:test';

import { FixedTimeItemLongWaitMessageBuilder } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitMessageBuilder.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_ResolveItemTypeMeta_TestGuardiansTalk_ExpectMeta', () => {
   const item = { item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK };

   const meta = FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta(item);

   assert.equal(meta.itemType, item.item_type);
   assert.equal(meta.typeLabel, Strings.entityLabels.guardiansTalk);
});


test('Test_ResolveItemTypeMeta_TestWildEncounter_ExpectMeta', () => {
   const item = { item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER };

   const meta = FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta(item);

   assert.equal(meta.itemType, item.item_type);
   assert.equal(meta.typePhrase, Strings.entityPhrases.wildEncounter);
});


test('Test_ResolveItemTypeMeta_TestUnsupported_ExpectThrows', () => {
   const item = { item_type: ItinerarySaveIssueItemType.ANIMAL };

   assert.throws(
      () => FixedTimeItemLongWaitMessageBuilder.resolveItemTypeMeta(item),
      /Unsupported fixed-time long-wait item type/
   );
});


test('Test_FixedTimeItemLongWaitIssueType_TestSharedEnum_ExpectWireValue', () => {
   const issueType = FixedTimeItemLongWaitMessageBuilder.fixedTimeItemLongWaitIssueType();

   assert.equal(issueType, ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT);
});


test('Test_IsLongWaitIssue_TestMatchingType_ExpectTrue', () => {
   const issue = { type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT };

   const isLongWait = FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue(issue);

   assert.equal(isLongWait, true);
});


test('Test_IsLongWaitIssue_TestOtherType_ExpectFalse', () => {
   const issue = { type: 'OTHER' };

   const isLongWait = FixedTimeItemLongWaitMessageBuilder.isLongWaitIssue(issue);

   assert.equal(isLongWait, false);
});


test('Test_LongWaitItems_TestIssues_ExpectFlattened', () => {
   const firstTalk = { itemName: 'Amur Tiger' };
   const secondTalk = { itemName: 'Snow Leopard' };
   const issues = [
      {
         type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
         items: [firstTalk, secondTalk],
      },
      { type: 'OTHER', items: [{ itemName: 'Skip' }] },
   ];

   const items = FixedTimeItemLongWaitMessageBuilder.longWaitItems(issues);

   assert.deepEqual(items, [firstTalk, secondTalk]);
});


test('Test_LongWaitConfirmMessage_TestWithTime_ExpectString', () => {
   const itemName = 'Amur Tiger';
   const itemTime = '11:00 AM';
   const typePhrase = 'talk';
   const strings = {
      fixedTimeItemLongWaitMessage: (name, time, type) => `${name}@${time}:${type}`,
      fixedTimeItemLongWaitMessageWithoutTime: (name, type) => `${name}:${type}`,
   };

   const message = FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage({
      itemName,
      itemTime,
      typePhrase,
   }, strings);

   assert.equal(message, strings.fixedTimeItemLongWaitMessage(itemName, itemTime, typePhrase));
});


test('Test_LongWaitConfirmMessage_TestWithoutTime_ExpectString', () => {
   const itemName = 'Amur Tiger';
   const typePhrase = 'talk';
   const strings = {
      fixedTimeItemLongWaitMessage: (name, time, type) => `${name}@${time}:${type}`,
      fixedTimeItemLongWaitMessageWithoutTime: (name, type) => `${name}:${type}`,
   };

   const message = FixedTimeItemLongWaitMessageBuilder.longWaitConfirmMessage({
      itemName,
      typePhrase,
   }, strings);

   assert.equal(message, strings.fixedTimeItemLongWaitMessageWithoutTime(itemName, typePhrase));
});
