/**
 * Region color identity for map + day planner.
 * Hex values live only in styles/tokens.css (--color-region-*).
 */

import { asTrimmedString } from '../api/normalizeValues.js';
import { normalizeAnimalIdentitySearchFields } from '../itinerary/animalIdentity.js';

export const REGION_COLOR_SLUGS = Object.freeze({
   Africa: 'africa',
   'Indo-Malaya': 'indo-malaya',
   'Canadian Domain': 'canadian-domain',
   'Discovery Zone': 'discovery-zone',
   Americas: 'americas',
   'Tundra Trek': 'tundra-trek',
   'Eurasia Wilds': 'eurasia-wilds',
   Australasia: 'australasia',
   'Front Courtyard': 'front-courtyard',
   'Wildlife Science Campus': 'wildlife-science-campus',
});

// Keep in sync with api/seed/data/exhibit.json.
const EXHIBIT_REGION_BY_NAME = Object.freeze({
   'australasia pavilion': 'Australasia',
   'australasia outdoor': 'Australasia',
   'eurasia wilds': 'Eurasia Wilds',
   'tundra trek': 'Tundra Trek',
   'americas outdoor mayan temple ruins': 'Americas',
   'americas pavilion': 'Americas',
   'canadian domain': 'Canadian Domain',
   'africa savanna': 'Africa',
   'african rainforest pavilion': 'Africa',
   'indo-malaya pavilion': 'Indo-Malaya',
   'indo-malaya outdoor': 'Indo-Malaya',
   'malayan woods pavilion': 'Indo-Malaya',
   'goat world': 'Discovery Zone',
   'kids zoo': 'Discovery Zone',
});

export function resolveRegionNameForExhibit(exhibitName = '') {
   const exhibitKey = normalizeAnimalIdentitySearchFields({
      exhibit: exhibitName,
   }).exhibit;

   if (!exhibitKey) {
      return '';
   }

   return EXHIBIT_REGION_BY_NAME[exhibitKey] ?? '';
}

export function resolveRegionColorSlug(regionName = '') {
   const regionKey = asTrimmedString(regionName);

   if (!regionKey) {
      return '';
   }

   return REGION_COLOR_SLUGS[regionKey] ?? '';
}

export function resolveRegionColorSlugForExhibit(exhibitName = '') {
   return resolveRegionColorSlug(resolveRegionNameForExhibit(exhibitName));
}

export function resolveRegionColorSlugForScheduledItem(item = null) {
   const region = asTrimmedString(item?.region);

   if (region) {
      return resolveRegionColorSlug(region);
   }

   const exhibit = asTrimmedString(item?.exhibit);

   if (exhibit) {
      return resolveRegionColorSlugForExhibit(exhibit);
   }

   const location = asTrimmedString(item?.location);

   if (location) {
      return resolveRegionColorSlugForExhibit(location);
   }

   return '';
}

export function applyRegionColorsToElement(element, regionSlug = '') {
   const slug = asTrimmedString(regionSlug);

   if (!element || !slug) {
      return false;
   }

   element.classList.add('itinerary-day-scheduled-pill--region-colored');
   element.classList.add(`itinerary-day-scheduled-pill--region-${slug}`);
   element.setAttribute('data-region-slug', slug);

   return true;
}
