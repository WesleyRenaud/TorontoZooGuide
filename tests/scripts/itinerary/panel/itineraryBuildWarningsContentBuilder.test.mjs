import assert from 'node:assert/strict';
import test from 'node:test';

import { AttractionWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/attractionWithoutAnimalFragment.js';
import { FixedTimeItemLongWaitFragment } from '../../../../scripts/itinerary/panel/fixedTimeItemLongWaitFragment.js';
import { GuardiansTalkUnscheduleFragment } from '../../../../scripts/itinerary/panel/guardiansTalkUnscheduleFragment.js';
import { GuardiansTalkWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryBuildWarningsContentBuilder } from '../../../../scripts/itinerary/panel/itineraryBuildWarningsContentBuilder.js';
import { WildEncounterUnscheduleFragment } from '../../../../scripts/itinerary/panel/wildEncounterUnscheduleFragment.js';
import { ItineraryErrorTypes } from '../../../../scripts/itinerary/itineraryErrorTypes.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

ItineraryErrorTypes.syncSuppressedItineraryErrorTypes({
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

installDomTestHooks();


test('Test_ItineraryBuildWarningIssueTypes_TestConfigured_ExpectTypes', () => {
   const types = ItineraryBuildWarningsContentBuilder.itineraryBuildWarningIssueTypes();

   assert.deepEqual(types, [
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
   ]);
});


test('Test_BuildWarningConfirmFlags_TestGuardiansTalkUnschedule_ExpectFlag', () => {
   const flags = ItineraryBuildWarningsContentBuilder.buildWarningConfirmFlags();

   assert.deepEqual(flags[ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS], {
      confirmingGuardiansTalkUnschedule: true,
   });
});


test('Test_BuildWarningConfirmFlags_TestFixedTimeItemLongWait_ExpectFlag', () => {
   const flags = ItineraryBuildWarningsContentBuilder.buildWarningConfirmFlags();

   assert.deepEqual(flags[ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT], {
      confirmingFixedTimeItemLongWait: true,
   });
});


test('Test_IssueType_TestTypeField_ExpectType', () => {
   const type = 'a';

   const issueType = ItineraryBuildWarningsContentBuilder.issueType({ type });

   assert.equal(issueType, type);
});


test('Test_IssueType_TestCodeField_ExpectCode', () => {
   const code = 'b';

   const issueType = ItineraryBuildWarningsContentBuilder.issueType({ code });

   assert.equal(issueType, code);
});


test('Test_IssueType_TestEmpty_ExpectEmptyString', () => {
   const issueType = ItineraryBuildWarningsContentBuilder.issueType({});

   assert.equal(issueType, '');
});


test('Test_AsSections_TestNull_ExpectEmptyArray', () => {
   const sections = ItineraryBuildWarningsContentBuilder.asSections(null);

   assert.deepEqual(sections, []);
});


test('Test_AsSections_TestSingleSection_ExpectWrapped', () => {
   const title = 'x';
   const section = { title };

   const sections = ItineraryBuildWarningsContentBuilder.asSections(section);

   assert.deepEqual(sections, [section]);
});


test('Test_BuildGuardiansTalkUnscheduleSection_TestWithTime_ExpectSection', () => {
   const talkName = 'Amur Tiger';
   const talkTime = '11:00 AM';
   const original = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues;
   GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => ({
      talkName,
      talkTime,
   });

   try {
      const section = ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings);

      assert.deepEqual(section, {
         type: ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
         title: strings.buildWarningScheduleOverlapTitle,
         message: strings.buildWarningScheduleOverlapMessage(talkName, talkTime),
      });
   } finally {
      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = original;
   }
});


test('Test_BuildGuardiansTalkUnscheduleSection_TestWithoutTime_ExpectOverlapMessage', () => {
   const talkName = 'Amur Tiger';
   const original = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues;
   GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => ({
      talkName,
   });

   try {
      const section = ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings);

      assert.equal(section.message, strings.buildWarningScheduleOverlapMessageWithoutTime(talkName));
   } finally {
      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = original;
   }
});


test('Test_BuildGuardiansTalkUnscheduleSection_TestMissingTalk_ExpectNull', () => {
   const original = GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues;
   GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = () => null;

   try {
      const section = ItineraryBuildWarningsContentBuilder.buildGuardiansTalkUnscheduleSection([], strings);

      assert.equal(section, null);
   } finally {
      GuardiansTalkUnscheduleFragment.getPrimaryGuardiansTalkFromUnscheduleIssues = original;
   }
});


test('Test_BuildWildEncounterUnscheduleSection_TestWithTime_ExpectMessage', () => {
   const encounterName = 'From Howls to Honks';
   const encounterTime = '1:00 PM';
   const original = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues;
   WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = () => ({
      encounterName,
      encounterTime,
   });

   try {
      const section = ItineraryBuildWarningsContentBuilder.buildWildEncounterUnscheduleSection([], strings);

      assert.equal(
         section.message,
         strings.buildWarningWildEncounterOverlapMessage(encounterName, encounterTime)
      );
   } finally {
      WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = original;
   }
});


test('Test_BuildWildEncounterUnscheduleSection_TestWithoutTime_ExpectMessage', () => {
   const encounterName = 'From Howls to Honks';
   const original = WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues;
   WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = () => ({
      encounterName,
   });

   try {
      const section = ItineraryBuildWarningsContentBuilder.buildWildEncounterUnscheduleSection([], strings);

      assert.equal(
         section.message,
         strings.buildWarningWildEncounterOverlapMessageWithoutTime(encounterName)
      );
   } finally {
      WildEncounterUnscheduleFragment.getPrimaryWildEncounterFromUnscheduleIssues = original;
   }
});


test('Test_BuildGuardiansTalkWithoutAnimalSections_TestTalks_ExpectMessages', () => {
   const talkName = 'Amur Tiger';
   const talkTime = '11:00 AM';
   const secondTalkName = 'African Lion';
   const originalTalks = GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues;
   GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues = () => [
      { talkName, talkTime },
      { talkName: secondTalkName },
   ];

   try {
      const talkSections = ItineraryBuildWarningsContentBuilder.buildGuardiansTalkWithoutAnimalSections([], strings);

      assert.equal(talkSections.length, Position.THIRD);
      assert.equal(
         talkSections.at(Position.FIRST).message,
         strings.buildWarningWithoutAnimalMessage(talkName, talkTime)
      );
   } finally {
      GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues = originalTalks;
   }
});


test('Test_BuildAttractionWithoutAnimalSections_TestAttraction_ExpectMessage', () => {
   const attractionMessage = 'carousel warning';
   const originalAttractions = AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues;
   const originalMessage = AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage;
   AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues = () => [
      { attractionName: 'Conservation Carousel' },
   ];
   AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage = () => attractionMessage;

   try {
      const attractionSections = ItineraryBuildWarningsContentBuilder.buildAttractionWithoutAnimalSections([], strings);

      assert.equal(attractionSections.at(Position.FIRST).message, attractionMessage);
   } finally {
      AttractionWithoutAnimalFragment.getAttractionsFromWithoutAnimalIssues = originalAttractions;
      AttractionWithoutAnimalFragment.attractionWithoutAnimalMessage = originalMessage;
   }
});


test('Test_BuildFixedTimeItemLongWaitSections_TestItems_ExpectMessages', () => {
   const talkName = 'Mornings in Malaysia';
   const talkTime = '2:00 PM';
   const talkPhrase = 'talk';
   const encounterName = 'From Howls to Honks';
   const encounterPhrase = 'encounter';
   const originalLongWait = FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues;
   FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues = () => [
      { itemName: talkName, itemTime: talkTime, typePhrase: talkPhrase },
      { itemName: encounterName, typePhrase: encounterPhrase },
   ];

   try {
      const waitSections = ItineraryBuildWarningsContentBuilder.buildFixedTimeItemLongWaitSections([], strings);

      assert.equal(waitSections.length, Position.THIRD);
      assert.equal(
         waitSections.at(Position.FIRST).message,
         strings.buildWarningLongWaitMessage(talkName, talkTime, talkPhrase)
      );
      assert.equal(
         waitSections.at(Position.SECOND).message,
         strings.buildWarningLongWaitMessageWithoutTime(encounterName, encounterPhrase)
      );
   } finally {
      FixedTimeItemLongWaitFragment.getFixedTimeItemsFromLongWaitIssues = originalLongWait;
   }
});


test('Test_CreateBuildWarningsContent_TestSections_ExpectModules', () => {
   const firstTitle = 'One';
   const firstMessage = 'First';
   const secondTitle = 'Two';
   const secondMessage = 'Second';

   const content = ItineraryBuildWarningsContentBuilder.createBuildWarningsContent([
      { title: firstTitle, message: firstMessage },
      { title: secondTitle, message: secondMessage },
   ]);
   const modules = content.querySelectorAll('.itin-build-warning-module');
   const title = content.querySelector('.itin-build-warning-module-title')?.textContent;

   assert.ok(content.classList.contains('itin-build-warnings'));
   assert.equal(modules.length, Position.THIRD);
   assert.equal(title, firstTitle);
});
