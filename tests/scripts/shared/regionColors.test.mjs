import assert from 'node:assert/strict';
import { test } from 'node:test';

import { RegionColors } from '../../../scripts/shared/regionColors.js';
import { ScheduledTimelinePill } from '../../../scripts/itinerary/panel/components/scheduledTimelinePill.js';
import {
   createNode,
   installPanelRowsTestHooks,
} from '../helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();

test('Test_ResolveRegionNameForExhibit_TestKnownExhibits_ExpectRegions', () => {
   assert.equal(RegionColors.resolveRegionNameForExhibit('Africa Savanna'), 'Africa');
   assert.equal(
      RegionColors.resolveRegionNameForExhibit('Americas Outdoor Mayan Temple Ruins'),
      'Americas'
   );
   assert.equal(RegionColors.resolveRegionNameForExhibit('Kids Zoo'), 'Discovery Zone');
   assert.equal(RegionColors.resolveRegionNameForExhibit('Unknown Exhibit'), '');
});

test('Test_ResolveRegionColorSlug_TestRegions_ExpectSlugs', () => {
   assert.equal(RegionColors.resolveRegionColorSlug('Africa'), 'africa');
   assert.equal(
      RegionColors.resolveRegionColorSlugForExhibit('Canadian Domain'),
      RegionColors.REGION_COLOR_SLUGS['Canadian Domain']
   );
   assert.equal(
      RegionColors.resolveRegionColorSlug('Front Courtyard'),
      RegionColors.REGION_COLOR_SLUGS['Front Courtyard']
   );
   assert.equal(
      RegionColors.resolveRegionColorSlug('Wildlife Science Campus'),
      'wildlife-science-campus'
   );
});

test('Test_ResolveRegionColorSlugForScheduledItem_TestFallbacks_ExpectSlug', () => {
   assert.equal(
      RegionColors.resolveRegionColorSlugForScheduledItem({
         species: 'African Lion',
         exhibit: 'Africa Savanna',
      }),
      'africa'
   );
   assert.equal(
      RegionColors.resolveRegionColorSlugForScheduledItem({
         name: 'Zoomobile',
         region: 'Front Courtyard',
      }),
      'front-courtyard'
   );
   assert.equal(
      RegionColors.resolveRegionColorSlugForScheduledItem({
         name: 'Greenhouse',
         region: 'Wildlife Science Campus',
      }),
      'wildlife-science-campus'
   );
   assert.equal(
      RegionColors.resolveRegionColorSlugForScheduledItem({
         name: 'Komodo Dragon',
         location: 'Australasia Pavilion',
      }),
      'australasia'
   );
   assert.equal(
      RegionColors.resolveRegionColorSlugForScheduledItem({
         name: 'African Lion',
      }),
      ''
   );
});

test('Test_ApplyRegionColorsToElement_TestSlug_ExpectClassAndData', () => {
   const pill = createNode('div');

   assert.equal(RegionColors.applyRegionColorsToElement(pill, 'americas'), true);
   assert.equal(pill.getAttribute('data-region-slug'), 'americas');
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-americas'));
});

test('Test_MakeScheduledPill_TestAnimalExhibit_ExpectRegionColored', () => {
   const pill = ScheduledTimelinePill.makeScheduledPill('African Lion', 30, {
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

test('Test_MakeScheduledPill_TestNonAnimal_ExpectUncolored', () => {
   const pill = ScheduledTimelinePill.makeScheduledPill('Lunch', 40, {
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
