import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
import { showRemovedItemsPopup } from '../../scripts/itinerary/panel/components/removedItemsPopup.js';
import { updateItineraryAdjustmentTypesFromConfig } from '../../scripts/itinerary/itineraryAdjustmentTypes.js';
import {
   areItineraryScheduleTimesOrdered,
   buildArrivalTimeBounds,
   buildDepartureTimeBounds,
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   isArrivalTimeWithinBounds,
   isDepartureTimeWithinBounds,
   parseClockTimeMinutes,
   resolveArrivalTimeValidationError,
   resolveDepartureTimeValidationError,
} from '../../scripts/itinerary/panel/dayPlannerSchedule.js';
import {
   buildMarkersByAnchorSlot,
   computeMarkerOffsetFraction,
   findTimelineAnchorSlot,
} from '../../scripts/itinerary/panel/dayPlannerTimelineMarkers.js';
import {
   computeStripHorizontalOffsetIndex,
   computeTimelineHorizontalOffsetIndex,
} from '../../scripts/itinerary/panel/components/dayPlannerTimelinePills.js';
import {
   formatClockTime,
   formatISODateFull,
   formatISODateLong,
   normalizeAnimal,
   normalizeAttraction,
   normalizeTalk,
   normalizeWild,
} from '../../scripts/itinerary/panel/format.js';
import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../../scripts/itinerary/panel/rows.js';
import {
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../scripts/shared/constants.js';
import { installTestWindow } from './helpers/domMock.mjs';

const EMPTY_ITINERARY = {
   animals: [],
   attractions: [],
   guardiansTalks: [],
   wildEncounters: [],
};

const TEST_ITINERARY_CONFIG = {
   eventTypes: [
      'arrival',
      'breakfast',
      'break',
      'departure',
      'dinner',
      'lunch',
      'shopping',
      'snack',
   ],
   visitBoundaryEventTypes: {
      arrival: 'arrival',
      departure: 'departure',
   },
};

function createNode(tagName, className = '', textContent = '') {
   const children = [];
   const listeners = {};
   const attributes = {};
   const classes = new Set(className ? className.split(/\s+/).filter(Boolean) : []);

   const node = {
      tagName,
      get className() {
         return [...classes].join(' ');
      },
      set className(value) {
         classes.clear();

         for (const token of String(value).split(/\s+/)) {
            if (token) {
               classes.add(token);
            }
         }
      },
      textContent,
      children,
      listeners,
      attributes,
      hidden: false,
      disabled: false,
      style: {
         setProperty(name, value) {
            attributes[`style:${name}`] = value;
         },
      },
      classList: {
         contains(value) {
            return classes.has(value);
         },
         add(value) {
            classes.add(value);
         },
         toggle(value, shouldAdd) {
            if (shouldAdd) {
               classes.add(value);
            } else {
               classes.delete(value);
            }
         },
      },
      appendChild(child) {
         child.parentElement = node;
         child.parent = node;
         children.push(child);
         return child;
      },
      insertBefore(newChild, referenceChild) {
         newChild.parentElement = node;
         newChild.parent = node;

         if (!referenceChild) {
            children.push(newChild);
            return newChild;
         }

         const referenceIndex = children.indexOf(referenceChild);

         if (referenceIndex < 0) {
            children.push(newChild);
            return newChild;
         }

         children.splice(referenceIndex, 0, newChild);
         return newChild;
      },
      removeChild(child) {
         const childIndex = children.indexOf(child);

         if (childIndex >= 0) {
            children.splice(childIndex, 1);
         }

         child.parentElement = null;
         child.parent = null;

         return child;
      },
      closest(selector) {
         let current = node;

         while (current) {
            if (nodeMatchesSelector(current, selector)) {
               return current;
            }

            current = current.parentElement ?? current.parent;
         }

         return null;
      },
      get offsetHeight() {
         if (classes.has('itinerary-day-open-pill')) {
            return TIMELINE_POINT_PILL_HEIGHT_PX;
         }

         if (classes.has('itinerary-day-grid-line')) {
            return TIMELINE_SLOT_HEIGHT_PX;
         }

         return 0;
      },
      append(...items) {
         children.push(...items);
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      contains(target) {
         if (target === node) {
            return true;
         }

         return children.some((child) => child.contains?.(target) ?? false);
      },
      click() {
         const event = {
            preventDefault() {},
            stopPropagation() {},
         };

         listeners.click?.(event);
      },
      getBoundingClientRect() {
         return {
            height: classes.has('itinerary-day-open-pill')
               ? TIMELINE_POINT_PILL_HEIGHT_PX
               : 100,
         };
      },
      setAttribute(name, value) {
         attributes[name] = value;
      },
      getAttribute(name) {
         return attributes[name] ?? null;
      },
      querySelector(selector) {
         const classNameToFind = selector.startsWith('.')
            ? selector.slice(1)
            : selector;
         const stack = [...children];

         while (stack.length > 0) {
            const child = stack.shift();

            if (child.className?.split(/\s+/).includes(classNameToFind)) {
               return child;
            }

            stack.push(...(child.children ?? []));
         }

         return null;
      },
      querySelectorAll(selector) {
         const matches = [];
         const classNameToFind = selector.startsWith('.')
            ? selector.slice(1)
            : selector;
         const stack = [...children];

         while (stack.length > 0) {
            const child = stack.shift();

            if (child.className?.split(/\s+/).includes(classNameToFind)) {
               matches.push(child);
            }

            stack.push(...(child.children ?? []));
         }

         return matches;
      },
   };

   if (className) {
      node.className = className;
   }

   return node;
}

function nodeMatchesSelector(node, selector) {
   if (!node || selector[0] !== '.') {
      return false;
   }

   const className = selector.slice(1);
   return node.classList?.contains(className) ?? false;
}

function allTextFor(node) {
   return [
      node.textContent,
      ...(node.children ?? []).map(allTextFor),
   ].flat(Infinity).filter(Boolean).join(' ');
}

function timelinePillTexts(planner) {
   const timeline = planner.querySelector('.itinerary-day-timeline');

   return [...(timeline?.querySelectorAll('.itinerary-day-open-pill') ?? [])].map(allTextFor);
}

function timelineScheduledPillTexts(planner) {
   const timeline = planner.querySelector('.itinerary-day-timeline');

   return [
      ...(timeline?.querySelectorAll('.itinerary-day-scheduled-pill') ?? []),
      ...(timeline?.querySelectorAll('.itinerary-day-event') ?? []),
   ].map(allTextFor);
}

function boundaryMarkerByLabel(planner, label) {
   return [...planner.querySelectorAll('.itinerary-day-boundary-marker')].find((marker) => (
      marker.attributes?.['aria-label'] === label
   ));
}

function boundaryMarkerStripByLabel(planner, label) {
   return boundaryMarkerByLabel(planner, label)?.parentElement ?? null;
}

function textFor(row, selector) {
   return row.querySelector(selector)?.textContent ?? '';
}

function imageSrcFor(row) {
   return row.querySelector('.itin-panel-thumb')?.children[0]?.src ?? '';
}

const documentListeners = new Map();

test.describe('itinerary panel rows', () => {
   beforeEach(() => {
      documentListeners.clear();
      globalThis.document = {
         createElement: (tagName) => createNode(tagName),
         createTextNode: (textContent) => createNode('#text', '', textContent),
         addEventListener(eventName, handler) {
            const handlers = documentListeners.get(eventName) ?? [];
            handlers.push(handler);
            documentListeners.set(eventName, handlers);
         },
         removeEventListener(eventName, handler) {
            const handlers = documentListeners.get(eventName) ?? [];
            documentListeners.set(
               eventName,
               handlers.filter((registeredHandler) => registeredHandler !== handler)
            );
         },
      };
      installTestWindow();
      updateItineraryAdjustmentTypesFromConfig({
         adjustmentTypes: {
            ARRIVAL_TIME_ADJUSTED: 'arrivalTimeAdjusted',
         DEPARTURE_TIME_ADJUSTED: 'departureTimeAdjusted',
         },
      });
      globalThis.requestAnimationFrame = (callback) => callback();
   });

   afterEach(() => {
      delete globalThis.document;
      delete globalThis.requestAnimationFrame;
   });

   test('formats and normalizes itinerary panel item data', () => {
      assert.match(formatISODateLong('2026-06-15'), /June 15, 2026/);
      assert.equal(formatISODateLong('not-a-date'), '');
      assert.equal(formatISODateFull('2026-06-20'), 'Saturday, June 20, 2026');
      assert.equal(formatISODateFull('not-a-date', 'Fallback Date'), 'not-a-date');
      assert.equal(formatClockTime('09:30'), '9:30 AM');
      assert.equal(formatClockTime('09:30:30'), '9:30:30 AM');
      assert.equal(formatClockTime('19:00'), '7:00 PM');
      assert.equal(formatClockTime('', 'Fallback Time'), 'Fallback Time');
      assert.equal(parseClockTimeMinutes('09:30'), 570);
      assert.equal(parseClockTimeMinutes('09:30:30'), 570.5);
      assert.equal(parseClockTimeMinutes('10:00 AM'), 600);
      assert.equal(parseClockTimeMinutes('10:00:30 AM'), 600.5);
      assert.equal(parseClockTimeMinutes('1:30 PM'), 810);
      assert.equal(parseClockTimeMinutes('bad-time'), null);
      assert.equal(formatMinutesAsClockTime(1140), '7:00 PM');
      assert.deepEqual(buildArrivalTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
      }), {
         minMinutes: 540,
         maxMinutes: 1080,
         minScheduleTime: '09:00',
         maxScheduleTime: '18:00',
         minClockTime: '9:00 AM',
         maxClockTime: '6:00 PM',
      });
      assert.deepEqual(buildArrivalTimeBounds({
         openTime: '09:30',
         lastAdmissionTime: '17:00',
      }), {
         minMinutes: 570,
         maxMinutes: 1020,
         minScheduleTime: '09:30',
         maxScheduleTime: '17:00',
         minClockTime: '9:30 AM',
         maxClockTime: '5:00 PM',
      });
      assert.equal(isArrivalTimeWithinBounds('9:00 AM', buildArrivalTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
      })), true);
      assert.equal(isArrivalTimeWithinBounds('8:45 AM', buildArrivalTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
      })), false);
      assert.equal(isArrivalTimeWithinBounds('6:00 PM', buildArrivalTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
      })), true);
      assert.equal(isArrivalTimeWithinBounds('6:15 PM', buildArrivalTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
      })), false);
      assert.equal(isArrivalTimeWithinBounds('', buildArrivalTimeBounds({
         openTime: '09:30',
         lastAdmissionTime: '17:00',
      })), true);
      assert.deepEqual(buildDepartureTimeBounds({
         openTime: '09:30',
         closeTime: '18:00',
      }), {
         minMinutes: 570,
         maxMinutes: 1080,
         minScheduleTime: '09:30',
         maxScheduleTime: '18:00',
         minClockTime: '9:30 AM',
         maxClockTime: '6:00 PM',
      });
      assert.equal(isDepartureTimeWithinBounds('9:30 AM', buildDepartureTimeBounds({
         openTime: '09:30',
         closeTime: '18:00',
      })), true);
      assert.equal(isDepartureTimeWithinBounds('9:00 AM', buildDepartureTimeBounds({
         earlyAdmissionTime: '09:00',
         openTime: '09:30',
         closeTime: '19:00',
      })), false);
      assert.equal(isDepartureTimeWithinBounds('6:00 PM', buildDepartureTimeBounds({
         openTime: '09:30',
         closeTime: '18:00',
      })), true);
      assert.equal(isDepartureTimeWithinBounds('6:15 PM', buildDepartureTimeBounds({
         openTime: '09:30',
         closeTime: '18:00',
      })), false);
      assert.equal(isDepartureTimeWithinBounds('', buildDepartureTimeBounds({
         openTime: '09:30',
         closeTime: '18:00',
      })), true);
      assert.equal(areItineraryScheduleTimesOrdered('9:30 AM', '5:00 PM'), true);
      assert.equal(areItineraryScheduleTimesOrdered('5:00 PM', '5:00 PM'), false);
      assert.equal(areItineraryScheduleTimesOrdered('5:15 PM', '5:00 PM'), false);
      assert.equal(areItineraryScheduleTimesOrdered('', '5:00 PM'), true);
      assert.equal(resolveDepartureTimeValidationError(
         '9:30 AM',
         buildDepartureTimeBounds({ openTime: '09:30', closeTime: '18:00' }),
         '9:30 AM',
         {
            departureTimeInvalid: 'hours',
            departureTimeAfterArrivalInvalid: 'order',
         }
      ), 'order');
      assert.equal(resolveArrivalTimeValidationError(
         '5:00 PM',
         buildArrivalTimeBounds({
            openTime: '09:30',
            lastAdmissionTime: '17:00',
         }),
         '5:00 PM',
         {
            arrivalTimeInvalid: 'hours',
            arrivalTimeBeforeDepartureInvalid: 'order',
         }
      ), 'order');
      assert.deepEqual(buildHalfHourSlotStarts(570, 720), [
         570,
         600,
         630,
         660,
         690,
      ]);
      assert.deepEqual(normalizeAnimal({
         species: '  African Lion  ',
         exhibit: '  Africa Savanna  ',
         likelihoodBefore: '0.9',
         likelihoodAfter: '60',
      }), {
         species: 'African Lion',
         exhibit: 'Africa Savanna',
         link: null,
         removalReason: null,
         likelihoodBefore: 0.9,
         likelihoodAfter: 60,
      });
      assert.equal(normalizeAttraction({
         name: '  Conservation Carousel  ',
         info_link: '  https://www.torontozoo.com/tickets/carousel  ',
      }).infoLink, 'https://www.torontozoo.com/tickets/carousel');
      assert.equal(normalizeTalk({ name: '  Amur Tiger  ' }).name, 'Amur Tiger');
      assert.equal(normalizeWild({ name: '  African Rainforest  ' }).name, 'African Rainforest');
   });

   test('timeline markers anchor to the preceding half-hour slot', () => {
      const slotStarts = buildHalfHourSlotStarts(570, 1140);
      const markersByAnchor = buildMarkersByAnchorSlot(
         [
            {
               startMinutes: parseClockTimeMinutes('11:35'),
               label: 'Arrival',
               kind: TEST_ITINERARY_CONFIG.visitBoundaryEventTypes.arrival,
            },
         ],
         slotStarts,
         1140
      );

      assert.equal(findTimelineAnchorSlot(parseClockTimeMinutes('11:35'), slotStarts), 690);
      assert.equal(computeMarkerOffsetFraction(695, 690, 720), 1 / 6);
      assert.deepEqual(markersByAnchor.get(690), [{
         label: 'Arrival',
         offsetFraction: 1 / 6,
         kind: 'arrival',
      }]);
   });

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

   test('computeStripHorizontalOffsetIndex shifts later overlapping strips', () => {
      const pointPillVerticalSpanFraction = (
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );

      assert.equal(
         computeStripHorizontalOffsetIndex([], 0.5, pointPillVerticalSpanFraction),
         0
      );
      assert.equal(computeStripHorizontalOffsetIndex([
         { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
      ], 0.67, pointPillVerticalSpanFraction), 1);
      assert.equal(computeStripHorizontalOffsetIndex([
         { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
         { offsetFraction: 0.67, horizontalOffsetIndex: 1 },
      ], 0.6, pointPillVerticalSpanFraction), 2);
   });

   test('computeTimelineHorizontalOffsetIndex shifts later overlapping placements', () => {
      assert.equal(computeTimelineHorizontalOffsetIndex([], 0.5, 0.5), 0);
      assert.equal(computeTimelineHorizontalOffsetIndex([
         { offsetFraction: 0.5, durationFraction: 0.5, horizontalOffsetIndex: 0 },
      ], 0.67, 0.5), 1);
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
         rows[0].querySelector('.itin-panel-name')?.className.includes('species-link'),
         'animal names should open species detail overlay'
      );
      assert.equal(textFor(rows[0], '.itin-panel-meta'), 'Exhibit: Africa Savanna');
      assert.equal(
         textFor(rows[0], '.itin-panel-alert'),
         'Projected visibility changed from 90% to 60% on your new date.'
      );
      assert.equal(textFor(rows[1], '.itin-panel-name'), 'African Lion');
      assert.equal(textFor(rows[1], '.itin-panel-meta'), 'Exhibit: Indo-Malaya Outdoor');
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

   test('animal and attraction rows show approximate scheduled start times', () => {
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

      assert.equal(
         animalRow.querySelectorAll('.itin-panel-meta')[1].textContent,
         'Time: ~2:30 PM'
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
            location: 'Front Courtyard',
            price: 'Extra charge',
            removalReason: 'The Conservation Carousel is temporarily closed.',
         },
      ]);

      assert.equal(textFor(row, '.itin-panel-name'), 'Conservation Carousel');
      assert.equal(
         row.querySelector('.itin-panel-name')?.className.includes('species-link'),
         false
      );
      assert.equal(
         imageSrcFor(row),
         'images/details/attractions/conservation-carousel.png'
      );
      assert.equal(textFor(row, '.itin-panel-meta'), 'Carousels are timeless and fun for all ages!');
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

      assert.equal(textFor(talkRow, '.itin-panel-name'), 'Amur Tiger');
      assert.equal(
         imageSrcFor(talkRow),
         'images/details/guardians-talks/amur-tiger.png'
      );
      assert.equal(textFor(talkRow, '.itin-panel-meta'), 'Location: Eurasia Wilds');
      assert.equal(
         talkRow.querySelectorAll('.itin-panel-meta')[1].textContent,
         'Time: 1:30 PM - 2:00 PM'
      );
      assert.equal(textFor(wildRow, '.itin-panel-name'), 'African Rainforest');
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
         wildRow.querySelector('.itin-panel-name')?.className.includes('species-link')
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
         ['Early Talk', 'Late Talk']
      );
      assert.deepEqual(
         wildRows.map((row) => textFor(row, '.itin-panel-name')),
         ['Morning Encounter', 'Afternoon Encounter']
      );
   });

});
