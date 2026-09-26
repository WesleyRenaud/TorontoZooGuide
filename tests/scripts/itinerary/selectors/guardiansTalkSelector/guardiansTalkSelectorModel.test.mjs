import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrencePresenter } from '../../../../../scripts/itinerary/scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';
import { GuardiansTalkScheduleItemKey } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkScheduleItemKey.js';
import { GuardiansTalkSelectorModel } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { Strings } from '../../../../../scripts/strings.js';


const talkRow = {
   name: 'Amur Tiger',
   location: 'Eurasia',
   start_time: '11:00 AM',
   end_time: '11:20 AM',
};


test('Test_GetGuardiansTalkName_TestRow_ExpectName', () => {
   const name = GuardiansTalkSelectorModel.getGuardiansTalkName(talkRow);

   assert.equal(name, talkRow.name);
});


test('Test_GetGuardiansTalkName_TestMissing_ExpectEmpty', () => {
   const row = {};

   const name = GuardiansTalkSelectorModel.getGuardiansTalkName(row);

   assert.equal(name, '');
});


test('Test_GetGuardiansTalkLocation_TestRow_ExpectLocation', () => {
   const location = GuardiansTalkSelectorModel.getGuardiansTalkLocation(talkRow);

   assert.equal(location, talkRow.location);
});


test('Test_GetGuardiansTalkLocation_TestMissing_ExpectEmpty', () => {
   const row = {};

   const location = GuardiansTalkSelectorModel.getGuardiansTalkLocation(row);

   assert.equal(location, '');
});


test('Test_GetGuardiansTalkId_TestRow_ExpectWireKey', () => {
   const talkId = GuardiansTalkSelectorModel.getGuardiansTalkId(talkRow);

   assert.equal(talkId, GuardiansTalkScheduleItemKey.fromRow(talkRow).toWire());
});


test('Test_GetGuardiansTalkId_TestMissingStart_ExpectEmpty', () => {
   const name = 'Talk';
   const row = { name };

   const talkId = GuardiansTalkSelectorModel.getGuardiansTalkId(row);

   assert.equal(talkId, '');
});


test('Test_FormatGuardiansTalkSearchTitle_TestName_ExpectLabeled', () => {
   const name = talkRow.name;

   const title = GuardiansTalkSelectorModel.formatGuardiansTalkSearchTitle(name);

   assert.equal(
      title,
      `${name}${GuardiansTalkSelectorModel.formatGuardiansTalkTitleSuffix(name)}`
   );
});


test('Test_GetGuardiansTalkSearchTitle_TestRow_ExpectLabeled', () => {
   const title = GuardiansTalkSelectorModel.getGuardiansTalkSearchTitle(talkRow);

   assert.equal(
      title,
      ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(
         talkRow.name,
         Strings.entityLabels.guardiansTalk
      )
   );
});


test('Test_GetGuardiansTalkSubtitle_TestRow_ExpectLocation', () => {
   const subtitle = GuardiansTalkSelectorModel.getGuardiansTalkSubtitle(talkRow);

   assert.equal(
      subtitle,
      ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: talkRow.location,
         timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(talkRow),
      })
   );
});


test('Test_BuildGuardiansTalkSelectionFields_TestRow_ExpectFields', () => {
   const fields = GuardiansTalkSelectorModel.buildGuardiansTalkSelectionFields(talkRow);

   assert.equal(fields.location, talkRow.location);
   assert.equal(fields.start_time, talkRow.start_time);
   assert.equal(fields.end_time, talkRow.end_time);
});


test('Test_ReadGuardiansTalkStoredFields_TestRow_ExpectFields', () => {
   const fields = GuardiansTalkSelectorModel.readGuardiansTalkStoredFields(talkRow);

   assert.equal(fields.location, talkRow.location);
   assert.equal(fields.start_time, talkRow.start_time);
   assert.equal(fields.end_time, talkRow.end_time);
});


test('Test_BuildGuardiansTalkImageSrc_TestName_ExpectDetailPath', () => {
   const imageSrc = GuardiansTalkSelectorModel.buildGuardiansTalkImageSrc(talkRow);

   assert.equal(
      imageSrc,
      ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(
         'guardians-talks',
         talkRow.name
      )
   );
});
