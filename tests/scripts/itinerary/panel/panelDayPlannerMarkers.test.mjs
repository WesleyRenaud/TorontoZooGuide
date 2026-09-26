import assert from 'node:assert/strict';
import { mock, test } from 'node:test';

import { DayPlannerBuilder } from '../../../../scripts/itinerary/panel/components/dayPlannerBuilder.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ZooClockTimeHelper } from '../../../../scripts/shared/zooClockTimeHelper.js';
import { Strings } from '../../../../scripts/strings.js';
import {
   EMPTY_ITINERARY,
   TEST_ITINERARY_CONFIG,
   allTextFor,
   boundaryMarkerByLabel,
   boundaryMarkerStripByLabel,
   createNode,
   documentListeners,
   installPanelRowsTestHooks,
} from '../../helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();

test('Test_MakeDayPlannerPreview_TestEarlyAdmissionAvailable_ExpectEarlyAndOpenLabels', () => {
   const earlyAdmissionTime = '09:00';
   const openTime = '09:30';
   const zooHours = {
      date: '2026-06-20',
      earlyAdmissionTime,
      openTime,
      lastAdmissionTime: '18:00',
      closeTime: '19:00',
   };

   const planner = DayPlannerBuilder.makeDayPlannerPreview(zooHours, EMPTY_ITINERARY);
   const text = allTextFor(planner);

   assert.match(text, new RegExp(ZooClockTimeHelper.formatClockTime(earlyAdmissionTime)));
   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.earlyAdmissionLabel));
   assert.match(text, new RegExp(ZooClockTimeHelper.formatClockTime(openTime)));
   assert.match(text, new RegExp(Strings.itinerary.dayPlanner.openLabel));
});


test('Test_MakeDayPlannerPreview_TestArrivalMarkerRemove_ExpectArrivalCleared', () => {
   const arrivalRemovals = [];
   const arrivalLabel = Strings.itinerary.dayPlanner.arrivalLabel;

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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
   const arrivalMarker = boundaryMarkerByLabel(planner, arrivalLabel);
   const openPill = [...planner.querySelectorAll('.itinerary-day-time-boundary-label')].find((label) => (
      allTextFor(label).includes(Strings.itinerary.dayPlanner.openLabel)
   ));

   assert.ok(arrivalMarker?.classList.contains('itinerary-day-boundary-marker--with-menu'));
   assert.equal(arrivalMarker?.attributes?.['data-boundary-marker-kind'], 'arrival');
   assert.equal(arrivalMarker?.attributes?.['aria-label'], arrivalLabel);
   assert.ok(openPill);

   arrivalMarker?.querySelector('.itinerary-day-open-pill-menu-item')?.click();

   assert.deepEqual(arrivalRemovals, ['']);
});


test('Test_Day_TestDayPlannerHeaderClearButtonsRemoveArrivalAnd_ExpectOk', async () => {
   const arrivalChanges = [];
   const departureChanges = [];
   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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

   assert.equal(clearButtons.length, Position.THIRD);
   assert.equal(
      clearButtons.at(Position.FIRST).attributes?.['aria-label'],
      Strings.itinerary.dayPlanner.clearArrivalTimeAria
   );
   assert.equal(
      clearButtons.at(Position.SECOND).attributes?.['aria-label'],
      Strings.itinerary.dayPlanner.clearDepartureTimeAria
   );

   clearButtons.at(Position.FIRST).click();
   await Promise.resolve();
   clearButtons.at(Position.SECOND).click();
   await Promise.resolve();

   assert.deepEqual(arrivalChanges, ['']);
   assert.deepEqual(departureChanges, ['']);
});


test('Test_Day_TestDayPlannerHeaderDisablesClearButtonsWhenTimes_ExpectOk', () => {
   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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

   assert.equal(clearButtons.length, Position.THIRD);
   assert.ok(clearButtons.every((button) => button.disabled));
});


test('Test_Day_TestDayPlannerDepartureInputRejectsInvalidPickerValue_ExpectOk', async (t) => {
   mock.timers.enable({ apis: ['setTimeout'] });
   t.after(() => {
      mock.timers.reset();
   });

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

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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
   const departureInput = inputs.at(Position.SECOND);
   const outsideTarget = createNode('button');
   const invalidDeparture = '8:00 PM';
   const restoredDeparture = ZooClockTimeHelper.formatClockTime('18:30');

   departureInput.value = invalidDeparture;
   documentListeners.get('mousedown')?.forEach((handler) => {
      handler({ target: outsideTarget });
   });
   await Promise.resolve();

   assert.deepEqual(departureChanges, []);
   assert.equal(pickerInstances.at(Position.SECOND)?.closeCalled, true);
   assert.equal(departureInput.value, restoredDeparture);

   mock.timers.tick(TimelineLayoutConstants.DAY_PLANNER_ACTION_FEEDBACK_DISMISS_MS);
});


