import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   getGuardiansTalksFromWithoutAnimalIssues,
   getPrimaryGuardiansTalkFromWithoutAnimalIssues,
   hasGuardiansTalkWithoutAnimalIssue,
   showGuardiansTalkWithoutAnimalConfirmation,
} from '../../scripts/itinerary/panel/guardiansTalkWithoutAnimalConfirmation.js';
import { installDomTestHooks } from './helpers/domTestSetup.mjs';

installDomTestHooks();

test('hasGuardiansTalkWithoutAnimalIssue detects matching issue type', () => {
   assert.equal(
      hasGuardiansTalkWithoutAnimalIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      true
   );
   assert.equal(
      hasGuardiansTalkWithoutAnimalIssue([
         { type: 'fixedTimeItemLongWait' },
      ]),
      false
   );
});

test('getPrimaryGuardiansTalkFromWithoutAnimalIssues returns talk without time', () => {
   assert.deepEqual(
      getPrimaryGuardiansTalkFromWithoutAnimalIssues([
         {
            type: 'guardiansTalkWithoutAnimal',
            items: [{ name: 'Komodo Dragon' }],
         },
      ]),
      { talkName: 'Komodo Dragon' }
   );
});

test('getGuardiansTalksFromWithoutAnimalIssues returns every named talk', () => {
   assert.deepEqual(
      getGuardiansTalksFromWithoutAnimalIssues([{
         type: 'guardiansTalkWithoutAnimal',
         items: [
            {
               name: 'Western Grey Kangaroo',
               start_time: '11:00 AM',
            },
            {
               name: 'African Lion',
               start_time: '2:00 PM',
            },
         ],
      }]),
      [
         {
            talkName: 'Western Grey Kangaroo',
            talkTime: '11:00 AM',
         },
         {
            talkName: 'African Lion',
            talkTime: '2:00 PM',
         },
      ]
   );
});

test('showGuardiansTalkWithoutAnimalConfirmation uses message without time', () => {
   let confirmed = false;

   showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{
         type: 'guardiansTalkWithoutAnimal',
         items: [{ name: 'Komodo Dragon' }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   });

   const popupMessage = document.querySelector('.tzg-popup-message');

   assert.equal(
      popupMessage?.textContent,
      'The Komodo Dragon guardians talk does not match an animal on your itinerary. Do you still want to keep it on your plan?'
   );

   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(confirmed, true);
});

test('showGuardiansTalkWithoutAnimalConfirmation no-ops for multiple talks', () => {
   showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{
         type: 'guardiansTalkWithoutAnimal',
         items: [
            { name: 'Western Grey Kangaroo' },
            { name: 'African Lion' },
         ],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});

test('showGuardiansTalkWithoutAnimalConfirmation no-ops without talk name', () => {
   showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{ type: 'guardiansTalkWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
