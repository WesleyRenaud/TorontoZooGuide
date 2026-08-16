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

export const SCHEDULED_DAY_PLANNER_SECTION_KEYS = [
   ITINERARY_PANEL_SECTION_KEYS.animals,
   ITINERARY_PANEL_SECTION_KEYS.attractions,
   ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
   ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
];

export const UNSCHEDULED_DAY_PLANNER_SECTION_KEYS = [
   ITINERARY_PANEL_SECTION_KEYS.animals,
   ITINERARY_PANEL_SECTION_KEYS.attractions,
];

export const SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS = [
   ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
   ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
];

export function buildSectionConfigs(
   {
      animals = [],
      attractions = [],
      guardiansTalks = [],
      wildEncounters = [],
      transportations = [],
   } = {},
   {
      keys = Object.values(ITINERARY_PANEL_SECTION_KEYS),
      onUnscheduleItem = null,
      onScheduleItem = null,
      onRemoveItem = null,
   } = {}
) {
   const rowActionOptions = { onUnscheduleItem, onScheduleItem, onRemoveItem };
   const animalRows = buildAnimalRows(animals, rowActionOptions);
   const attractionRows = buildAttractionRows([
      ...attractions,
      ...transportations.filter((transportation) => (
         transportation?.added_as_attraction === true
      )),
   ], rowActionOptions);
   const guardiansRows = buildGuardiansRows(guardiansTalks, { onRemoveItem });
   const wildRows = buildWildRows(wildEncounters, { onRemoveItem });
   const sectionConfigs = [
      {
         key: ITINERARY_PANEL_SECTION_KEYS.animals,
         title: APP_STRINGS.site.nav.animals,
         count: animalRows.length,
         children: animalRows,
         stepKey: ITINERARY_PANEL_SECTION_KEYS.animals,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.attractions,
         title: APP_STRINGS.map.filter.attractions,
         count: attractionRows.length,
         children: attractionRows,
         stepKey: ITINERARY_PANEL_SECTION_KEYS.attractions,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         title: APP_STRINGS.site.nav.meetTheGuardians,
         count: guardiansRows.length,
         children: guardiansRows,
         stepKey: ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
      },
      {
         key: ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
         title: APP_STRINGS.site.nav.wildEncounters,
         count: wildRows.length,
         children: wildRows,
         stepKey: ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
      },
   ];

   return sectionConfigs.filter((sectionConfig) => (
      keys.includes(sectionConfig.key)
   ));
}
