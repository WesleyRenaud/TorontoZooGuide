/**
 * Region color identity for map + day planner.
 * Hex values live only in styles/tokens.css (--color-region-*).
 */

import { ValueNormalizer } from '../api/valueNormalizer.js';
import { AnimalIdentity } from '../itinerary/animalIdentity.js';

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

export class RegionColors {
   static REGION_COLOR_SLUGS = Object.freeze({
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

   static resolveRegionNameForExhibit(exhibitName = '') {
      const exhibitKey = AnimalIdentity.normalizeAnimalIdentitySearchFields({
         exhibit: exhibitName,
      }).exhibit;

      if (!exhibitKey) {
         return '';
      }

      return EXHIBIT_REGION_BY_NAME[exhibitKey] ?? '';
   }

   static resolveRegionColorSlug(regionName = '') {
      const regionKey = ValueNormalizer.asTrimmedString(regionName);

      if (!regionKey) {
         return '';
      }

      return RegionColors.REGION_COLOR_SLUGS[regionKey] ?? '';
   }

   static resolveRegionColorSlugForExhibit(exhibitName = '') {
      return RegionColors.resolveRegionColorSlug(
         RegionColors.resolveRegionNameForExhibit(exhibitName)
      );
   }

   static resolveRegionColorSlugForScheduledItem(item = null) {
      const region = ValueNormalizer.asTrimmedString(item?.region);

      if (region) {
         return RegionColors.resolveRegionColorSlug(region);
      }

      const exhibit = ValueNormalizer.asTrimmedString(item?.exhibit);

      if (exhibit) {
         return RegionColors.resolveRegionColorSlugForExhibit(exhibit);
      }

      const location = ValueNormalizer.asTrimmedString(item?.location);

      if (location) {
         return RegionColors.resolveRegionColorSlugForExhibit(location);
      }

      return '';
   }

   static applyRegionColorsToElement(element, regionSlug = '') {
      const slug = ValueNormalizer.asTrimmedString(regionSlug);

      if (!element || !slug) {
         return false;
      }

      element.classList.add('itinerary-day-scheduled-pill--region-colored');
      element.classList.add(`itinerary-day-scheduled-pill--region-${slug}`);
      element.setAttribute('data-region-slug', slug);

      return true;
   }
}
