import assert from 'node:assert/strict';
import test from 'node:test';

import { DetailImageBuilder } from '../../../scripts/assets/detailImageBuilder.js';
import { ScheduledOccurrencePresenter } from '../../../scripts/itinerary/scheduledOccurrencePresenter.js';


test('Test_BuildOccurrenceDetailImageSrc_TestEmptyName_ExpectNull', () => {
   const directory = 'animals';
   const name = '';

   const src = ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(directory, name);

   assert.equal(src, null);
});


test('Test_BuildOccurrenceDetailImageSrc_TestNullName_ExpectNull', () => {
   const directory = 'animals';
   const name = null;

   const src = ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(directory, name);

   assert.equal(src, null);
});


test('Test_BuildOccurrenceDetailImageSrc_TestName_ExpectDetailImage', () => {
   const original = DetailImageBuilder.buildDetailImageSrc;
   DetailImageBuilder.buildDetailImageSrc = (dir, name, options) => `${dir}/${name}:${options.basePath}`;
   const directory = 'animals';
   const name = 'African Lion';

   try {
      const src = ScheduledOccurrencePresenter.buildOccurrenceDetailImageSrc(directory, name);

      assert.equal(src, `${directory}/${name}:../images/details`);
   } finally {
      DetailImageBuilder.buildDetailImageSrc = original;
   }
});


test('Test_FormatOccurrenceTitleSuffix_TestNamePresent_ExpectLabeledSuffix', () => {
   const name = 'Talk';
   const label = ' Guardians';

   const suffix = ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(name, label);

   assert.equal(suffix, ` ${label}`);
});


test('Test_FormatOccurrenceTitleSuffix_TestBlankName_ExpectEmpty', () => {
   const name = '  ';
   const label = ' Guardians';

   const suffix = ScheduledOccurrencePresenter.formatOccurrenceTitleSuffix(name, label);

   assert.equal(suffix, '');
});


test('Test_FormatOccurrenceSearchTitle_TestNameAndLabel_ExpectCombined', () => {
   const name = 'Amur Tiger';
   const label = ' Talk';

   const title = ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(name, label);

   assert.equal(title, `${name} ${label}`);
});


test('Test_FormatOccurrenceSearchTitle_TestEmptyName_ExpectLabel', () => {
   const name = '';
   const label = 'Talk';

   const title = ScheduledOccurrencePresenter.formatOccurrenceSearchTitle(name, label);

   assert.equal(title, label);
});


test('Test_BuildOccurrenceSubtitle_TestParts_ExpectJoined', () => {
   const primaryValue = 'African Rainforest';
   const timeRange = '11:00 AM - 12:00 PM';

   const subtitle = ScheduledOccurrencePresenter.buildOccurrenceSubtitle({
      primaryValue,
      timeRange,
   });

   assert.equal(subtitle, `${primaryValue}  •  ${timeRange}`);
});


test('Test_BuildOccurrenceSubtitle_TestMissing_ExpectDash', () => {
   const parts = {};

   const subtitle = ScheduledOccurrencePresenter.buildOccurrenceSubtitle(parts);

   assert.equal(subtitle, '-');
});
