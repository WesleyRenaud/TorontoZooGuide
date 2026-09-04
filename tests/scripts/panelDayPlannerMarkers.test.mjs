import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { SectionConfigs } from '../../scripts/itinerary/panel/sectionConfigs.js';
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


test.describe('itinerary day planner preview markers', () => {
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
   
});
