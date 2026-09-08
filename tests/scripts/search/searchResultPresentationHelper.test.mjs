import assert from 'node:assert/strict';
import test from 'node:test';

import { SearchResultPresentationHelper } from '../../../scripts/search/searchResultPresentationHelper.js';

test('Test_BuildNamedResultPresentation_TestRow_ExpectTitleAndSubtitle', () => {
   const presentation = SearchResultPresentationHelper.buildNamedResultPresentation(
      'Fallback',
      (row) => row.location
   );

   assert.equal(presentation.getTitle({ name: 'Lion Talk' }), 'Lion Talk');
   assert.equal(presentation.getTitle({}), 'Fallback');
   assert.equal(presentation.getSubtitle({ location: 'Theatre' }), 'Theatre');
});
