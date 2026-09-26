import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduleTimeConflictView } from '../../../../scripts/itinerary/panel/scheduleTimeConflictView.js';
import { AssetKeyNormalizer } from '../../../../scripts/assets/assetKeyNormalizer.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { ItinerarySaveIssueItemType } from '../../../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.WILD_ENCOUNTER,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const guardiansTalk = {
   name: 'African Lion',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.GUARDIANS_TALK,
   location: 'Africa Savanna',
};

installDomTestHooks();


test('Test_BuildConflictItemImageSrc_TestWildEncounter_ExpectPath', () => {
   const src = ScheduleTimeConflictView.buildConflictItemImageSrc(firstEncounter);

   assert.equal(
      src,
      `images/details/wild-encounters/${AssetKeyNormalizer.normalize(firstEncounter.name)}.png`
   );
});


test('Test_BuildConflictItemImageSrc_TestGuardiansTalk_ExpectPath', () => {
   const src = ScheduleTimeConflictView.buildConflictItemImageSrc(guardiansTalk);

   assert.equal(
      src,
      `images/details/guardians-talks/${AssetKeyNormalizer.normalize(guardiansTalk.name)}.png`
   );
});


test('Test_BuildConflictItemImageSrc_TestBlankName_ExpectNull', () => {
   const item = { name: '' };

   const src = ScheduleTimeConflictView.buildConflictItemImageSrc(item);

   assert.equal(src, null);
});


test('Test_CreateSaveIssuesContent_TestNonWildEncounter_ExpectEmpty', () => {
   const issues = [{ type: 'otherIssue', items: [firstEncounter] }];

   const { content, conflictGroups } = ScheduleTimeConflictView.createSaveIssuesContent(issues);

   assert.equal(content.className, 'itin-save-issues');
   assert.equal(content.children.length, 0);
   assert.deepEqual(conflictGroups, []);
});


test('Test_CreateSaveIssuesContent_TestConflictRows_ExpectRendered', () => {
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [secondEncounter, firstEncounter],
   }];

   const { content, conflictGroups } = ScheduleTimeConflictView.createSaveIssuesContent(issues);

   const section = content.querySelector('.itin-save-issue-section');
   const rows = content.querySelectorAll('.itin-save-issue-conflict-row');
   const buttons = content.querySelectorAll('.itin-save-issue-select-btn');

   assert.ok(section);
   assert.equal(
      section?.querySelector('.itin-save-issue-section-title')?.textContent,
      Strings.itinerary.confirmation.scheduleConflictsTitle
   );
   assert.equal(rows.length, issues.at(Position.FIRST).items.length);
   assert.equal(buttons.length, issues.at(Position.FIRST).items.length);
   assert.equal(conflictGroups.length, 1);
   assert.equal(conflictGroups.at(Position.FIRST).items.length, issues.at(Position.FIRST).items.length);
   assert.deepEqual(
      new Set(
         [...rows].map(
            (row) => row.querySelector('.animal-result-species')?.textContent
         )
      ),
      new Set([firstEncounter.name, secondEncounter.name])
   );
   assert.ok(
      [...rows].every((row) => row.querySelector('.animal-result-exhibit'))
   );
});


test('Test_CreateSaveIssuesContent_TestToggleAdd_ExpectSelectedRemove', () => {
   const issues = [{
      type: ItineraryErrorType.WILD_ENCOUNTER_TIME_CONFLICT,
      items: [firstEncounter, secondEncounter],
   }];

   const { content } = ScheduleTimeConflictView.createSaveIssuesContent(issues);
   const [firstButton, secondButton] = content.querySelectorAll('.itin-save-issue-select-btn');

   firstButton?.click();

   assert.equal(firstButton?.textContent, Strings.itinerary.actions.remove);
   assert.equal(firstButton?.classList.contains('is-added'), true);
   assert.equal(secondButton?.disabled, true);
});
