import assert from 'node:assert/strict';
import test from 'node:test';

import { SvgPathParsingHelper } from '../../../scripts/map/svgPathParsingHelper.js';
import { Position } from '../../../scripts/shared/enums/position.js';


test('Test_ReadNumber_TestTokenIndex_ExpectParsedFloat', () => {
   const value = '12.5';
   const tokens = ['M', value, 'L'];

   const number = SvgPathParsingHelper.readNumber(tokens, Position.SECOND);

   assert.equal(number, Number(value));
});


test('Test_ReadNumber_TestMissingToken_ExpectNaN', () => {
   const tokens = ['M'];

   const number = SvgPathParsingHelper.readNumber(tokens, Position.SECOND);

   assert.equal(Number.isNaN(number), true);
});
