import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ItinerarySaveIssueItemType } from '../../scripts/shared/enums/itinerarySaveIssueItemType.js';
import {
   buildConflictItemImageSrc,
   createSaveIssuesContent,
   WILD_ENCOUNTER_TIME_CONFLICT,
} from '../../scripts/itinerary/panel/scheduleTimeConflictContent.js';
import { APP_STRINGS } from '../../scripts/strings.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

const firstEncounter = {
   name: 'From Howls to Honks',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Mayan Temple Meeting Spot',
};

const secondEncounter = {
   name: 'Great Barrier Reef',
   start_time: '13:00',
   end_time: '13:45',
   item_type: ItinerarySaveIssueItemType.wildEncounter,
   meeting_spot: 'Wild Encounter - Eurasia Meeting Spot',
};

const guardiansTalk = {
   name: 'African Lion',
   start_time: '14:00',
   end_time: '14:30',
   item_type: ItinerarySaveIssueItemType.guardiansTalk,
   location: 'Africa Savanna',
};

test('buildConflictItemImageSrc maps wild encounters and guardians talks to detail images', () => {
   assert.equal(
      buildConflictItemImageSrc(firstEncounter),
      'images/details/wild-encounters/from-howls-to-honks.png'
   );
   assert.equal(
      buildConflictItemImageSrc(guardiansTalk),
      'images/details/guardians-talks/african-lion.png'
   );
   assert.equal(buildConflictItemImageSrc({ name: '' }), null);
});

test.describe('scheduleTimeConflictContent', () => {
   installDomTestHooks();

   test('createSaveIssuesContent ignores non-wild-encounter issues', () => {
      const { content, conflictGroups } = createSaveIssuesContent([
         { type: 'otherIssue', items: [firstEncounter] },
      ]);

      assert.equal(content.className, 'itin-save-issues');
      assert.equal(content.children.length, 0);
      assert.deepEqual(conflictGroups, []);
   });

   test('createSaveIssuesContent renders conflict rows and selection groups', () => {
      const { content, conflictGroups } = createSaveIssuesContent([
         {
            type: WILD_ENCOUNTER_TIME_CONFLICT,
            items: [secondEncounter, firstEncounter],
         },
      ]);

      const section = content.querySelector('.itin-save-issue-section');
      const rows = content.querySelectorAll('.itin-save-issue-conflict-row');
      const buttons = content.querySelectorAll('.itin-save-issue-select-btn');

      assert.ok(section);
      assert.equal(
         section?.querySelector('.itin-save-issue-section-title')?.textContent,
         APP_STRINGS.itinerary.confirmation.scheduleConflictsTitle
      );
      assert.equal(rows.length, 2);
      assert.equal(buttons.length, 2);
      assert.equal(conflictGroups.length, 1);
      assert.equal(conflictGroups[0].items.length, 2);
      assert.deepEqual(
         new Set(
            [...rows].map(
               row => row.querySelector('.animal-result-species')?.textContent
            )
         ),
         new Set(['From Howls to Honks', 'Great Barrier Reef'])
      );
      assert.ok(
         rows.every(row => row.querySelector('.animal-result-exhibit'))
      );
   });

   test('createSaveIssuesContent toggles add buttons into selected remove buttons', () => {
      const { content } = createSaveIssuesContent([
         {
            type: WILD_ENCOUNTER_TIME_CONFLICT,
            items: [firstEncounter, secondEncounter],
         },
      ]);

      const [firstButton, secondButton] = content.querySelectorAll(
         '.itin-save-issue-select-btn'
      );

      assert.equal(
         firstButton?.textContent,
         APP_STRINGS.itinerary.actions.addSymbol
      );

      firstButton?.click();

      assert.equal(
         firstButton?.textContent,
         APP_STRINGS.itinerary.actions.remove
      );
      assert.equal(firstButton?.classList.contains('is-added'), true);
      assert.equal(secondButton?.disabled, true);
   });
});
