import assert from 'node:assert/strict';
import test from 'node:test';

import { ItineraryPanelRowsBuilder } from '../../../../scripts/itinerary/panel/itineraryPanelRowsBuilder.js';
import { SectionConfigs } from '../../../../scripts/itinerary/panel/sectionConfigs.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { TransportationSequenceItems } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSequenceItems.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { Strings } from '../../../../scripts/strings.js';


test('Test_BuildSectionConfigs_TestFilteredKeys_ExpectSections', () => {
   const originalExpand = TransportationSequenceItems.expandTransportationListItems;
   const originalAnimals = ItineraryPanelRowsBuilder.buildAnimalRows;
   const originalAttractions = ItineraryPanelRowsBuilder.buildAttractionRows;
   const originalTransport = ItineraryPanelRowsBuilder.buildTransportationRows;
   const originalGuardians = ItineraryPanelRowsBuilder.buildGuardiansRows;
   const originalWild = ItineraryPanelRowsBuilder.buildWildRows;
   const originalIsAttraction = TransportationSelectorModel.isTransportationAddedAsAttraction;
   const animalRow = { id: 'animal' };
   const attractionRow = { id: 'attraction' };
   const attractionRide = { id: 'ride-attr', asAttraction: true };
   const transitRide = { id: 'ride', asAttraction: false };
   TransportationSequenceItems.expandTransportationListItems = (items) => items;
   ItineraryPanelRowsBuilder.buildAnimalRows = () => [animalRow];
   ItineraryPanelRowsBuilder.buildAttractionRows = () => [attractionRow];
   ItineraryPanelRowsBuilder.buildTransportationRows = (items) => items.map((item) => ({ id: item.id }));
   ItineraryPanelRowsBuilder.buildGuardiansRows = () => [{ id: 'talk' }];
   ItineraryPanelRowsBuilder.buildWildRows = () => [{ id: 'wild' }];
   TransportationSelectorModel.isTransportationAddedAsAttraction = (item) => item.asAttraction;

   try {
      const sections = SectionConfigs.buildSectionConfigs(
         {
            animals: [{}],
            attractions: [{}],
            guardiansTalks: [{}],
            wildEncounters: [{}],
            transportations: [attractionRide, transitRide],
         },
         {
            keys: [
               SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
               SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
               SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
            ],
         }
      );

      assert.equal(sections.length, 3);
      assert.equal(sections.at(Position.FIRST).title, Strings.site.nav.animals);
      assert.equal(sections.at(Position.FIRST).count, 1);
      assert.equal(
         sections.at(Position.SECOND).key,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions
      );
      assert.ok(sections.at(Position.SECOND).children.some((row) => row.id === attractionRow.id));
      assert.ok(sections.at(Position.SECOND).children.some((row) => row.id === attractionRide.id));
      assert.deepEqual(sections.at(Position.THIRD).children, [{ id: transitRide.id }]);
   } finally {
      TransportationSequenceItems.expandTransportationListItems = originalExpand;
      ItineraryPanelRowsBuilder.buildAnimalRows = originalAnimals;
      ItineraryPanelRowsBuilder.buildAttractionRows = originalAttractions;
      ItineraryPanelRowsBuilder.buildTransportationRows = originalTransport;
      ItineraryPanelRowsBuilder.buildGuardiansRows = originalGuardians;
      ItineraryPanelRowsBuilder.buildWildRows = originalWild;
      TransportationSelectorModel.isTransportationAddedAsAttraction = originalIsAttraction;
   }
});


test('Test_ScheduledDayPlannerSectionKeys_TestSets_ExpectMembership', () => {
   const scheduledKeys = SectionConfigs.SCHEDULED_DAY_PLANNER_SECTION_KEYS;

   assert.deepEqual(
      scheduledKeys,
      [
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
      ]
   );
});


test('Test_UnscheduledDayPlannerSectionKeys_TestGuardiansTalks_ExpectOmitted', () => {
   const unscheduledKeys = SectionConfigs.UNSCHEDULED_DAY_PLANNER_SECTION_KEYS;

   assert.ok(!unscheduledKeys.includes(SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks));
});


test('Test_ScheduledDayPlannerEditSectionKeys_TestTalksAndWild_ExpectKeys', () => {
   const editKeys = SectionConfigs.SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS;

   assert.deepEqual(
      editKeys,
      [
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
      ]
   );
});
