import assert from 'node:assert/strict';
import test from 'node:test';

import { SectionConfigs } from '../../../../scripts/itinerary/panel/sectionConfigs.js';
import { ItineraryPanelRowsBuilder } from '../../../../scripts/itinerary/panel/itineraryPanelRowsBuilder.js';
import { TransportationSequenceItems } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSequenceItems.js';
import { TransportationSelectorModel } from '../../../../scripts/itinerary/selectors/transportationSelector/transportationSelectorModel.js';
import { Strings } from '../../../../scripts/strings.js';

test('Test_BuildSectionConfigs_TestFilteredKeys_ExpectSections', () => {
   const originalExpand = TransportationSequenceItems.expandTransportationListItems;
   const originalAnimals = ItineraryPanelRowsBuilder.buildAnimalRows;
   const originalAttractions = ItineraryPanelRowsBuilder.buildAttractionRows;
   const originalTransport = ItineraryPanelRowsBuilder.buildTransportationRows;
   const originalGuardians = ItineraryPanelRowsBuilder.buildGuardiansRows;
   const originalWild = ItineraryPanelRowsBuilder.buildWildRows;
   const originalIsAttraction = TransportationSelectorModel.isTransportationAddedAsAttraction;

   TransportationSequenceItems.expandTransportationListItems = (items) => items;
   ItineraryPanelRowsBuilder.buildAnimalRows = () => [{ id: 'animal' }];
   ItineraryPanelRowsBuilder.buildAttractionRows = () => [{ id: 'attraction' }];
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
            transportations: [
               { id: 'ride-attr', asAttraction: true },
               { id: 'ride', asAttraction: false },
            ],
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
      assert.equal(sections[0].title, Strings.site.nav.animals);
      assert.equal(sections[0].count, 1);
      assert.equal(sections[1].key, 'attractions');
      assert.ok(sections[1].children.some((row) => row.id === 'attraction'));
      assert.ok(sections[1].children.some((row) => row.id === 'ride-attr'));
      assert.deepEqual(sections[2].children, [{ id: 'ride' }]);
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

test('Test_SectionKeyConstants_TestSets_ExpectMembership', () => {
   assert.deepEqual(
      SectionConfigs.SCHEDULED_DAY_PLANNER_SECTION_KEYS,
      [
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.animals,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.attractions,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.transportations,
      ]
   );
   assert.ok(
      !SectionConfigs.UNSCHEDULED_DAY_PLANNER_SECTION_KEYS.includes(
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks
      )
   );
   assert.deepEqual(
      SectionConfigs.SCHEDULED_DAY_PLANNER_EDIT_SECTION_KEYS,
      [
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.guardiansTalks,
         SectionConfigs.ITINERARY_PANEL_SECTION_KEYS.wildEncounters,
      ]
   );
});
