import assert from 'node:assert/strict';
import test from 'node:test';

import { MarkerHoverTextFormatter } from '../../../scripts/markers/markerHoverTextFormatter.js';
import { Strings } from '../../../scripts/strings.js';

test('Test_ReadItemText_TestFieldOrFallback_ExpectValue', () => {
   assert.equal(
      MarkerHoverTextFormatter.readItemText({ title: 'Restroom' }, 'title', 'Fallback'),
      'Restroom'
   );
   assert.equal(
      MarkerHoverTextFormatter.readItemText({}, 'title', 'Fallback'),
      'Fallback'
   );
});

test('Test_FormatCountedHoverText_TestSingleAndMultiple_ExpectTitles', () => {
   assert.equal(
      MarkerHoverTextFormatter.formatCountedHoverText(
         [{ name: 'African Lion' }],
         (item) => item.name
      ),
      'African Lion'
   );
   assert.equal(
      MarkerHoverTextFormatter.formatCountedHoverText(
         [{ name: 'African Lion' }, { name: 'Amur Tiger' }],
         (item) => item.name
      ),
      'African Lion + 1'
   );
});

test('Test_FormatGuardiansTalkHoverText_TestNamedAndAnonymous_ExpectStrings', () => {
   assert.equal(
      MarkerHoverTextFormatter.formatGuardiansTalkHoverText([{ name: 'Lion Talk' }]),
      Strings.map.hover.guardiansTalkWithName('Lion Talk')
   );
   assert.equal(
      MarkerHoverTextFormatter.formatGuardiansTalkHoverText([{}]),
      Strings.entityLabels.guardiansTalk
   );
   assert.equal(
      MarkerHoverTextFormatter.formatGuardiansTalkHoverText([{ name: 'Lion Talk' }, {}]),
      `${Strings.map.hover.guardiansTalkWithName('Lion Talk')} + 1`
   );
});

test('Test_FormatWildEncounterHoverText_TestSingleAndMultiple_ExpectStrings', () => {
   assert.equal(
      MarkerHoverTextFormatter.formatWildEncounterHoverText([{ name: 'Red Panda' }]),
      Strings.map.hover.wildEncounterMeetingSpotWithName('Red Panda')
   );
   assert.equal(
      MarkerHoverTextFormatter.formatWildEncounterHoverText([{}]),
      Strings.map.hover.wildEncounterMeetingSpot
   );
   assert.equal(
      MarkerHoverTextFormatter.formatWildEncounterHoverText([
         { name: 'Red Panda' },
         { name: 'Otter' },
      ]),
      Strings.map.hover.wildEncounterMultiple('Red Panda', 1)
   );
});
