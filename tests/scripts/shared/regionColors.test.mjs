import assert from 'node:assert/strict';
import { test } from 'node:test';

import { ScheduledTimelineView } from '../../../scripts/itinerary/panel/components/scheduledTimelineView.js';
import { RegionColors } from '../../../scripts/shared/regionColors.js';
import {
   createNode,
   installPanelRowsTestHooks,
} from '../helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();


test('Test_ResolveRegionNameForExhibit_TestAfricaSavanna_ExpectAfrica', () => {
   const exhibit = 'Africa Savanna';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, RegionColors.EXHIBIT_REGION_BY_NAME[exhibit.toLowerCase()]);
});


test('Test_ResolveRegionNameForExhibit_TestAmericasRuins_ExpectAmericas', () => {
   const exhibit = 'Americas Outdoor Mayan Temple Ruins';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, RegionColors.EXHIBIT_REGION_BY_NAME[exhibit.toLowerCase()]);
});


test('Test_ResolveRegionNameForExhibit_TestKidsZoo_ExpectDiscoveryZone', () => {
   const exhibit = 'Kids Zoo';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, RegionColors.EXHIBIT_REGION_BY_NAME[exhibit.toLowerCase()]);
});


test('Test_ResolveRegionNameForExhibit_TestUnknown_ExpectEmpty', () => {
   const exhibit = 'Unknown Exhibit';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, '');
});


test('Test_ResolveRegionNameForExhibit_TestEmpty_ExpectEmpty', () => {
   const exhibit = '';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, exhibit);
});


test('Test_ResolveRegionNameForExhibit_TestBlank_ExpectEmpty', () => {
   const exhibit = '   ';

   const region = RegionColors.resolveRegionNameForExhibit(exhibit);

   assert.equal(region, '');
});


test('Test_ResolveRegionColorSlug_TestAfrica_ExpectSlug', () => {
   const region = 'Africa';

   const slug = RegionColors.resolveRegionColorSlug(region);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[region]);
});


test('Test_ResolveRegionColorSlug_TestEmpty_ExpectEmpty', () => {
   const region = '';

   const slug = RegionColors.resolveRegionColorSlug(region);

   assert.equal(slug, region);
});


test('Test_ResolveRegionColorSlug_TestBlank_ExpectEmpty', () => {
   const region = '   ';

   const slug = RegionColors.resolveRegionColorSlug(region);

   assert.equal(slug, '');
});


test('Test_ResolveRegionColorSlugForExhibit_TestCanadianDomain_ExpectSlug', () => {
   const exhibit = 'Canadian Domain';

   const slug = RegionColors.resolveRegionColorSlugForExhibit(exhibit);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[exhibit]);
});


test('Test_ResolveRegionColorSlug_TestFrontCourtyard_ExpectSlug', () => {
   const region = 'Front Courtyard';

   const slug = RegionColors.resolveRegionColorSlug(region);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[region]);
});


test('Test_ResolveRegionColorSlug_TestWildlifeScienceCampus_ExpectSlug', () => {
   const region = 'Wildlife Science Campus';

   const slug = RegionColors.resolveRegionColorSlug(region);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[region]);
});


test('Test_ResolveRegionColorSlugForScheduledItem_TestExhibit_ExpectSlug', () => {
   const exhibit = 'Africa Savanna';
   const item = {
      species: 'African Lion',
      exhibit,
   };

   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.equal(slug, RegionColors.resolveRegionColorSlugForExhibit(exhibit));
});


test('Test_ResolveRegionColorSlugForScheduledItem_TestFrontCourtyard_ExpectSlug', () => {
   const region = 'Front Courtyard';
   const item = {
      name: 'Zoomobile',
      region,
   };

   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[region]);
});


test('Test_ResolveRegionColorSlugForScheduledItem_TestWildlifeCampus_ExpectSlug', () => {
   const region = 'Wildlife Science Campus';
   const item = {
      name: 'Greenhouse',
      region,
   };

   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.equal(slug, RegionColors.REGION_COLOR_SLUGS[region]);
});


test('Test_ResolveRegionColorSlugForScheduledItem_TestLocation_ExpectSlug', () => {
   const location = 'Australasia Pavilion';
   const item = {
      name: 'Komodo Dragon',
      location,
   };

   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.equal(slug, RegionColors.resolveRegionColorSlugForExhibit(location));
});


test('Test_ResolveRegionColorSlugForScheduledItem_TestNameOnly_ExpectEmpty', () => {
   const item = {
      name: 'African Lion',
   };

   const slug = RegionColors.resolveRegionColorSlugForScheduledItem(item);

   assert.equal(slug, '');
});


test('Test_ApplyRegionColorsToElement_TestSlug_ExpectClassAndData', () => {
   const pill = createNode('div');
   const slug = RegionColors.REGION_COLOR_SLUGS.Americas;

   const applied = RegionColors.applyRegionColorsToElement(pill, slug);

   assert.equal(applied, true);
   assert.equal(pill.getAttribute('data-region-slug'), slug);
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(pill.classList.contains(`itinerary-day-scheduled-pill--region-${slug}`));
});


test('Test_MakeScheduledPill_TestAnimalExhibit_ExpectRegionColored', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const minutes = 30;

   const pill = ScheduledTimelineView.makeScheduledPill(species, minutes, {
      item: {
         species,
         exhibit,
      },
   });
   const slug = RegionColors.resolveRegionColorSlugForExhibit(exhibit);

   assert.ok(pill);
   assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--region-colored'));
   assert.ok(pill.classList.contains(`itinerary-day-scheduled-pill--region-${slug}`));
   assert.equal(pill.getAttribute('data-region-slug'), slug);
});


test('Test_MakeScheduledPill_TestNonAnimal_ExpectUncolored', () => {
   const name = 'Lunch';
   const minutes = 40;

   const pill = ScheduledTimelineView.makeScheduledPill(name, minutes, {
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
