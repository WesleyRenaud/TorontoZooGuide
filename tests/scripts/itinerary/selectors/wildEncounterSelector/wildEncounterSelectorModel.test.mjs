import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledOccurrencePresenter } from '../../../../../scripts/itinerary/scheduledOccurrencePresenter.js';
import { ScheduledOccurrenceTimeModel } from '../../../../../scripts/itinerary/scheduledOccurrenceTimeModel.js';
import { WildEncounterScheduleItemKey } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { WildEncounterSelectorModel } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { Strings } from '../../../../../scripts/strings.js';


const encounterRow = {
   name: 'Giraffe Encounter',
   meeting_spot: 'African Savanna',
   start_time: '1:00 PM',
   end_time: '1:30 PM',
   link: 'https://example.com/giraffe',
};


test('Test_GetWildEncounterName_TestRow_ExpectName', () => {
   const name = WildEncounterSelectorModel.getWildEncounterName(encounterRow);

   assert.equal(name, encounterRow.name);
});


test('Test_GetWildEncounterName_TestMissing_ExpectEmpty', () => {
   const row = {};

   const name = WildEncounterSelectorModel.getWildEncounterName(row);

   assert.equal(name, '');
});


test('Test_GetWildEncounterMeetingSpot_TestRow_ExpectMeetingSpot', () => {
   const meetingSpot = WildEncounterSelectorModel.getWildEncounterMeetingSpot(encounterRow);

   assert.equal(meetingSpot, encounterRow.meeting_spot);
});


test('Test_GetWildEncounterMeetingSpot_TestMissing_ExpectEmpty', () => {
   const row = {};

   const meetingSpot = WildEncounterSelectorModel.getWildEncounterMeetingSpot(row);

   assert.equal(meetingSpot, '');
});


test('Test_GetWildEncounterId_TestRow_ExpectWireKey', () => {
   const encounterId = WildEncounterSelectorModel.getWildEncounterId(encounterRow);

   assert.equal(encounterId, WildEncounterScheduleItemKey.fromRow(encounterRow).toWire());
});


test('Test_GetWildEncounterSearchTitle_TestRow_ExpectLabeled', () => {
   const title = WildEncounterSelectorModel.getWildEncounterSearchTitle(encounterRow);

   assert.equal(
      title,
      ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(
         encounterRow.name,
         Strings.entityLabels.wildEncounter
      )
   );
});


test('Test_GetWildEncounterTitleSuffix_TestRow_ExpectSuffix', () => {
   const suffix = WildEncounterSelectorModel.getWildEncounterTitleSuffix(encounterRow);

   assert.equal(
      suffix,
      ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(
         encounterRow.name,
         Strings.entityLabels.wildEncounter
      )
   );
});


test('Test_GetWildEncounterLink_TestRow_ExpectLink', () => {
   const link = WildEncounterSelectorModel.getWildEncounterLink(encounterRow);

   assert.equal(link, encounterRow.link);
});


test('Test_GetWildEncounterSubtitle_TestRow_ExpectMeetingSpot', () => {
   const subtitle = WildEncounterSelectorModel.getWildEncounterSubtitle(encounterRow);

   assert.equal(
      subtitle,
      ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: encounterRow.meeting_spot,
         timeRange: ScheduledOccurrenceTimeModel.buildScheduledOccurrenceTimeRange(encounterRow),
      })
   );
});


test('Test_BuildWildEncounterSelectionFields_TestRow_ExpectFields', () => {
   const fields = WildEncounterSelectorModel.buildWildEncounterSelectionFields(encounterRow);

   assert.equal(fields.meeting_spot, encounterRow.meeting_spot);
   assert.equal(fields.start_time, encounterRow.start_time);
   assert.equal(fields.end_time, encounterRow.end_time);
});


test('Test_ReadWildEncounterStoredFields_TestRow_ExpectFields', () => {
   const fields = WildEncounterSelectorModel.readWildEncounterStoredFields(encounterRow);

   assert.equal(fields.meeting_spot, encounterRow.meeting_spot);
   assert.equal(fields.start_time, encounterRow.start_time);
   assert.equal(fields.end_time, encounterRow.end_time);
});


test('Test_BuildWildEncounterImageSrc_TestName_ExpectDetailPath', () => {
   const imageSrc = WildEncounterSelectorModel.buildWildEncounterImageSrc(encounterRow);

   assert.equal(
      imageSrc,
      ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(
         'wild-encounters',
         encounterRow.name
      )
   );
});
