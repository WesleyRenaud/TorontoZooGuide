import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { showRemovedItemsPopup } from '../../scripts/itinerary/panel/components/removedItemsPopup.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../../scripts/itinerary/panel/rows.js';
import { buildSectionConfigs } from '../../scripts/itinerary/panel/sectionConfigs.js';
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
} from './helpers/panelRowsTestSetup.mjs';

test.describe('itinerary panel row builders', () => {
   installPanelRowsTestHooks();

   test('buildAnimalRows adds unschedule action when handler is provided', () => {
      const unscheduleCalls = [];
      const [row] = buildAnimalRows([
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
   
   test('unscheduled list rows show schedule and remove buttons for animals and attractions only', () => {
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
   
   test('buildAnimalRows adds remove action when handler is provided', () => {
      const removeCalls = [];
      const [row] = buildAnimalRows([
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
   
   test('buildAnimalRows adds schedule action when handler is provided', () => {
      const scheduleCalls = [];
      const [row] = buildAnimalRows([
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
   test('buildAnimalRows keeps separate viewing spots for the same species', () => {
      const rows = buildAnimalRows([
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

   test('buildAnimalRows deduplicates animal exhibit pairs and renders visibility alerts', () => {
      const rows = buildAnimalRows([
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
   
   test('animal section count matches deduplicated rendered rows', () => {
      const [animalSection] = buildSectionConfigs({
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

   test('attraction section includes transportation added as an attraction', () => {
      const [attractionSection] = buildSectionConfigs({
         attractions: [{ name: 'Conservation Carousel' }],
         transportations: [
            { name: 'Zoomobile', added_as_attraction: true },
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
   });
   
   test('removed items popup renders arrival time adjustments', () => {
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
   
   test('removed items popup renders departure time adjustments', () => {
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
   
   test('removed items popup renders unscheduled items', () => {
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
   
   test('animal rows omit scheduled start times', () => {
      const [animalRow] = buildAnimalRows([
         {
            species: 'African Lion',
            exhibit: 'Africa Savanna',
            start_time: '14:28',
            end_time: '14:36',
         },
      ]);
      const [attractionRow] = buildAttractionRows([
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
   
   test('buildAttractionRows renders seeded attraction metadata and removal reason', () => {
      const [row] = buildAttractionRows([
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
   
   test('buildGuardiansRows and buildWildRows render schedule metadata', () => {
      const [talkRow] = buildGuardiansRows([
         {
            name: 'Amur Tiger',
            location: 'Eurasia Wilds',
            start_time: '13:30',
            end_time: '14:00',
         },
      ]);
      const [wildRow] = buildWildRows([
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
   
   test('buildWildRows links encounter title when url is present', () => {
      const [wildRow] = buildWildRows([
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
   
   test('scheduled item row builders sort rows by start time', () => {
      const animalRows = buildAnimalRows([
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
      const attractionRows = buildAttractionRows([
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
      const talkRows = buildGuardiansRows([
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
      const wildRows = buildWildRows([
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
   
   test('buildAnimalRows omits schedule actions for already-scheduled animals', () => {
      const scheduleCalls = [];
      const [row] = buildAnimalRows([
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
   
   test('buildAnimalRows omits unschedule actions for unscheduled animals', () => {
      const [row] = buildAnimalRows([
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
   
   test('buildAttractionRows omits row actions when the attraction id is blank', () => {
      const [row] = buildAttractionRows([
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
   
   test('buildGuardiansRows omits remove action when the talk name is blank', () => {
      const removeCalls = [];
      const [row] = buildGuardiansRows([
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

   test('buildGuardiansRows links the talk name only when a linked animal is present', () => {
      const [linkedRow, plainRow] = buildGuardiansRows([
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
   
   test('buildAnimalRows omits image src when asset path segments are invalid', () => {
      const [row] = buildAnimalRows([
         {
            species: '!!!',
            exhibit: 'Africa Savanna',
         },
      ]);
   
      assert.equal(imageSrcFor(row), '');
   });
   
   test('buildAttractionRows links attraction title when infoLink is present', () => {
      const opened = [];

      globalThis.window.open = (url) => {
         opened.push(url);
      };

      const [row] = buildAttractionRows([
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
