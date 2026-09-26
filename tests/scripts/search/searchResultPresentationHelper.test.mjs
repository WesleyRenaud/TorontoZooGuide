import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchResultPresentationHelper } from '../../../scripts/search/searchResultPresentationHelper.js';


test('Test_BuildNamedResultPresentation_TestNamedRow_ExpectTitle', () => {
   const fallbackTitle = 'Fallback';
   const name = 'Lion Talk';
   const presentation = SearchResultPresentationHelper.buildNamedResultPresentation(
      fallbackTitle,
      (row) => row.location
   );

   const title = presentation.getTitle({ name });

   assert.equal(title, name);
});


test('Test_BuildNamedResultPresentation_TestMissingName_ExpectFallback', () => {
   const fallbackTitle = 'Fallback';
   const presentation = SearchResultPresentationHelper.buildNamedResultPresentation(
      fallbackTitle,
      (row) => row.location
   );

   const title = presentation.getTitle({});

   assert.equal(title, fallbackTitle);
});


test('Test_BuildNamedResultPresentation_TestLocation_ExpectSubtitle', () => {
   const fallbackTitle = 'Fallback';
   const location = 'Theatre';
   const presentation = SearchResultPresentationHelper.buildNamedResultPresentation(
      fallbackTitle,
      (row) => row.location
   );

   const subtitle = presentation.getSubtitle({ location });

   assert.equal(subtitle, location);
});
