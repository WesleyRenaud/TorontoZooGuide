import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from './rows.js';
import { APP_STRINGS } from '../../strings.js';

export const ITINERARY_PANEL_SECTION_KEYS = {
   animals: 'animals',
   attractions: 'attractions',
   guardiansTalks: 'guardiansTalks',
   wildEncounters: 'wildEncounters',
};

export function buildSectionConfigs(
   {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
   } = {},
   {
      keys = Object.values(ITINERARY_PANEL_SECTION_KEYS),
      onUnscheduleItem = null,
   } = {}
) {
   const unscheduleRowOptions = { onUnscheduleItem };
   const sectionConfigs = [
      {
         key: ITINERARY_PANEL_SECTION_KEYS.animals,
         title: APP_STRINGS.site.nav.animals,
         count: animals.length,
         children: buildAnimalRows(animals, unscheduleRowOptions),
         stepKey: ITINERARY_PANEL_SECTION_KEYS.animals,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.attractions,
         title: APP_STRINGS.map.filter.attractions,
         count: attractions.length,
         children: buildAttractionRows(attractions, unscheduleRowOptions),
         stepKey: ITINERARY_PANEL_SECTION_KEYS.attractions,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         title: APP_STRINGS.site.nav.meetTheGuardians,
         count: guardiansTalks.length,
         children: buildGuardiansRows(guardiansTalks),
         stepKey: ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
         title: APP_STRINGS.site.nav.wildEncounters,
         count: wildEncounters.length,
         children: buildWildRows(wildEncounters),
         stepKey: ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
      },
   ];

   return sectionConfigs.filter((sectionConfig) => (
      keys.includes(sectionConfig.key)
   ));
}
