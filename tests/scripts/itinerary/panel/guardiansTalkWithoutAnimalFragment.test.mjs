import assert from 'node:assert/strict';
import { test } from 'node:test';

import { GuardiansTalkWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_HasGuardiansTalkWithoutAnimalIssue_TestMatching_ExpectDetected', () => {
   assert.equal(
      GuardiansTalkWithoutAnimalFragment.hasGuardiansTalkWithoutAnimalIssue([
         { type: 'guardiansTalkWithoutAnimal' },
      ]),
      true
   );
   assert.equal(
      GuardiansTalkWithoutAnimalFragment.hasGuardiansTalkWithoutAnimalIssue([
         { type: 'fixedTimeItemLongWait' },
      ]),
      false
   );
});

test('Test_GetPrimaryGuardiansTalkFromWithoutAnimalIssues_TestTalk_ExpectNoTime', () => {
   assert.deepEqual(
      GuardiansTalkWithoutAnimalFragment.getPrimaryGuardiansTalkFromWithoutAnimalIssues([
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
      GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues([{
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

   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
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
   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
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
   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{ type: 'guardiansTalkWithoutAnimal', items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   assert.equal(document.querySelector('.tzg-popup'), null);
});

test('Test_GetGuardiansTalkNamesFromWithoutAnimalIssues_TestNamesAndBlanks_ExpectFiltered', () => {
   assert.deepEqual(
      GuardiansTalkWithoutAnimalFragment.getGuardiansTalkNamesFromWithoutAnimalIssues([{
         type: 'guardiansTalkWithoutAnimal',
         items: [
            { name: '  Komodo Dragon  ', start_time: '11:00 AM' },
            { name: '' },
            { name: 'African Lion' },
         ],
      }]),
      ['Komodo Dragon', 'African Lion']
   );
});
