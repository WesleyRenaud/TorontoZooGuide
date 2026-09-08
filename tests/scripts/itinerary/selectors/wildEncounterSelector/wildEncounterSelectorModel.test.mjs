import assert from 'node:assert/strict';
import test from 'node:test';

import { WildEncounterSelectorModel } from '../../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterSelectorModel.js';
import { Strings } from '../../../../../scripts/strings.js';

const encounterRow = {
   name: 'Giraffe Encounter',
   meeting_spot: 'African Savanna',
   start_time: '1:00 PM',
   end_time: '1:30 PM',
   link: 'https://example.com/giraffe',
};

test('Test_GetWildEncounterNameAndMeetingSpot_TestRow_ExpectStrings', () => {
   assert.equal(WildEncounterSelectorModel.getWildEncounterName(encounterRow), 'Giraffe Encounter');
   assert.equal(WildEncounterSelectorModel.getWildEncounterName({}), '');
   assert.equal(WildEncounterSelectorModel.getWildEncounterMeetingSpot(encounterRow), 'African Savanna');
   assert.equal(WildEncounterSelectorModel.getWildEncounterMeetingSpot({}), '');
});

test('Test_GetWildEncounterId_TestRow_ExpectWireKey', () => {
   assert.equal(
      WildEncounterSelectorModel.getWildEncounterId(encounterRow),
      'Giraffe Encounter||1:00 PM||1:30 PM'
   );
});

test('Test_FormatWildEncounterTitles_TestName_ExpectLabeled', () => {
   assert.match(
      WildEncounterSelectorModel.getWildEncounterSearchTitle(encounterRow),
      new RegExp(Strings.entityLabels.wildEncounter)
   );
   assert.ok(WildEncounterSelectorModel.getWildEncounterTitleSuffix(encounterRow).length > 0);
});

test('Test_GetWildEncounterLinkAndSubtitle_TestRow_ExpectValues', () => {
   assert.equal(WildEncounterSelectorModel.getWildEncounterLink(encounterRow), 'https://example.com/giraffe');
   assert.match(WildEncounterSelectorModel.getWildEncounterSubtitle(encounterRow), /African Savanna/);
});

test('Test_BuildWildEncounterSelectionAndStoredFields_TestRow_ExpectFields', () => {
   assert.deepEqual(WildEncounterSelectorModel.buildWildEncounterSelectionFields(encounterRow), {
      meeting_spot: 'African Savanna',
      start_time: '1:00 PM',
      end_time: '1:30 PM',
   });
   assert.deepEqual(WildEncounterSelectorModel.readWildEncounterStoredFields(encounterRow), {
      meeting_spot: 'African Savanna',
      start_time: '1:00 PM',
      end_time: '1:30 PM',
   });
});

test('Test_BuildWildEncounterImageSrc_TestName_ExpectDetailPath', () => {
   assert.match(
      WildEncounterSelectorModel.buildWildEncounterImageSrc(encounterRow) ?? '',
      /wild-encounters/
   );
});
