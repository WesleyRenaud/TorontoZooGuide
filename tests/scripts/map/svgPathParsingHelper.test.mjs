import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParsingHelper } from '../../../scripts/map/svgPathParsingHelper.js';

test('Test_ReadNumber_TestTokenIndex_ExpectParsedFloat', () => {
   assert.equal(SvgPathParsingHelper.readNumber(['M', '12.5', 'L'], 1), 12.5);
   assert.equal(Number.isNaN(SvgPathParsingHelper.readNumber(['M'], 1)), true);
});
