import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
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

test('showGuardiansTalkWithoutAnimalConfirmation no-ops without talk name', () => {
   showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{ type: 'guardiansTalkWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
