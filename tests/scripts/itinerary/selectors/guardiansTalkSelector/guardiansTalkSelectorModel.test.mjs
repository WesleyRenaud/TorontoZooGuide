import assert from 'node:assert/strict';
import test from 'node:test';

import { GuardiansTalkSelectorModel } from '../../../../../scripts/itinerary/selectors/guardiansTalkSelector/guardiansTalkSelectorModel.js';
import { Strings } from '../../../../../scripts/strings.js';

const talkRow = {
   name: 'Amur Tiger',
   location: 'Eurasia',
   start_time: '11:00 AM',
   end_time: '11:20 AM',
};

test('Test_GetGuardiansTalkNameAndLocation_TestRow_ExpectStrings', () => {
   assert.equal(GuardiansTalkSelectorModel.getGuardiansTalkName(talkRow), 'Amur Tiger');
   assert.equal(GuardiansTalkSelectorModel.getGuardiansTalkName({}), '');
   assert.equal(GuardiansTalkSelectorModel.getGuardiansTalkLocation(talkRow), 'Eurasia');
   assert.equal(GuardiansTalkSelectorModel.getGuardiansTalkLocation({}), '');
});

test('Test_GetGuardiansTalkId_TestRow_ExpectWireKey', () => {
   assert.equal(
      GuardiansTalkSelectorModel.getGuardiansTalkId(talkRow),
      'Amur Tiger||11:00 AM||11:20 AM'
   );
   assert.equal(GuardiansTalkSelectorModel.getGuardiansTalkId({ name: 'Talk' }), '');
});

test('Test_FormatGuardiansTalkTitles_TestName_ExpectLabeled', () => {
   assert.equal(
      GuardiansTalkSelectorModel.formatGuardiansTalkSearchTitle('Amur Tiger'),
      `Amur Tiger${GuardiansTalkSelectorModel.formatGuardiansTalkTitleSuffix('Amur Tiger')}`
   );
   assert.match(
      GuardiansTalkSelectorModel.getGuardiansTalkSearchTitle(talkRow),
      new RegExp(Strings.entityLabels.guardiansTalk)
   );
});

test('Test_GetGuardiansTalkSubtitle_TestRow_ExpectJoined', () => {
   assert.match(GuardiansTalkSelectorModel.getGuardiansTalkSubtitle(talkRow), /Eurasia/);
});

test('Test_BuildGuardiansTalkSelectionAndStoredFields_TestRow_ExpectFields', () => {
   assert.deepEqual(GuardiansTalkSelectorModel.buildGuardiansTalkSelectionFields(talkRow), {
      location: 'Eurasia',
      start_time: '11:00 AM',
      end_time: '11:20 AM',
   });
   assert.deepEqual(GuardiansTalkSelectorModel.readGuardiansTalkStoredFields(talkRow), {
      location: 'Eurasia',
      start_time: '11:00 AM',
      end_time: '11:20 AM',
   });
});

test('Test_BuildGuardiansTalkImageSrc_TestName_ExpectDetailPath', () => {
   assert.match(
      GuardiansTalkSelectorModel.buildGuardiansTalkImageSrc(talkRow) ?? '',
      /guardians-talks/
   );
});
