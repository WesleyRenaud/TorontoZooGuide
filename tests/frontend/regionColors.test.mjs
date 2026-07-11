import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   applyRegionColorsToElement,
   REGION_COLOR_SLUGS,
   resolveRegionColorSlug,
   resolveRegionColorSlugForExhibit,
   resolveRegionColorSlugForScheduledItem,
   resolveRegionNameForExhibit,
} from '../../scripts/shared/regionColors.js';
import { makeScheduledPill } from '../../scripts/itinerary/panel/components/scheduledTimelinePill.js';
import {
   createNode,
   installPanelRowsTestHooks,
} from './helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();

test('resolveRegionNameForExhibit maps exhibits to their regions', () => {
   assert.equal(resolveRegionNameForExhibit('Africa Savanna'), 'Africa');
   assert.equal(
      resolveRegionNameForExhibit('Americas Outdoor Mayan Temple Ruins'),
      'Americas'
   );
   assert.equal(resolveRegionNameForExhibit('Kids Zoo'), 'Discovery Zone');
   assert.equal(resolveRegionNameForExhibit('Unknown Exhibit'), '');
});

test('resolveRegionColorSlug maps regions to shared token slugs', () => {
   assert.equal(resolveRegionColorSlug('Africa'), 'africa');
   assert.equal(
      resolveRegionColorSlugForExhibit('Canadian Domain'),
      REGION_COLOR_SLUGS['Canadian Domain']
   );
   assert.equal(resolveRegionColorSlug('Front Courtyard'), '');
});

test('resolveRegionColorSlugForScheduledItem uses animal exhibit only', () => {
   assert.equal(
      resolveRegionColorSlugForScheduledItem({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'africa'
   );
   assert.equal(
      resolveRegionColorSlugForScheduledItem({
         name: 'African Lion',
         location: 'Africa Savanna',
      }),
      ''
   );
});

test('applyRegionColorsToElement sets region class and data attribute', () => {
   const pill = createNode('div');

   assert.equal(applyRegionColorsToElement(pill, 'americas'), true);
   assert.equal(pill.getAttribute('data-region-slug'), 'americas');
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-americas'));
});

test('makeScheduledPill colors animal pills by exhibit region', () => {
   const pill = makeScheduledPill('African Lion', 30, {
      item: {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      },
   });

   assert.ok(pill);
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-africa'));
   assert.equal(pill.getAttribute('data-region-slug'), 'africa');
});

test('makeScheduledPill leaves non-animal pills uncolored by region', () => {
   const pill = makeScheduledPill('Lunch', 40, {
      item: {
         event_type: 'lunch',
      },
   });

   assert.ok(pill);
   assert.equal(
      pill.classList.contains('itinerary-day-scheduled-pill--region-colored'),
      false
   );
});
