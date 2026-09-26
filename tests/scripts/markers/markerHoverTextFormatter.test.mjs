import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHoverTextFormatter } from '../../../scripts/markers/markerHoverTextFormatter.js';
import { Position } from '../../../scripts/shared/enums/position.js';
import { Strings } from '../../../scripts/strings.js';


test('Test_ReadItemText_TestField_ExpectValue', () => {
   const title = 'Restroom';
   const fallback = 'Fallback';
   const item = { title };

   const text = MarkerHoverTextFormatter.readItemText(item, 'title', fallback);

   assert.equal(text, title);
});


test('Test_ReadItemText_TestMissingField_ExpectFallback', () => {
   const fallback = 'Fallback';
   const item = {};

   const text = MarkerHoverTextFormatter.readItemText(item, 'title', fallback);

   assert.equal(text, fallback);
});


test('Test_FormatCountedHoverText_TestSingle_ExpectTitle', () => {
   const name = 'African Lion';
   const items = [{ name }];

   const text = MarkerHoverTextFormatter.formatCountedHoverText(items, (item) => item.name);

   assert.equal(text, name);
});


test('Test_FormatCountedHoverText_TestMultiple_ExpectMoreCount', () => {
   const name = 'African Lion';
   const items = [{ name }, { name: 'Amur Tiger' }];

   const text = MarkerHoverTextFormatter.formatCountedHoverText(items, (item) => item.name);

   assert.equal(text, `${name} ${Strings.format.moreCount(items.length + Position.LAST)}`);
});


test('Test_FormatGuardiansTalkHoverText_TestNamed_ExpectNamedString', () => {
   const name = 'Lion Talk';
   const items = [{ name }];

   const text = MarkerHoverTextFormatter.formatGuardiansTalkHoverText(items);

   assert.equal(text, Strings.map.hover.guardiansTalkWithName(name));
});


test('Test_FormatGuardiansTalkHoverText_TestAnonymous_ExpectLabel', () => {
   const items = [{}];

   const text = MarkerHoverTextFormatter.formatGuardiansTalkHoverText(items);

   assert.equal(text, Strings.entityLabels.guardiansTalk);
});


test('Test_FormatGuardiansTalkHoverText_TestMultiple_ExpectMoreCount', () => {
   const name = 'Lion Talk';
   const items = [{ name }, {}];

   const text = MarkerHoverTextFormatter.formatGuardiansTalkHoverText(items);

   assert.equal(
      text,
      `${Strings.map.hover.guardiansTalkWithName(name)} ${Strings.format.moreCount(items.length + Position.LAST)}`
   );
});


test('Test_FormatWildEncounterHoverText_TestNamed_ExpectNamedString', () => {
   const name = 'Red Panda';
   const items = [{ name }];

   const text = MarkerHoverTextFormatter.formatWildEncounterHoverText(items);

   assert.equal(text, Strings.map.hover.wildEncounterMeetingSpotWithName(name));
});


test('Test_FormatWildEncounterHoverText_TestAnonymous_ExpectMeetingSpot', () => {
   const items = [{}];

   const text = MarkerHoverTextFormatter.formatWildEncounterHoverText(items);

   assert.equal(text, Strings.map.hover.wildEncounterMeetingSpot);
});


test('Test_FormatWildEncounterHoverText_TestMultiple_ExpectMultipleString', () => {
   const name = 'Red Panda';
   const items = [{ name }, { name: 'Otter' }];

   const text = MarkerHoverTextFormatter.formatWildEncounterHoverText(items);

   assert.equal(
      text,
      Strings.map.hover.wildEncounterMultiple(name, items.length + Position.LAST)
   );
});
