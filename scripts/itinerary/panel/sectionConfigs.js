import { Rows } from './rows.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationSequenceItems } from '../selectors/transportationSelector/transportationSequenceItems.js';
import { APP_STRINGS } from '../../strings.js';

export class SectionConfigs {
   static ITINERARY_PANEL_SECTION_KEYS = {
      animals: 'animals',
      attractions: 'attractions',
      transportations: 'transportations',
      guardiansTalks: 'guardiansTalks',
      wildEncounters: 'wildEncounters',
   };

   static SCHEDULED_DAY_PLANNER_SECTION_KEYS = [
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
   ];

   static UNSCHEDULED_DAY_PLANNER_SECTION_KEYS = [
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
   ];

   static SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS = [
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
      SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
   ];

   static buildSectionConfigs(
      {
         animals = [],
         attractions = [],
         guardiansTalks = [],
         wildEncounters = [],
         transportations = [],
      } = {},
      {
         keys = Object.values(SectionConfigs.ITINERARY_PANEL_SECTION_KEYS),
         onUnscheduleItem = null,
         onScheduleItem = null,
         onRemoveItem = null,
         splitTransportationSequences = false,
      } = {}
   ) {
      const rowActionOptions = { onUnscheduleItem, onScheduleItem, onRemoveItem };
      const listTransportations = TransportationSequenceItems.expandTransportationListItems(
         transportations,
         { splitSequences: splitTransportationSequences }
      );
      const animalRows = Rows.buildAnimalRows(animals, rowActionOptions);
      const attractionRows = [
         ...Rows.buildAttractionRows(attractions, rowActionOptions),
         ...Rows.buildTransportationRows(
            listTransportations.filter(
               TransportationSelectorModel.isTransportationAddedAsAttraction
            ),
            rowActionOptions
         ),
      ];
      const transportationRows = Rows.buildTransportationRows(
         listTransportations.filter((item) => (
            !TransportationSelectorModel.isTransportationAddedAsAttraction(item)
         )),
         rowActionOptions
      );
      const guardiansRows = Rows.buildGuardiansRows(guardiansTalks, { onRemoveItem });
      const wildRows = Rows.buildWildRows(wildEncounters, { onRemoveItem });
      const sectionConfigs = [
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
            title: APP_STRINGS.site.nav.animals,
            count: animalRows.length,
            children: animalRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
            title: APP_STRINGS.map.filter.attractions,
            count: attractionRows.length,
            children: attractionRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
            title: APP_STRINGS.entityLabels.transportation,
            count: transportationRows.length,
            children: transportationRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
            title: APP_STRINGS.site.nav.meetTheGuardians,
            count: guardiansRows.length,
            children: guardiansRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
            title: APP_STRINGS.site.nav.wildEncounters,
            count: wildRows.length,
            children: wildRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
         },
      ];

      return sectionConfigs.filter((sectionConfig) => (
         keys.includes(sectionConfig.key)
      ));
   }
}
