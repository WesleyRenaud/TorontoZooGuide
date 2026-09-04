import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../../../scripts/itinerary/panel/components/dayPlanner.js';
import { showRemovedItemsPopup } from '../../../../scripts/itinerary/panel/components/removedItemsPopup.js';
import { Rows } from '../../../../scripts/itinerary/panel/rows.js';
import { SectionConfigs } from '../../../../scripts/itinerary/panel/sectionConfigs.js';
import {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   imageSrcFor,
   installPanelRowsTestHooks,
   textFor,
   timelinePillTexts,
   timelineScheduledPillTexts,
} from '../../helpers/panelRowsTestSetup.mjs';

test.describe('Test_Rows', () => {
   installPanelRowsTestHooks();

   test('Test_BuildAnimalRows_TestUnscheduleHandler_ExpectAction', () => {
      const unscheduleCalls = [];
      const [row] = Rows.buildAnimalRows([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            start_time: '1:00 PM',
            end_time: '1:30 PM',
         },
      ], {
         onUnscheduleItem: (request) => {
            unscheduleCalls.push(request);
         },
      });
      const button = row.querySelector('.itin-panel-item-action-btn');
   
      assert.equal(button?.textContent, 'Unschedule');
      button?.click();
      assert.deepEqual(unscheduleCalls, [{
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }]);
   });
   
   test('Test_UnscheduledListRows_TestAnimalsAndAttractions_ExpectScheduleAndRemove', () => {
      const scheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
            wildEncounters: [],
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:00 PM',
                  end_time: '1:30 PM',
               },
               {
                  species: 'Giant Panda',
                  exhibit: 'Eurasia Wilds',
               },
            ],
            attractions: [
               {
                  name: 'Conservation Carousel',
                  subtitle: 'Carousels are timeless and fun for all ages!',
               },
               {
                  name: 'Zoomobile',
                  subtitle: 'Ride the rails',
                  start_time: '2:30 PM',
                  end_time: '3:00 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onScheduleItineraryItem: (pick) => {
                  scheduleCalls.push(pick);
               },
               onUnscheduleItineraryItem: () => {},
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const dayItemsSections = [...planner.querySelectorAll('.itinerary-day-items-sections')];
      const scheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const unscheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Unscheduled Items')
      ));
      const scheduledButtons = scheduledList?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
      const unscheduledButtons = unscheduledList?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
      const pandaRow = [...(unscheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Giant Panda')
      ));
      const pandaButtons = pandaRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
   
      assert.equal(scheduledButtons.length, 5);
      assert.equal(
         unscheduledList?.querySelectorAll('.itin-panel-item').length,
         2
      );
      assert.equal(unscheduledButtons.length, 4);
      assert.equal(
         unscheduledButtons.every((button) => (
            button.textContent === 'Schedule' || button.textContent === 'Remove'
         )),
         true
      );
      assert.deepEqual(
         [...pandaButtons].map((button) => button.textContent),
         ['Schedule', 'Remove']
      );
   
      [...unscheduledButtons]
         .filter((button) => button.textContent === 'Schedule')
         .forEach((button) => {
            button.click();
         });
   
      assert.equal(scheduleCalls.length, 2);
      assert.equal(scheduleCalls[0].itemType, 'animals');
      assert.equal(scheduleCalls[0].row.species, 'Giant Panda');
      assert.equal(scheduleCalls[0].row.scheduleItemKind, 'animals');
      assert.equal(scheduleCalls[1].itemType, 'attractions');
      assert.equal(scheduleCalls[1].row.name, 'Conservation Carousel');
      assert.equal(scheduleCalls[1].row.scheduleItemKind, 'attractions');
      assert.equal(removeCalls.length, 0);
   });
   
   test('Test_BuildAnimalRows_TestRemoveHandler_ExpectAction', () => {
      const removeCalls = [];
      const [row] = Rows.buildAnimalRows([
         {
            species: 'Giant Panda',
            exhibit: 'Eurasia Wilds',
         },
      ], {
         onRemoveItem: (request) => {
            removeCalls.push(request);
         },
      });
      const button = row.querySelector('.itin-panel-item-action-btn');
   
      assert.equal(button?.textContent, 'Remove');
      button?.click();
      assert.deepEqual(removeCalls, [{
         itemType: 'animals',
         key: 'Giant Panda||Eurasia Wilds',
      }]);
   });
   
   test('Test_BuildAnimalRows_TestScheduleHandler_ExpectAction', () => {
      const scheduleCalls = [];
      const [row] = Rows.buildAnimalRows([
         {
            species: 'Giant Panda',
            exhibit: 'Eurasia Wilds',
         },
      ], {
         onScheduleItem: (pick) => {
            scheduleCalls.push(pick);
         },
      });
      const button = row.querySelector('.itin-panel-item-action-btn');
   
      assert.equal(button?.textContent, 'Schedule');
      button?.click();
      assert.equal(scheduleCalls.length, 1);
      assert.equal(scheduleCalls[0].itemType, 'animals');
      assert.equal(scheduleCalls[0].row.species, 'Giant Panda');
      assert.equal(scheduleCalls[0].row.scheduleItemKind, 'animals');
   });
   test('Test_BuildAnimalRows_TestSameSpecies_ExpectSeparateViewingSpots', () => {
      const rows = Rows.buildAnimalRows([
         {
            species: 'Western Lowland Gorilla',
            exhibit: 'African Rainforest Pavilion',
            enclosure_name: 'Indoor',
            enclosure_type: 'Indoor',
         },
         {
            species: 'Western Lowland Gorilla',
            exhibit: 'African Rainforest Pavilion',
            enclosure_name: 'Outdoor',
            enclosure_type: 'Outdoor',
         },
      ]);

      assert.equal(rows.length, 2);
      assert.match(textFor(rows[0], '.itin-panel-name'), /Indoor/);
      assert.match(textFor(rows[1], '.itin-panel-name'), /Outdoor/);
      assert.equal(
         textFor(rows[0], '.itin-panel-meta'),
         'African Rainforest Pavilion'
      );
      assert.equal(
         textFor(rows[1], '.itin-panel-meta'),
         'African Rainforest Pavilion'
      );
   });

   test('Test_BuildAnimalRows_TestDuplicateExhibits_ExpectDedupedWithAlerts', () => {
      const rows = Rows.buildAnimalRows([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            likelihoodBefore: 90,
            likelihoodAfter: 60,
         },
         {
            species: ' african lion ',
            exhibit: 'Africa Savanna',
         },
         {
            species: 'African Lion',
            exhibit: 'Indo-Malaya Outdoor',
         },
      ]);
   
      assert.equal(rows.length, 2);
      assert.equal(
         imageSrcFor(rows[0]),
         'images/details/animals/africa-savanna/african-lion.png'
      );
      assert.equal(textFor(rows[0], '.itin-panel-name'), 'African Lion');
      assert.ok(
         rows[0].querySelector('.itin-panel-name')?.querySelector('.species-link'),
         'animal names should open species detail overlay'
      );
      assert.equal(textFor(rows[0], '.itin-panel-meta'), 'Africa Savanna');
      assert.equal(
         textFor(rows[0], '.itin-panel-alert'),
         'Projected visibility changed from 90% to 60% on your new date.'
      );
      assert.equal(textFor(rows[1], '.itin-panel-name'), 'African Lion');
      assert.equal(textFor(rows[1], '.itin-panel-meta'), 'Indo-Malaya Outdoor');
   });
   
   test('Test_AnimalSection_TestDeduplicatedRows_ExpectMatchingCount', () => {
      const [animalSection] = SectionConfigs.buildSectionConfigs({
         animals: [
            {
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            },
            {
               species: ' african lion ',
               exhibit: 'Africa Savanna',
            },
            {
               species: 'African Lion',
               exhibit: 'Indo-Malaya Outdoor',
            },
         ],
      }, {
         keys: ['animals'],
      });
   
      assert.equal(animalSection.count, 2);
      assert.equal(animalSection.children.length, 2);
   });

   test('Test_AttractionSection_TestAddedAsAttractionTransportation_ExpectIncluded', () => {
      const [attractionSection] = SectionConfigs.buildSectionConfigs({
         attractions: [{ name: 'Conservation Carousel' }],
         transportations: [
            {
               name: 'Zoomobile',
               added_as_attraction: true,
               legs: [
                  { from_station: 'Main Station', to_station: 'Canadian Domain' },
                  { from_station: 'Canadian Domain', to_station: 'Wildlife Health' },
               ],
            },
            { name: 'Zoo Shuttle', added_as_attraction: false },
         ],
      }, {
         keys: ['attractions'],
      });

      assert.equal(attractionSection.count, 2);
      assert.deepEqual(
         attractionSection.children.map((row) => textFor(row, '.itin-panel-name')),
         ['Conservation Carousel', 'Zoomobile']
      );
      assert.match(
         allTextFor(attractionSection.children[1]),
         /Main Station → Wildlife Health/
      );
   });

   test('Test_TransportationSection_TestPureTransportations_ExpectNoScheduleActions', () => {
      const scheduleCalls = [];
      const removeCalls = [];
      const [transportationSection] = SectionConfigs.buildSectionConfigs({
         transportations: [
            {
               name: 'Zoomobile',
               added_as_attraction: false,
               main_station: 'Main Zoomobile Station',
            },
            {
               name: 'Zoo Shuttle',
               added_as_attraction: true,
            },
         ],
      }, {
         keys: ['transportations'],
         onScheduleItem: (pick) => {
            scheduleCalls.push(pick);
         },
         onRemoveItem: (request) => {
            removeCalls.push(request);
         },
      });

      assert.equal(transportationSection.count, 1);
      assert.deepEqual(
         transportationSection.children.map((row) => textFor(row, '.itin-panel-name')),
         ['Zoomobile']
      );
      assert.doesNotMatch(
         allTextFor(transportationSection.children[0]),
         /round trip|Main Zoomobile Station/
      );

      const buttons = [
         ...(transportationSection.children[0]?.querySelectorAll('.itin-panel-item-action-btn') ?? []),
      ];
      assert.deepEqual(
         buttons.map((button) => button.textContent),
         ['Remove']
      );

      buttons[0]?.click();
      assert.equal(scheduleCalls.length, 0);
      assert.deepEqual(removeCalls, [{
         itemType: 'transportations',
         key: 'Zoomobile||0',
      }]);
   });

   test('Test_AttractionSection_TestUnscheduledRoundTrip_ExpectMainStationLine', () => {
      const [attractionSection] = SectionConfigs.buildSectionConfigs({
         attractions: [],
         transportations: [
            {
               name: 'Zoomobile',
               added_as_attraction: true,
               main_station: 'Main Zoomobile Station',
               legs: [],
            },
         ],
      }, {
         keys: ['attractions'],
      });

      assert.match(
         allTextFor(attractionSection.children[0]),
         /Main Zoomobile Station \(round trip\)/
      );
   });

   test('Test_TransportationStationLine_TestRoundTrip_ExpectMarked', () => {
      const [attractionSection] = SectionConfigs.buildSectionConfigs({
         attractions: [],
         transportations: [
            {
               name: 'Zoomobile',
               added_as_attraction: true,
               legs: [
                  {
                     from_station: 'Main Zoomobile Station',
                     to_station: 'Canadian Domain',
                  },
                  {
                     from_station: 'Canadian Domain',
                     to_station: 'Main Zoomobile Station',
                  },
               ],
            },
         ],
      }, {
         keys: ['attractions'],
      });

      assert.match(
         allTextFor(attractionSection.children[0]),
         /Main Zoomobile Station \(round trip\)/
      );
      assert.doesNotMatch(
         allTextFor(attractionSection.children[0]),
         /Main Zoomobile Station → Main Zoomobile Station/
      );
   });
   
   test('Test_RemovedItemsPopup_TestArrivalAdjustments_ExpectRendered', () => {
      const mount = document.createElement('div');
   
      showRemovedItemsPopup({
         mountEl: mount,
         adjustments: [
            {
               type: 'arrivalTimeAdjusted',
               field: 'arrivalTime',
               previousValue: '09:00',
               value: '09:30',
               reason: 'arrivalOutsideAdmissionHours',
            },
         ],
      });
   
      const text = allTextFor(mount);
   
      assert.match(text, /Times Updated/);
      assert.match(text, /Arrival changed from 9:00 AM to 9:30 AM/);
      assert.match(text, /different admission hours/);
      assert.ok(
         mount.querySelector('.itin-panel-item'),
         'arrival adjustments should use the same item row styling as animals'
      );
      assert.equal(
         mount.querySelector('.itin-panel-item .itin-panel-thumb'),
         null,
         'arrival adjustments should not render an image placeholder'
      );
   });
   
   test('Test_RemovedItemsPopup_TestDepartureAdjustments_ExpectRendered', () => {
      const mount = document.createElement('div');
   
      showRemovedItemsPopup({
         mountEl: mount,
         adjustments: [
            {
               type: 'departureTimeAdjusted',
               field: 'departureTime',
               previousValue: '18:30',
               value: '18:00',
               reason: 'departureOutsideOperatingHours',
            },
         ],
      });
   
      const text = allTextFor(mount);
   
      assert.match(text, /Times Updated/);
      assert.match(text, /Departure changed from 6:30 PM to 6:00 PM/);
      assert.match(text, /different operating hours/);
      assert.ok(
         mount.querySelector('.itin-panel-item'),
         'departure adjustments should use the same item row styling as animals'
      );
      assert.equal(
         mount.querySelector('.itin-panel-item .itin-panel-thumb'),
         null,
         'departure adjustments should not render an image placeholder'
      );
   });
   
   test('Test_RemovedItemsPopup_TestUnscheduledItems_ExpectRendered', () => {
      const mount = document.createElement('div');
   
      showRemovedItemsPopup({
         mountEl: mount,
         unscheduled: {
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '09:00',
                  end_time: '09:08',
               },
            ],
            attractions: [
               {
                  name: 'Conservation Carousel',
                  start_time: '09:08',
                  end_time: '09:16',
               },
            ],
         },
      });
   
      const text = allTextFor(mount);
   
      assert.match(text, /Unscheduled Items/);
      assert.match(text, /still on your itinerary/);
      assert.match(text, /African Lion/);
      assert.match(text, /Conservation Carousel/);
   });
   
   test('Test_AnimalRows_TestScheduledStartTimes_ExpectOmitted', () => {
      const [animalRow] = Rows.buildAnimalRows([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            start_time: '14:28',
            end_time: '14:36',
         },
      ]);
      const [attractionRow] = Rows.buildAttractionRows([
         {
            name: 'Zoomobile',
            start_time: '2:23 PM',
            end_time: '2:35 PM',
         },
      ]);
   
      assert.equal(animalRow.querySelectorAll('.itin-panel-meta').length, 1);
      assert.equal(
         animalRow.querySelectorAll('.itin-panel-meta')[0].textContent.includes('Time:'),
         false
      );
      assert.equal(
         attractionRow.querySelectorAll('.itin-panel-meta')[0].textContent,
         'Time: ~2:25 PM'
      );
   });
   
   test('Test_BuildAttractionRows_TestSeededMetadata_ExpectRemovalReason', () => {
      const [row] = Rows.buildAttractionRows([
         {
            name: 'Conservation Carousel',
            subtitle: 'Carousels are timeless and fun for all ages!',
            region: 'Front Courtyard',
            price: 'Extra charge',
            removalReason: 'The Conservation Carousel is temporarily closed.',
         },
      ]);
   
      assert.equal(textFor(row, '.itin-panel-name'), 'Conservation Carousel');
      assert.equal(
         row.querySelector('.itin-panel-name')?.querySelector('.species-link'),
         null
      );
      assert.equal(
         imageSrcFor(row),
         'images/details/attractions/conservation-carousel.png'
      );
      assert.equal(textFor(row, '.itin-panel-meta'), 'Carousels are timeless and fun for all ages!');
      assert.match(allTextFor(row), /Location: Front Courtyard/);
      assert.equal(
         textFor(row, '.itin-panel-alert'),
         'Not available on this date: The Conservation Carousel is temporarily closed.'
      );
   });
   
   test('Test_BuildGuardiansAndWildRows_TestScheduleMetadata_ExpectRendered', () => {
      const [talkRow] = Rows.buildGuardiansRows([
         {
            name: 'Amur Tiger',
            location: 'Eurasia Wilds',
            start_time: '13:30',
            end_time: '14:00',
         },
      ]);
      const [wildRow] = Rows.buildWildRows([
         {
            name: 'African Rainforest',
            meeting_spot: 'Wild Encounter - Africa Meeting Spot',
            start_time: '14:00',
            end_time: '14:45',
         },
      ]);
   
      assert.equal(textFor(talkRow, '.itin-panel-name'), 'Amur Tiger Meet The Guardians Talk');
      assert.equal(
         talkRow.querySelector('.itin-panel-name')?.querySelector('.species-link'),
         null
      );
      assert.equal(
         imageSrcFor(talkRow),
         'images/details/guardians-talks/amur-tiger.png'
      );
      assert.equal(textFor(talkRow, '.itin-panel-meta'), 'Location: Eurasia Wilds');
      assert.equal(
         talkRow.querySelectorAll('.itin-panel-meta')[1].textContent,
         'Time: 1:30 PM - 2:00 PM'
      );
      assert.equal(textFor(wildRow, '.itin-panel-name'), 'African Rainforest Wild Encounter');
      assert.equal(
         wildRow.querySelector('.itin-panel-name')?.querySelector('.species-link'),
         null
      );
      assert.equal(
         imageSrcFor(wildRow),
         'images/details/wild-encounters/african-rainforest.png'
      );
      assert.equal(
         textFor(wildRow, '.itin-panel-meta'),
         'Meeting Spot: Wild Encounter - Africa Meeting Spot'
      );
      assert.equal(
         wildRow.querySelectorAll('.itin-panel-meta')[1].textContent,
         'Time: 2:00 PM - 2:45 PM'
      );
   });
   
   test('Test_BuildWildRows_TestUrlPresent_ExpectLinkedTitle', () => {
      const [wildRow] = Rows.buildWildRows([
         {
            name: 'African Rainforest',
            meeting_spot: 'Wild Encounter - Africa Meeting Spot',
            link: 'https://www.torontozoo.com/wildencounters/african-rainforest',
         },
      ]);

      assert.ok(
         wildRow.querySelector('.itin-panel-name')?.querySelector('.species-link')
      );
      assert.equal(
         wildRow.querySelector('.itin-panel-name')?.querySelector('.species-link')
            ?.textContent,
         'African Rainforest'
      );
      assert.equal(
         textFor(wildRow, '.itin-panel-name'),
         'African Rainforest Wild Encounter'
      );
      assert.equal(wildRow.querySelector('.itin-panel-link'), null);
   });
   
   test('Test_ScheduledItemRowBuilders_TestStartTime_ExpectSorted', () => {
      const animalRows = Rows.buildAnimalRows([
         {
            species: 'Late Animal',
            exhibit: 'Eurasia Wilds',
            start_time: '1:30 PM',
            end_time: '2:00 PM',
         },
         {
            species: 'Early Animal',
            exhibit: 'Africa Savanna',
            start_time: '10:00 AM',
            end_time: '10:30 AM',
         },
      ]);
      const attractionRows = Rows.buildAttractionRows([
         {
            name: 'Afternoon Attraction',
            start_time: '14:00',
            end_time: '14:30',
         },
         {
            name: 'Morning Attraction',
            start_time: '11:00',
            end_time: '11:30',
         },
      ]);
      const talkRows = Rows.buildGuardiansRows([
         {
            name: 'Late Talk',
            location: 'Eurasia Wilds',
            start_time: '1:30 PM',
         },
         {
            name: 'Early Talk',
            location: 'Africa Savanna',
            start_time: '10:00 AM',
         },
      ]);
      const wildRows = Rows.buildWildRows([
         {
            name: 'Afternoon Encounter',
            meeting_spot: 'Wild Encounter - Africa Meeting Spot',
            start_time: '14:00',
         },
         {
            name: 'Morning Encounter',
            meeting_spot: 'Wild Encounter - Australasia Meeting Spot',
            start_time: '11:00',
         },
      ]);
   
      assert.deepEqual(
         animalRows.map((row) => textFor(row, '.itin-panel-name')),
         ['Early Animal', 'Late Animal']
      );
      assert.deepEqual(
         attractionRows.map((row) => textFor(row, '.itin-panel-name')),
         ['Morning Attraction', 'Afternoon Attraction']
      );
      assert.deepEqual(
         talkRows.map((row) => textFor(row, '.itin-panel-name')),
         ['Early Talk Meet The Guardians Talk', 'Late Talk Meet The Guardians Talk']
      );
      assert.deepEqual(
         wildRows.map((row) => textFor(row, '.itin-panel-name')),
         ['Morning Encounter Wild Encounter', 'Afternoon Encounter Wild Encounter']
      );
   });
   
   test('Test_BuildAnimalRows_TestAlreadyScheduled_ExpectOmitSchedule', () => {
      const scheduleCalls = [];
      const [row] = Rows.buildAnimalRows([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            start_time: '1:00 PM',
            end_time: '1:30 PM',
         },
      ], {
         onScheduleItem: (pick) => {
            scheduleCalls.push(pick);
         },
         onUnscheduleItem: () => {},
      });
      const buttonLabels = [...row.querySelectorAll('.itin-panel-item-action-btn')]
         .map((button) => button.textContent);
   
      assert.equal(buttonLabels.includes('Schedule'), false);
      assert.equal(scheduleCalls.length, 0);
   });
   
   test('Test_BuildAnimalRows_TestUnscheduled_ExpectOmitUnschedule', () => {
      const [row] = Rows.buildAnimalRows([
         {
            species: 'Giant Panda',
            exhibit: 'Eurasia Wilds',
         },
      ], {
         onUnscheduleItem: () => {},
      });
      const buttonLabels = [...row.querySelectorAll('.itin-panel-item-action-btn')]
         .map((button) => button.textContent);
   
      assert.equal(buttonLabels.includes('Unschedule'), false);
   });
   
   test('Test_BuildAttractionRows_TestBlankId_ExpectOmitActions', () => {
      const [row] = Rows.buildAttractionRows([
         {
            name: '   ',
            start_time: '1:00 PM',
            end_time: '1:30 PM',
         },
      ], {
         onUnscheduleItem: () => {},
         onRemoveItem: () => {},
      });
   
      assert.equal(row.querySelectorAll('.itin-panel-item-action-btn').length, 0);
   });
   
   test('Test_BuildGuardiansRows_TestBlankName_ExpectOmitRemove', () => {
      const removeCalls = [];
      const [row] = Rows.buildGuardiansRows([
         {
            name: '   ',
            location: 'Eurasia Wilds',
         },
      ], {
         onRemoveItem: (request) => {
            removeCalls.push(request);
         },
      });

      assert.equal(row.querySelectorAll('.itin-panel-item-action-btn').length, 0);
      assert.equal(removeCalls.length, 0);
   });

   test('Test_BuildGuardiansRows_TestLinkedAnimal_ExpectConditionalLink', () => {
      const [linkedRow, plainRow] = Rows.buildGuardiansRows([
         {
            name: 'African Lion',
            location: 'Africa Savanna',
            linked_animals: [
               { species: 'African Lion', exhibit: 'Africa Savanna' },
            ],
         },
         {
            name: 'Guardians of Plants',
            location: 'Greenhouse',
            linked_animals: [],
         },
      ]);

      assert.ok(
         linkedRow.querySelector('.itin-panel-name')?.querySelector('.species-link'),
         'talks with linked animals should open the animal overlay'
      );
      assert.equal(
         linkedRow.querySelector('.itin-panel-name')?.querySelector('.species-link')
            ?.textContent,
         'African Lion'
      );
      assert.equal(
         textFor(linkedRow, '.itin-panel-name'),
         'African Lion Meet The Guardians Talk'
      );
      assert.equal(
         plainRow.querySelector('.itin-panel-name')?.querySelector('.species-link'),
         null
      );
      assert.equal(
         textFor(plainRow, '.itin-panel-name'),
         'Guardians of Plants Meet The Guardians Talk'
      );
   });
   
   test('Test_BuildAnimalRows_TestInvalidAssetPath_ExpectOmitImage', () => {
      const [row] = Rows.buildAnimalRows([
         {
            species: '!!!',
            exhibit: 'Africa Savanna',
         },
      ]);
   
      assert.equal(imageSrcFor(row), '');
   });
   
   test('Test_BuildAttractionRows_TestInfoLink_ExpectLinkedTitle', () => {
      const opened = [];

      globalThis.window.open = (url) => {
         opened.push(url);
      };

      const [row] = Rows.buildAttractionRows([
         {
            name: 'Conservation Carousel',
            info_link: 'https://www.torontozoo.com/tickets/carousel',
         },
      ]);
      const titleLink = row.querySelector('.itin-panel-name')?.querySelector('.species-link');

      assert.ok(titleLink);
      assert.equal(titleLink.textContent, 'Conservation Carousel');
      assert.equal(row.querySelector('.itin-panel-link'), null);

      titleLink.click();
      assert.deepEqual(opened, ['https://www.torontozoo.com/tickets/carousel']);
   });
});
