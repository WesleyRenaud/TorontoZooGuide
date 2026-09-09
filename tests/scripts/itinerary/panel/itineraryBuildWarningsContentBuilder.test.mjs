import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryBuildWarningsContentBuilder } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsContentBuilder.js';
import { AttractionWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { WildEncounterUnscheduleFragment } from '../../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

ItineraryErrorTypes.updateItineraryErrorTypesFromConfig({
   suppressedErrorTypes: [],
});

const strings = {
   buildWarningScheduleOverlapTitle: 'Schedule overlap',
   buildWarningScheduleOverlapMessage: (name, time) => `${name} at ${time}`,
   buildWarningScheduleOverlapMessageWithoutTime: (name) => `${name} overlaps`,
   buildWarningWildEncounterOverlapMessage: (name, time) => `wild ${name} at ${time}`,
   buildWarningWildEncounterOverlapMessageWithoutTime: (name) => `wild ${name}`,
   buildWarningWithoutAnimalTitle: 'Without animal',
   buildWarningWithoutAnimalMessage: (name, time) => `${name} missing animal ${time}`,
   buildWarningWithoutAnimalMessageWithoutTime: (name) => `${name} missing animal`,
   buildWarningLongWaitTitle: 'Long wait',
   buildWarningLongWaitMessage: (name, time, phrase) => `${name} ${time} ${phrase}`,
   buildWarningLongWaitMessageWithoutTime: (name, phrase) => `${name} ${phrase}`,
};

test('Test_ItineraryBuildWarningIssueTypes_TestConfigured_ExpectTypes', () => {
   assert.deepEqual(
      ItineraryBuildWarningsContentBuilder.itineraryBuildWarningIssueTypes(),
      [
         'guardiansTalkWillUnscheduleItems',
         'wildEncounterWillUnscheduleItems',
         'guardiansTalkWithoutAnimal',
         'attractionWithoutAnimal',
         'fixedTimeItemLongWait',
      ]
   );
});

test('Test_BuildWarningConfirmFlags_TestTypes_ExpectFlagMap', () => {
   const flags = ItineraryBuildWarningsContentBuilder.buildWarningConfirmFlags();
   assert.deepEqual(flags.guardiansTalkWillUnscheduleItems, {
      confirmingGuardiansTalkUnschedule: true,
   });
   assert.deepEqual(flags.fixedTimeItemLongWait, {
      confirmingFixedTimeItemLongWait: true,
   });
});

test('Test_IssueTypeAndAsSections_TestValues_ExpectNormalized', () => {
   assert.equal(ItineraryBuildWarningsContentBuilder.issueType({ type: 'a' }), 'a');
   assert.equal(ItineraryBuildWarningsContentBuilder.issueType({ code: 'b' }), 'b');
   assert.equal(ItineraryBuildWarningsContentBuilder.issueType({}), '');
   assert.deepEqual(ItineraryBuildWarningsContentBuilder.asSections(null), []);
   assert.deepEqual(
      ItineraryBuildWarningsContentBuilder.asSections({ title: 'x' }),
      [{ title: 'x' }]
   );
});

test('Test_BuildGuardiansTalkUnscheduleSection_TestWithAndWithoutTime_ExpectSection', () => {
   const original = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues;
   GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => ({
      talkName: 'Amur Tiger',
      talkTime: '11:00 AM',
   });

   try {
      assert.deepEqual(
         ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings),
         {
            type: 'guardiansTalkWillUnscheduleItems',
            title: 'Schedule overlap',
            message: 'Amur Tiger at 11:00 AM',
         }
      );

      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => ({
         talkName: 'Amur Tiger',
      });
      assert.equal(
         ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings).message,
         'Amur Tiger overlaps'
      );

      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => null;
      assert.equal(
         ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings),
         null
      );
   } finally {
      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = original;
   }
});

test('Test_BuildWildEncounterUnscheduleSection_TestWithAndWithoutTime_ExpectSection', () => {
   const original = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues;
   WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = () => ({
      encounterName: 'Howls',
      encounterTime: '1:00 PM',
   });

   try {
      assert.match(
         ItineraryBuildWarningsContentBuilder.buildWildEncounterUnscheduleSection([], strings).message,
         /wild Howls at 1:00 PM/
      );

      WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = () => ({
         encounterName: 'Howls',
      });
      assert.equal(
         ItineraryBuildWarningsContentBuilder.buildWildEncounterUnscheduleSection([], strings).message,
         'wild Howls'
      );
   } finally {
      WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = original;
   }
});

test('Test_BuildWithoutAnimalAndLongWaitSections_TestIssues_ExpectMapped', () => {
   const originalTalks = GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues;
   const originalAttractions = AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues;
   const originalMessage = AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage;
   const originalLongWait = FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues;

   GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues = () => [
      { talkName: 'Tiger', talkTime: '11:00 AM' },
      { talkName: 'Lion' },
   ];
   AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues = () => [
      { attractionName: 'Carousel' },
   ];
   AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage = () => 'carousel warning';
   FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues = () => [
      { itemName: 'Talk', itemTime: '2:00 PM', typePhrase: 'talk' },
      { itemName: 'Encounter', typePhrase: 'encounter' },
   ];

   try {
      const talkSections = ItineraryBuildWarningsContentBuilder.buildGuardiansTalkWithoutAnimalSections([], strings);
      assert.equal(talkSections.length, 2);
      assert.match(talkSections[0].message, /Tiger missing animal 11:00 AM/);

      const attractionSections = ItineraryBuildWarningsContentBuilder.buildAttractionWithoutAnimalSections([], strings);
      assert.equal(attractionSections[0].message, 'carousel warning');

      const waitSections = ItineraryBuildWarningsContentBuilder.buildFixedTimeItemLongWaitSections([], strings);
      assert.equal(waitSections.length, 2);
      assert.match(waitSections[0].message, /Talk 2:00 PM talk/);
      assert.match(waitSections[1].message, /Encounter encounter/);
   } finally {
      GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues = originalTalks;
      AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues = originalAttractions;
      AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage = originalMessage;
      FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues = originalLongWait;
   }
});

test('Test_CreateBuildWarningsContent_TestSections_ExpectModules', () => {
   const content = ItineraryBuildWarningsContentBuilder.createBuildWarningsContent([
      { title: 'One', message: 'First' },
      { title: 'Two', message: 'Second' },
   ]);

   assert.ok(content.classList.contains('itin-build-warnings'));
   const modules = content.querySelectorAll('.itin-build-warning-module');
   assert.equal(modules.length, 2);
   assert.equal(
      content.querySelector('.itin-build-warning-module-title')?.textContent,
      'One'
   );
});
