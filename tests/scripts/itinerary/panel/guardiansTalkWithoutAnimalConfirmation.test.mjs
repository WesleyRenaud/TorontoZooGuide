import assert from 'node:assert/strict';
import { test } from 'node:test';

import { GuardiansTalkWithoutAnimalConfirmation } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalConfirmation.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_HasGuardiansTalkWithoutAnimalIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      GuardiansTalkWithoutAnimalConfirmation.hasGuardiansTalkWithoutAnimalIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      true
   );
   assert.equal(
      GuardiansTalkWithoutAnimalConfirmation.hasGuardiansTalkWithoutAnimalIssue([
         { type: 'fixedTimeItemLongWait' },
      ]),
      false
   );
});

test('Test_GetPrimaryGuardiansTalkFromWithoutAnimalIssues_TestTalk_ExpectNoTime', () => {
   assert.deepEqual(
      GuardiansTalkWithoutAnimalConfirmation.getPrimaryGuardiansTalkFromWithoutAnimalIssues([
         {
            type: 'guardiansTalkWithoutAnimal',
            items: [{ name: 'Komodo Dragon' }],
         },
      ]),
      { talkName: 'Komodo Dragon' }
   );
});

test('Test_GetGuardiansTalksFromWithoutAnimalIssues_TestNamedTalks_ExpectAll', () => {
   assert.deepEqual(
      GuardiansTalkWithoutAnimalConfirmation.getGuardiansTalksFromWithoutAnimalIssues([{
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

test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   let confirmed = false;

   GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation({
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

test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMultiple_ExpectNoOp', () => {
   GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation({
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

test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMissingName_ExpectNoOp', () => {
   GuardiansTalkWithoutAnimalConfirmation.showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{ type: 'guardiansTalkWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});