test('Test_Departure_TestDepartureMarkerRemoveMenuClearsDepartureTimeThrough_ExpectOk', () => {
   const departureRemovals = [];
   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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

   assert.deepEqual(departureRemovals, ['']);
});


test('Test_Day_TestDayPlannerKeepsScheduledItemsVisibleWhenThey_ExpectOk', () => {
   const capybaraName = 'Capybara';
   const arrivalTime = '09:30';

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: arrivalTime,
         lastAdmissionTime: '18:00',
         closeTime: '19:00',
      },
      {
         arrivalTime,
         itineraryConfig: TEST_ITINERARY_CONFIG,
         ...EMPTY_ITINERARY,
         animals: [
            {
               species: capybaraName,
               exhibit: 'Indo-Malaya',
               start_time: arrivalTime,
               end_time: '09:45',
            },
         ],
      }
   );
   const arrivalStrip = boundaryMarkerStripByLabel(planner, Strings.itinerary.dayPlanner.arrivalLabel);
   const capybaraPill = [...planner.querySelectorAll('.itinerary-day-scheduled-pill')].find((pill) => (
      allTextFor(pill).includes(capybaraName)
   ));
   const capybaraStrip = capybaraPill?.parentElement;

   assert.ok(arrivalStrip);
   assert.ok(capybaraPill);
   assert.equal(capybaraStrip?.attributes?.['data-scheduled-column'], 'true');
   assert.equal(capybaraStrip?.attributes?.['data-offset-fraction'], undefined);
   assert.equal(arrivalStrip?.attributes?.['data-visit-boundary-placement'], 'ends-at-anchor');
   assert.notEqual(arrivalStrip, capybaraStrip);
});


test('Test_Day_TestDayPlannerStacksDepartureMarkerAndClosePills_ExpectOk', () => {
   const planner = DayPlannerBuilder.makeDayPlannerPreview(
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
   const closeTime = ZooClockTimeHelper.formatClockTime('18:00');
   const timeCells = planner.querySelectorAll('.itinerary-day-time');
   const closeTimeCells = [...timeCells].filter((cell) => (
      cell.querySelector('.itinerary-day-time-label')?.textContent === closeTime
   ));
   const departureStrip = boundaryMarkerStripByLabel(planner, 'Departure');

   assert.equal(closeTimeCells.length, Position.SECOND);
   assert.match(allTextFor(closeTimeCells.at(Position.FIRST)), new RegExp(Strings.itinerary.dayPlanner.closeLabel));
   assert.ok(departureStrip);
   assert.equal(
      departureStrip.querySelectorAll('.itinerary-day-boundary-marker').length,
      Position.SECOND
   );
   assert.equal(departureStrip.attributes?.['data-visit-boundary-placement'], 'starts-at-anchor');
});


test('Test_Day_TestDayPlannerPositionsOffSlotArrivalAndDeparture_ExpectOk', () => {
   const arrivalTime = '09:45';
   const departureTime = '17:15';
   const offsetFraction = '0.5';

   const planner = DayPlannerBuilder.makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
         closeTime: '19:00',
      },
      {
         arrivalTime,
         departureTime,
         itineraryConfig: TEST_ITINERARY_CONFIG,
         ...EMPTY_ITINERARY,
      }
   );
   const timeLabels = [...planner.querySelectorAll('.itinerary-day-time-label')].map(
      (cell) => cell.textContent
   );
   const arrivalStrip = boundaryMarkerStripByLabel(planner, Strings.itinerary.dayPlanner.arrivalLabel);
   const departureStrip = boundaryMarkerStripByLabel(planner, 'Departure');

   assert.ok(!timeLabels.includes(ZooClockTimeHelper.formatClockTime(arrivalTime)));
   assert.ok(!timeLabels.includes(ZooClockTimeHelper.formatClockTime(departureTime)));
   assert.ok(boundaryMarkerByLabel(planner, Strings.itinerary.dayPlanner.arrivalLabel));
   assert.ok(boundaryMarkerByLabel(planner, 'Departure'));
   assert.equal(arrivalStrip?.attributes?.['data-offset-fraction'], offsetFraction);
   assert.equal(departureStrip?.attributes?.['data-offset-fraction'], offsetFraction);
});
