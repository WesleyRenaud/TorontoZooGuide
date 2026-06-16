import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { buildSectionConfigs } from '../../scripts/itinerary/panel/sectionConfigs.js';
import {
   buildAnimalRows,
   buildAttractionRows,
} from '../../scripts/itinerary/panel/rows.js';
import {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   documentListeners,
   imageSrcFor,
   installPanelRowsTestHooks,
   textFor,
   timelinePillTexts,
   timelineScheduledPillTexts,
} from './helpers/panelRowsTestSetup.mjs';

test.describe('itinerary day planner preview', () => {
   installPanelRowsTestHooks();

   test('day planner starts at early admission when available', () => {
      const planner = makeDayPlannerPreview({
         date: '2026-06-20',
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
         closeTime: '19:00',
      }, EMPTY_ITINERARY);
      const text = allTextFor(planner);
   
      assert.match(text, /9:00 AM/);
      assert.match(text, /Early Admission/);
      assert.match(text, /9:30 AM/);
      assert.match(text, /Zoo Opens/);
   });
   
   test('arrival marker remove menu clears arrival time through handler', () => {
      const arrivalRemovals = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:45',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         },
         {
            onArrivalTimeChange: (value) => {
               arrivalRemovals.push(value);
            },
         }
      );
      const arrivalMarker = boundaryMarkerByLabel(planner, 'Arrival');
      const openPill = [...planner.querySelectorAll('.itinerary-day-time-boundary-label')].find((label) => (
         allTextFor(label).includes('Zoo Opens')
      ));
   
      assert.ok(arrivalMarker?.classList.contains('itinerary-day-boundary-marker--with-menu'));
      assert.equal(arrivalMarker?.attributes?.['data-boundary-marker-kind'], 'arrival');
      assert.equal(arrivalMarker?.attributes?.['aria-label'], 'Arrival');
      assert.ok(openPill);
   
      arrivalMarker?.querySelector('.itinerary-day-open-pill-menu-item')?.click();
      assert.deepEqual(arrivalRemovals, [ '' ]);
   });
   
   test('day planner header clear buttons remove arrival and departure times', async () => {
      const arrivalChanges = [];
      const departureChanges = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:45',
            departureTime: '17:15',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         },
         {
            onArrivalTimeChange: async (value) => {
               arrivalChanges.push(value);
            },
            onDepartureTimeChange: async (value) => {
               departureChanges.push(value);
            },
         }
      );
      const clearButtons = [...planner.querySelectorAll('.itinerary-day-time-clear-btn')];
   
      assert.equal(clearButtons.length, 2);
      assert.equal(clearButtons[0].attributes?.['aria-label'], 'Clear arrival time');
      assert.equal(clearButtons[1].attributes?.['aria-label'], 'Clear departure time');
   
      clearButtons[0].click();
      await Promise.resolve();
      clearButtons[1].click();
      await Promise.resolve();
   
      assert.deepEqual(arrivalChanges, [ '' ]);
      assert.deepEqual(departureChanges, [ '' ]);
   });
   
   test('day planner header disables clear buttons when times are unset', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         },
         {
            onArrivalTimeChange: () => {},
            onDepartureTimeChange: () => {},
         }
      );
      const clearButtons = [...planner.querySelectorAll('.itinerary-day-time-clear-btn')];
   
      assert.equal(clearButtons.length, 2);
      assert.ok(clearButtons.every((button) => button.disabled));
   });
   
   test('day planner departure input rejects invalid picker value on outside click', async () => {
      const departureChanges = [];
      const pickerInstances = [];
   
      window.flatpickr = (input, options = {}) => {
         const instance = {
            input,
            isOpen: true,
            calendarContainer: createNode('div', 'flatpickr-calendar'),
            closeCalled: false,
            clear() {
               input.value = '';
            },
            close() {
               instance.closeCalled = true;
               instance.isOpen = false;
               options.onClose?.([], '', instance);
            },
            setDate(value) {
               input.value = value;
            },
         };
   
         pickerInstances.push(instance);
         options.onReady?.([], input.value, instance);
         options.onOpen?.([], input.value, instance);
   
         return instance;
      };
   
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            departureTime: '18:30',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         },
         {
            onDepartureTimeChange: async (value) => {
               departureChanges.push(value);
            },
         }
      );
      const inputs = [...planner.querySelectorAll('.itinerary-day-time-input')];
      const departureInput = inputs[1];
      const outsideTarget = createNode('button');
   
      departureInput.value = '8:00 PM';
      documentListeners.get('mousedown')?.forEach((handler) => {
         handler({ target: outsideTarget });
      });
      await Promise.resolve();
   
      assert.deepEqual(departureChanges, []);
      assert.equal(pickerInstances[1]?.closeCalled, true);
      assert.equal(departureInput.value, '6:30 PM');
   });
   
   test('scheduled generic event pill renders on the timeline with remove menu', () => {
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            events: [
               {
                  event_type: 'lunch',
                  start_time: '12:00 PM',
                  end_time: '12:40 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const lunchPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Lunch')
      ));
   
      assert.ok(lunchPill);
      assert.ok(lunchPill.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.ok(lunchPill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(
         lunchPill.querySelector('.itinerary-day-scheduled-pill-label')?.className.includes('species-link'),
         false
      );
      assert.match(
         lunchPill.querySelector('.itinerary-day-scheduled-pill-time-range')?.textContent ?? '',
         /12:00 PM – 12:40 PM/
      );
      lunchPill?.querySelector('.itinerary-day-open-pill-menu-item')?.click();
      assert.deepEqual(removeCalls, [{
         itemType: 'lunch',
         key: '',
      }]);
   });
   
   test('scheduled guardians talk renders as timeline event card without pill menu', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: () => {},
               onRemoveItineraryItem: () => {},
            },
         }
      );
      const tigerEvent = [...planner.querySelectorAll('.itinerary-day-event')].find((event) => (
         allTextFor(event).includes('Amur Tiger')
      ));
   
      assert.ok(tigerEvent);
      assert.equal(
         tigerEvent.querySelector('.itinerary-day-scheduled-pill--with-menu'),
         null
      );
   });
   
   test('scheduled animal pill menu offers unschedule and remove', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:15 PM',
                  end_time: '1:45 PM',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
               onRemoveItineraryItem: (request) => {
                  removeCalls.push(request);
               },
            },
         }
      );
      const lionPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('African Lion')
      ));
      const menuItems = [
         ...(lionPill?.querySelectorAll('.itinerary-day-open-pill-menu-item') ?? []),
      ];
   
      assert.equal(menuItems.length, 2);
      assert.deepEqual(
         menuItems.map((button) => button.textContent),
         ['Unschedule', 'Remove']
      );
   
      menuItems[0].click();
      menuItems[1].click();
   
      assert.deepEqual(unscheduleCalls, [{
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }]);
      assert.deepEqual(removeCalls, [{
         itemType: 'animals',
         key: 'African Lion||Africa Savanna',
      }]);
   });
   
   test('scheduled list rows show unschedule and remove buttons for animals and attractions only', () => {
      const unscheduleCalls = [];
      const removeCalls = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:00 PM',
                  end_time: '1:30 PM',
               },
            ],
            attractions: [
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
               onUnscheduleItineraryItem: (request) => {
                  unscheduleCalls.push(request);
               },
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
      const tigerRow = [...(scheduledList?.querySelectorAll('.itin-panel-item') ?? [])].find((row) => (
         allTextFor(row).includes('Amur Tiger')
      ));
      const tigerButtons = tigerRow?.querySelectorAll('.itin-panel-item-action-btn') ?? [];
   
      assert.equal(scheduledButtons.length, 5);
      assert.equal(
         scheduledButtons.every((button) => (
            button.textContent === 'Unschedule' || button.textContent === 'Remove'
         )),
         true
      );
      assert.equal(tigerButtons.length, 1);
      assert.equal(tigerButtons[0]?.textContent, 'Remove');
      assert.equal(unscheduledList?.querySelectorAll('.itin-panel-item-action-btn').length ?? 0, 0);
   
      [...scheduledButtons]
         .filter((button) => button.textContent === 'Unschedule')
         .forEach((button) => {
            button.click();
         });
   
      assert.deepEqual(unscheduleCalls, [
         {
            itemType: 'animals',
            key: 'African Lion||Africa Savanna',
         },
         {
            itemType: 'attractions',
            key: 'Zoomobile',
         },
      ]);
      assert.equal(removeCalls.length, 0);
   });
   
   test('departure marker remove menu clears departure time through handler', () => {
      const departureRemovals = [];
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-15',
            openTime: '09:30',
            lastAdmissionTime: '17:00',
            closeTime: '18:00',
         },
         {
            departureTime: '17:15',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         },
         {
            onDepartureTimeChange: (value) => {
               departureRemovals.push(value);
            },
         }
      );
      const departureMarker = boundaryMarkerByLabel(planner, 'Departure');
   
      assert.ok(departureMarker?.classList.contains('itinerary-day-boundary-marker--with-menu'));
      assert.equal(departureMarker?.attributes?.['data-boundary-marker-kind'], 'departure');
      assert.equal(departureMarker?.attributes?.['aria-label'], 'Departure');
      departureMarker?.querySelector('.itinerary-day-open-pill-menu-item')?.click();
      assert.deepEqual(departureRemovals, [ '' ]);
   });
   
   test('day planner stacks zoo hours and arrival markers at the same time', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:30',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         }
      );
      const openTimeCell = [...planner.querySelectorAll('.itinerary-day-time')].find((cell) => (
         cell.querySelector('.itinerary-day-time-label')?.textContent === '9:30 AM'
      ));
      const arrivalStrip = boundaryMarkerStripByLabel(planner, 'Arrival');
      const markers = arrivalStrip?.querySelectorAll('.itinerary-day-boundary-marker') ?? [];
   
      assert.match(allTextFor(openTimeCell), /Zoo Opens/);
      assert.ok(arrivalStrip);
      assert.equal(markers.length, 1);
      assert.equal(arrivalStrip?.querySelector('.itinerary-day-boundary-marker')?.attributes?.['aria-label'], 'Arrival');
   });
   
   test('day planner keeps scheduled items visible when they start at arrival time', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:30',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Babirusa',
                  exhibit: 'Indo-Malaya',
                  start_time: '09:30',
                  end_time: '09:45',
               },
            ],
         }
      );
      const arrivalStrip = boundaryMarkerStripByLabel(planner, 'Arrival');
      const babirusaPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Babirusa')
      ));
      const babirusaStrip = babirusaPill?.parentElement;
   
      assert.ok(arrivalStrip);
      assert.ok(babirusaPill);
      assert.equal(babirusaStrip?.attributes?.['data-scheduled-column'], 'true');
      assert.equal(babirusaStrip?.attributes?.['data-offset-fraction'], undefined);
      assert.equal(arrivalStrip?.attributes?.['data-visit-boundary-placement'], 'ends-at-anchor');
      assert.notEqual(arrivalStrip, babirusaStrip);
   });
   
   test('day planner stacks departure marker and close pills at the same time', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-15',
            openTime: '09:30',
            lastAdmissionTime: '17:00',
            closeTime: '18:00',
         },
         {
            departureTime: '18:00',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         }
      );
      const timeCells = planner.querySelectorAll('.itinerary-day-time');
      const closeTimeCells = [...timeCells].filter((cell) => (
         cell.querySelector('.itinerary-day-time-label')?.textContent === '6:00 PM'
      ));
   
      assert.equal(closeTimeCells.length, 1);
      assert.match(allTextFor(closeTimeCells[0]), /Zoo Closes/);
   
      const pillStrips = planner.querySelectorAll('.itinerary-day-pill-strip');
      const departureStrip = boundaryMarkerStripByLabel(planner, 'Departure');
   
      assert.ok(departureStrip);
      assert.equal(departureStrip.querySelectorAll('.itinerary-day-boundary-marker').length, 1);
      assert.equal(departureStrip.attributes?.['data-visit-boundary-placement'], 'starts-at-anchor');
   });
   
   test('day planner positions off-slot arrival and departure between half-hour lines', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '09:45',
            departureTime: '17:15',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
         }
      );
      const timeLabels = [...planner.querySelectorAll('.itinerary-day-time-label')].map(
         (cell) => cell.textContent
      );
      const arrivalStrip = boundaryMarkerStripByLabel(planner, 'Arrival');
      const departureStrip = boundaryMarkerStripByLabel(planner, 'Departure');
   
      assert.ok(!timeLabels.includes('9:45 AM'));
      assert.ok(!timeLabels.includes('5:15 PM'));
      assert.ok(boundaryMarkerByLabel(planner, 'Arrival'));
      assert.ok(boundaryMarkerByLabel(planner, 'Departure'));
      assert.equal(arrivalStrip?.attributes?.['data-offset-fraction'], '0.5');
      assert.equal(departureStrip?.attributes?.['data-offset-fraction'], '0.5');
   });
   
   test('day planner renders scheduled guardians talks and wild encounters', () => {
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
            wildEncounters: [
               {
                  name: 'African Rainforest',
                  meeting_spot: 'Wild Encounter - Africa Meeting Spot',
                  start_time: '2:00 PM',
                  end_time: '2:45 PM',
                  maximum_duration: 45,
               },
            ],
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
         }
      );
      const text = allTextFor(planner);
   
      assert.match(text, /Amur Tiger/);
      assert.match(text, /Location: Eurasia Wilds/);
      assert.match(text, /African Rainforest/);
      assert.match(text, /Meeting Spot: Wild Encounter - Africa Meeting Spot/);
      assert.match(text, /Scheduled Items/);
      assert.match(text, /Meet The Guardians \(1\)/);
      assert.match(text, /Wild Encounters \(1\)/);
      assert.match(text, /Animals \(1\)/);
      assert.match(text, /African Lion/);
      assert.match(text, /Attractions \(1\)/);
      assert.match(text, /Zoomobile/);
      assert.match(text, /Unscheduled Items/);
      assert.match(text, /Animals \(1\)/);
      assert.match(text, /Giant Panda/);
      assert.match(text, /Attractions \(1\)/);
      assert.match(text, /Conservation Carousel/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Meet The Guardians/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Wild Encounters/);
      assert.ok(text.indexOf('Scheduled Items') < text.indexOf('Unscheduled Items'));
   
      const timelineEventTexts = timelineScheduledPillTexts(planner);
   
      assert.equal(timelineEventTexts.length, 4);
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('African Lion')));
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('Amur Tiger')));
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('African Rainforest')));
      assert.ok(timelineEventTexts.some((eventText) => eventText.includes('Zoomobile')));
   
      const dayItemsSections = [...planner.querySelectorAll('.itinerary-day-items-sections')];
      const scheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Scheduled Items')
      ));
      const unscheduledList = dayItemsSections.find((section) => (
         section.querySelector('.itinerary-day-items-title')?.textContent?.includes('Unscheduled Items')
      ));
   
      assert.equal(
         scheduledList?.querySelectorAll('.itin-panel-section-edit-btn').length,
         2
      );
      assert.ok(
         (unscheduledList?.querySelectorAll('.itin-panel-section-edit-btn').length ?? 0) > 0
      );
   });
   
   test('day planner positions off-slot scheduled items between half-hour lines', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '1:15 PM',
                  end_time: '1:45 PM',
               },
            ],
         }
      );
      const lionPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('African Lion')
      ));
      const lionStrip = lionPill?.parentElement;
   
      assert.ok(lionPill);
      assert.equal(lionStrip?.className, 'itinerary-day-pill-strip');
      assert.equal(lionStrip?.attributes?.['data-offset-fraction'], '0.5');
      assert.equal(lionPill.attributes?.['data-duration-fraction'], '1');
   });
   
   test('day planner renders scheduled duration as a larger pill', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            arrivalTime: '11:35',
            departureTime: '17:15',
            itineraryConfig: TEST_ITINERARY_CONFIG,
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Polar Bear',
                  exhibit: 'Tundra Trek',
                  start_time: '11:35 AM',
                  end_time: '11:45 AM',
               },
            ],
         }
      );
      const polarPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Polar Bear')
      ));
      const polarStrip = polarPill?.parentElement;
   
      assert.ok(polarPill);
      assert.equal(polarStrip?.className, 'itinerary-day-pill-strip');
      assert.equal(polarStrip?.attributes?.['data-scheduled-column'], 'true');
      assert.equal(polarPill.attributes?.['data-duration-fraction'], String(10 / 30));
      assert.equal(
         Boolean(boundaryMarkerByLabel(planner, 'Arrival')),
         true
      );
      assert.ok(boundaryMarkerByLabel(planner, 'Departure'));
      assert.equal(
         [...planner.querySelectorAll('.itinerary-day-boundary-marker')].some((marker) => (
            marker.attributes?.['aria-label'] === 'Polar Bear'
         )),
         false
      );
   });
   
   test('day planner keeps short scheduled visits readable', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Ring-Tailed Lemur',
                  exhibit: 'Australasia',
                  start_time: '12:00',
                  end_time: '12:08',
               },
            ],
         },
         {},
         {
            scheduleHandlers: {
               onUnscheduleItineraryItem: () => {},
            },
         }
      );
      const lemurPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
         allTextFor(pill).includes('Ring-Tailed Lemur')
      ));
   
      assert.ok(lemurPill?.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.equal(lemurPill.attributes?.['data-duration-fraction'], String(8 / 30));
      assert.match(allTextFor(lemurPill), /Ring-Tailed Lemur/);
   });
   
   test('day planner merges overlapping scheduled pills into carousel groups', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Polar Bear',
                  exhibit: 'Tundra Trek',
                  start_time: '4:30 PM',
                  end_time: '4:32 PM',
               },
               {
                  species: 'African Lion',
                  exhibit: 'Africa Savanna',
                  start_time: '4:32 PM',
                  end_time: '4:34 PM',
               },
            ],
         }
      );
      const groupedPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill--grouped')].find((pill) => (
         allTextFor(pill).includes('Polar Bear')
         || allTextFor(pill).includes('African Lion')
      ));
   
      assert.ok(groupedPill);
      assert.match(allTextFor(groupedPill), /\+ 1/);
   });
   
   test('day planner keeps scheduled pills within the timeline grid width', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            animals: [
               {
                  species: 'Solomon Island Leaf Frog',
                  exhibit: 'Americas',
                  start_time: '11:00 AM',
                  end_time: '11:30 AM',
               },
            ],
         }
      );
      const pill = planner.querySelector('.itinerary-day-scheduled-pill');
      const strip = pill?.parentElement;
   
      assert.ok(pill);
      assert.equal(strip?.attributes?.['data-scheduled-column'], 'true');
      assert.equal(strip?.attributes?.['data-dynamic-horizontal-offset'], undefined);
   });

   test('day planner omits guardians talks and wild encounters from unscheduled items', () => {
      const planner = makeDayPlannerPreview(
         {
            date: '2026-06-20',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         {
            ...EMPTY_ITINERARY,
            guardiansTalks: [
               {
                  name: 'Amur Tiger',
                  location: 'Eurasia Wilds',
                  start_time: '1:30 PM',
                  end_time: '2:00 PM',
                  maximum_duration: 30,
               },
            ],
         }
      );
      const text = allTextFor(planner);
   
      assert.match(text, /Scheduled Items/);
      assert.match(text, /Meet The Guardians \(1\)/);
      assert.match(text, /Unscheduled Items/);
      assert.match(text, /Animals \(0\)/);
      assert.match(text, /Attractions \(0\)/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Meet The Guardians/);
      assert.doesNotMatch(text, /Unscheduled Items[\s\S]*Wild Encounters/);
   });
});
