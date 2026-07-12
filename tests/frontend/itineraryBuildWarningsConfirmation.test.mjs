import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   buildConfirmedOptionsFromBuildWarnings,
   buildItineraryBuildWarningSections,
   hasMultipleItineraryBuildWarnings,
   showItineraryBuildWarningsConfirmation,
} from '../../scripts/itinerary/panel/itineraryBuildWarningsConfirmation.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

const overlapAndWithoutAnimalIssues = [
   {
      type: 'guardiansTalkWillUnscheduleItems',
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
   {
      type: 'guardiansTalkWithoutAnimal',
      items: [{
         name: 'Amur Tiger',
         start_time: '11:00 AM',
      }],
   },
];

test('hasMultipleItineraryBuildWarnings detects multiple warning types', () => {
   assert.equal(
      hasMultipleItineraryBuildWarnings(overlapAndWithoutAnimalIssues),
      true
   );
   assert.equal(
      hasMultipleItineraryBuildWarnings([
         overlapAndWithoutAnimalIssues[0],
      ]),
      false
   );
});

test('buildConfirmedOptionsFromBuildWarnings sets all matching flags', () => {
   assert.deepEqual(
      buildConfirmedOptionsFromBuildWarnings(overlapAndWithoutAnimalIssues),
      {
         confirmingGuardiansTalkUnschedule: true,
         confirmingGuardiansTalkWithoutAnimal: true,
      }
   );
});

test('buildItineraryBuildWarningSections includes each warning message', () => {
   const sections = buildItineraryBuildWarningSections(
      overlapAndWithoutAnimalIssues
   );

   assert.equal(sections.length, 2);
   assert.equal(sections[0].type, 'guardiansTalkWillUnscheduleItems');
   assert.equal(sections[0].title, 'Schedule overlap');
   assert.match(sections[0].message, /Amur Tiger/);
   assert.equal(sections[1].type, 'guardiansTalkWithoutAnimal');
   assert.equal(sections[1].title, 'No matching animal');
   assert.match(sections[1].message, /does not match an animal/);
});

test('buildItineraryBuildWarningSections covers encounter and no-time copy', () => {
   const sections = buildItineraryBuildWarningSections([
      {
         type: 'wildEncounterWillUnscheduleItems',
         items: [{ name: 'Capybara' }],
      },
      {
         type: 'guardiansTalkWillUnscheduleItems',
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: 'guardiansTalkWithoutAnimal',
         items: [{ name: 'Amur Tiger' }],
      },
      {
         type: 'guardiansTalkLongWait',
         items: [{ name: 'Amur Tiger' }],
      },
   ]);

   assert.deepEqual(
      sections.map((section) => section.type),
      [
         'guardiansTalkWillUnscheduleItems',
         'wildEncounterWillUnscheduleItems',
         'guardiansTalkWithoutAnimal',
         'guardiansTalkLongWait',
      ]
   );
   assert.match(sections[0].message, /Amur Tiger guardians talk overlaps/);
   assert.match(sections[1].message, /Capybara wild encounter overlaps/);
   assert.match(sections[2].message, /does not match an animal on your itinerary\.$/);
   assert.match(sections[3].message, /is a long wait from your other scheduled items\.$/);
});

test('showItineraryBuildWarningsConfirmation shows all warnings in one popup', () => {
   let confirmed = false;

   showItineraryBuildWarningsConfirmation({
      issues: overlapAndWithoutAnimalIssues,
      onConfirm: () => {
         confirmed = true;
      },
   });

   const titles = [...document.querySelectorAll('.itin-build-warning-module-title')]
      .map((el) => el.textContent);
   const messages = [...document.querySelectorAll('.itin-build-warning-module-message')]
      .map((el) => el.textContent);

   assert.equal(
      document.querySelector('.itin-top-title')?.textContent,
      'Your Itinerary Has the Following Issues:'
   );
   assert.equal(
      document.querySelectorAll('.itin-build-warning-module').length,
      2
   );
   assert.deepEqual(titles, [
      'Schedule overlap',
      'No matching animal',
   ]);
   assert.equal(messages.length, 2);
   assert.doesNotMatch(messages.join(' '), /\?/);

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('showItineraryBuildWarningsConfirmation cancels when no sections', () => {
   let cancelled = false;

   showItineraryBuildWarningsConfirmation({
      issues: [],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
      onCancel: () => {
         cancelled = true;
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
   assert.equal(cancelled, true);
});
