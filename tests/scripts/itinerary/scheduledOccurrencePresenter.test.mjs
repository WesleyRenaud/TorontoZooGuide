import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { ScheduledOccurrencePresenter } from '../../../scripts/itinerary/scheduledOccurrencePresenter.js';

test('Test_BuildOccurrenceDetailImageSrc_TestMissingName_ExpectNull', () => {
   assert.equal(ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc('animals', ''), null);
   assert.equal(ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc('animals', null), null);
});

test('Test_BuildOccurrenceDetailImageSrc_TestName_ExpectDetailImage', () => {
   const original = DetailImageBuilder.buildDetailImageSrc;
   DetailImageBuilder.buildDetailImageSrc = (dir, name, options) => `${dir}/${name}:${options.basePath}`;

   try {
      assert.equal(
         ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc('animals', 'African Lion'),
         'animals/African Lion:../images/details'
      );
   } finally {
      DetailImageBuilder.buildDetailImageSrc = original;
   }
});

test('Test_FormatOccurrenceTitleSuffix_TestNamePresent_ExpectLabeledSuffix', () => {
   assert.equal(ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix('Talk', ' Guardians'), '  Guardians');
   assert.equal(ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix('  ', ' Guardians'), '');
});

test('Test_FormatOccurrenceSearchTitle_TestNameAndLabel_ExpectCombined', () => {
   assert.equal(
      ScheduledOccurrencePresenter.formatOccurrenceSearchTitle('Amur Tiger', ' Talk'),
      'Amur Tiger  Talk'
   );
   assert.equal(ScheduledOccurrencePresenter.formatOccurrenceSearchTitle('', 'Talk'), 'Talk');
});

test('Test_BuildOccurrenceSubtitle_TestParts_ExpectJoinedOrDash', () => {
   assert.equal(
      ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
         primaryValue: 'African Rainforest',
         timeRange: '11:00 AM - 12:00 PM',
      }),
      'African Rainforest  •  11:00 AM - 12:00 PM'
   );
   assert.equal(ScheduledOccurrencePresenter.buildOccurrenceSubtitle({}), '-');
});
