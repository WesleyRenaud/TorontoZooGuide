import { ItineraryPanelRowsBuilder } from './itineraryPanelRowsBuilder.js';
import { TransportationSelectorModel } from '../selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationSequenceItems } from '../selectors/transportationSelector/transportationSequenceItems.js';
import { ScheduleItemKind } from '../../shared/enums/scheduleItemKind.js';
import { Strings } from '../../strings.js';

export class SectionConfigs {
   static ITINERARY_PANEL_SECTION_KEYS = {
      animals: ScheduleItemKind.ANIMAL.itemType,
      attractions: ScheduleItemKind.ATTRACTION.itemType,
      transportations: ScheduleItemKind.TRANSPORTATION.itemType,
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
      const animalRows = ItineraryPanelRowsBuilder.buildAnimalRows(animals, rowActionOptions);
      const attractionRows = [
         ...ItineraryPanelRowsBuilder.buildAttractionRows(attractions, rowActionOptions),
         ...ItineraryPanelRowsBuilder.buildTransportationRows(
            listTransportations.filter(
               TransportationSelectorModel.isTransportationAddedAsAttraction
            ),
            rowActionOptions
         ),
      ];
      const transportationRows = ItineraryPanelRowsBuilder.buildTransportationRows(
         listTransportations.filter((item) => (
            !TransportationSelectorModel.isTransportationAddedAsAttraction(item)
         )),
         rowActionOptions
      );
      const guardiansRows = ItineraryPanelRowsBuilder.buildGuardiansRows(guardiansTalks, { onRemoveItem });
      const wildRows = ItineraryPanelRowsBuilder.buildWildRows(wildEncounters, { onRemoveItem });
      const sectionConfigs = [
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
            title: Strings.site.nav.animals,
            count: animalRows.length,
            children: animalRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
            title: Strings.map.filter.attractions,
            count: attractionRows.length,
            children: attractionRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
            title: Strings.entityLabels.transportation,
            count: transportationRows.length,
            children: transportationRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
            title: Strings.site.nav.meetTheGuardians,
            count: guardiansRows.length,
            children: guardiansRows,
            stepKey: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         },
         {
            key: SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
            title: Strings.site.nav.wildEncounters,
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
