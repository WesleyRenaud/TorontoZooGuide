import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgConstants } from '../../../scripts/shared/svgConstants.js';

test('Test_SvgConstants_TestSvgNamespace_ExpectValue', () => {
   assert.equal(SvgConstants.SVG_NS, 'http://www.w3.org/2000/svg');
});
