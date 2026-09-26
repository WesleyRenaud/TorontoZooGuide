import assert from 'node:assert/strict';
import { test } from 'node:test';

import { GuardiansTalkWithoutAnimalFragment } from '../../../../scripts/itinerary/panel/guardiansTalkWithoutAnimalFragment.js';
import { ItineraryErrorType } from '../../../../scripts/shared/enums/itineraryErrorType.js';
import { Strings } from '../../../../scripts/strings.js';
import { installDomTestHooks } from '../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_HasGuardiansTalkWithoutAnimalIssue_TestMatching_ExpectTrue', () => {
   const issues = [{ type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL }];

   const hasIssue = GuardiansTalkWithoutAnimalFragment.hasGuardiansTalkWithoutAnimalIssue(issues);

   assert.equal(hasIssue, true);
});


test('Test_HasGuardiansTalkWithoutAnimalIssue_TestOtherType_ExpectFalse', () => {
   const issues = [{ type: ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT }];

   const hasIssue = GuardiansTalkWithoutAnimalFragment.hasGuardiansTalkWithoutAnimalIssue(issues);

   assert.equal(hasIssue, false);
});


test('Test_GetPrimaryGuardiansTalkFromWithoutAnimalIssues_TestTalk_ExpectNoTime', () => {
   const talkName = 'Komodo Dragon';
   const issues = [{
      type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items: [{ name: talkName }],
   }];

   const talk = GuardiansTalkWithoutAnimalFragment.getPrimaryGuardiansTalkFromWithoutAnimalIssues(issues);

   assert.deepEqual(talk, { talkName });
});


test('Test_GetGuardiansTalksFromWithoutAnimalIssues_TestNamedTalks_ExpectAll', () => {
   const kangaroo = 'Western Grey Kangaroo';
   const kangarooTime = '11:00 AM';
   const lion = 'African Lion';
   const lionTime = '2:00 PM';
   const issues = [{
      type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items: [
         { name: kangaroo, start_time: kangarooTime },
         { name: lion, start_time: lionTime },
      ],
   }];

   const talks = GuardiansTalkWithoutAnimalFragment.getGuardiansTalksFromWithoutAnimalIssues(issues);

   assert.deepEqual(talks, [
      { talkName: kangaroo, talkTime: kangarooTime },
      { talkName: lion, talkTime: lionTime },
   ]);
});


test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMessage_ExpectNoTime', () => {
   const talkName = 'Komodo Dragon';
   let confirmed = false;

   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{
         type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         items: [{ name: talkName }],
      }],
      onConfirm: () => {
         confirmed = true;
      },
   });

   const popupMessage = document.querySelector('.tzg-popup-message');
   document.querySelector('.tzg-popup-confirm')?.click();

   assert.equal(
      popupMessage?.textContent,
      Strings.itinerary.confirmation.guardiansTalkWithoutAnimalMessageWithoutTime(talkName)
   );
   assert.equal(confirmed, true);
});


test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMultiple_ExpectNoOp', () => {
   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{
         type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
         items: [
            { name: 'Western Grey Kangaroo' },
            { name: 'African Lion' },
         ],
      }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});


test('Test_ShowGuardiansTalkWithoutAnimalConfirmation_TestMissingName_ExpectNoOp', () => {
   GuardiansTalkWithoutAnimalFragment.showGuardiansTalkWithoutAnimalConfirmation({
      issues: [{ type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL, items: [] }],
      onConfirm: () => {
         throw new Error('should not confirm');
      },
   });

   const popup = document.querySelector('.tzg-popup');

   assert.equal(popup, null);
});


test('Test_GetGuardiansTalkNamesFromWithoutAnimalIssues_TestNamesAndBlanks_ExpectFiltered', () => {
   const komodo = 'Komodo Dragon';
   const lion = 'African Lion';
   const issues = [{
      type: ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      items: [
         { name: `  ${komodo}  `, start_time: '11:00 AM' },
         { name: '' },
         { name: lion },
      ],
   }];

   const names = GuardiansTalkWithoutAnimalFragment.getGuardiansTalkNamesFromWithoutAnimalIssues(issues);

   assert.deepEqual(names, [komodo, lion]);
});
