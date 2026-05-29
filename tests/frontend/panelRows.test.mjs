import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import { makeDayPlannerPreview } from '../../scripts/itinerary/panel/components/dayPlanner.js';
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

function createNode(tagName, className = '', textContent = '') {
   const children = [];
   const listeners = {};
   const attributes = {};
   const classes = new Set(className ? className.split(/\s+/) : []);

   return {
      tagName,
      className,
      textContent,
      children,
      listeners,
      attributes,
      style: {
         setProperty(name, value) {
            attributes[`style:${name}`] = value;
         },
      },
      classList: {
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
         children.push(child);
         return child;
      },
      append(...items) {
         children.push(...items);
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
      },
      getBoundingClientRect() {
         return {
            height: 100,
         };
      },
      setAttribute(name, value) {
         attributes[name] = value;
      },
      querySelector(selector) {
         const classNameToFind = selector.startsWith('.')
            ? selector.slice(1)
            : selector;
         const stack = [...children];

         while (stack.length > 0) {
            const child = stack.shift();

            if (child.className === classNameToFind) {
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

            if (child.className === classNameToFind) {
               matches.push(child);
            }

            stack.push(...(child.children ?? []));
         }

         return matches;
      },
   };
}

function allTextFor(node) {
   return [
      node.textContent,
      ...(node.children ?? []).map(allTextFor),
   ].flat(Infinity).filter(Boolean).join(' ');
}

function textFor(row, selector) {
   return row.querySelector(selector)?.textContent ?? '';
}

function imageSrcFor(row) {
   return row.querySelector('.itin-panel-thumb')?.children[0]?.src ?? '';
}

beforeEach(() => {
   globalThis.document = {
      createElement: (tagName) => createNode(tagName),
      createTextNode: (textContent) => createNode('#text', '', textContent),
   };
   globalThis.window = {
      addEventListener: () => {},
      getComputedStyle: () => ({
         gap: '0',
         paddingBottom: '0',
         paddingTop: '0',
         rowGap: '0',
      }),
      open: () => {},
      removeEventListener: () => {},
   };
   globalThis.requestAnimationFrame = (callback) => callback();
});

afterEach(() => {
   delete globalThis.document;
   delete globalThis.requestAnimationFrame;
   delete globalThis.window;
});

test('formats and normalizes itinerary panel item data', () => {
   assert.match(formatISODateLong('2026-06-15'), /June 15, 2026/);
   assert.equal(formatISODateLong('not-a-date'), '');
   assert.equal(formatISODateFull('2026-06-20'), 'Saturday, June 20, 2026');
   assert.equal(formatISODateFull('not-a-date', 'Fallback Date'), 'not-a-date');
   assert.equal(formatClockTime('09:30'), '9:30 AM');
   assert.equal(formatClockTime('19:00'), '7:00 PM');
   assert.equal(formatClockTime('', 'Fallback Time'), 'Fallback Time');
   assert.equal(parseClockTimeMinutes('09:30'), 570);
   assert.equal(parseClockTimeMinutes('10:00 AM'), 600);
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

test('day planner starts at early admission when available', () => {
   const planner = makeDayPlannerPreview({
      date: '2026-06-20',
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
      closeTime: '19:00',
   });
   const text = allTextFor(planner);

   assert.match(text, /9:00 AM/);
   assert.match(text, /Early Admission/);
   assert.match(text, /9:30 AM/);
   assert.match(text, /Zoo Opens/);
});

test('day planner stacks zoo hours and arrival pills at the same time', () => {
   const planner = makeDayPlannerPreview(
      {
         date: '2026-06-20',
         openTime: '09:30',
         lastAdmissionTime: '18:00',
         closeTime: '19:00',
      },
      {
         arrivalTime: '09:30',
      }
   );
   const pillStrip = planner.querySelector('.itinerary-day-pill-strip');
   const pills = pillStrip.querySelectorAll('.itinerary-day-open-pill');

   assert.ok(pillStrip);
   assert.equal(pills.length, 2);
   assert.match(allTextFor(pillStrip), /Zoo Opens/);
   assert.match(allTextFor(pillStrip), /Arrival/);
});

test('day planner stacks departure and close pills at the same time', () => {
   const planner = makeDayPlannerPreview(
      {
         date: '2026-06-15',
         openTime: '09:30',
         lastAdmissionTime: '17:00',
         closeTime: '18:00',
      },
      {
         departureTime: '18:00',
      }
   );
   const timeCells = planner.querySelectorAll('.itinerary-day-time');
   const closeTimeCells = timeCells.filter((cell) => cell.textContent === '6:00 PM');

   assert.equal(closeTimeCells.length, 1);

   const pillStrips = planner.querySelectorAll('.itinerary-day-pill-strip');
   const closePillStrip = pillStrips.find((strip) => (
      allTextFor(strip).includes('Departure')
      && allTextFor(strip).includes('Zoo Closes')
   ));

   assert.ok(closePillStrip);
   assert.equal(closePillStrip.querySelectorAll('.itinerary-day-open-pill').length, 2);
});

test('day planner renders itinerary arrival and departure times', () => {
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
      }
   );
   const text = allTextFor(planner);

   assert.match(text, /9:45 AM/);
   assert.match(text, /Arrival/);
   assert.match(text, /5:15 PM/);
   assert.match(text, /Departure/);
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
               maximum_duration: 30,
            },
         ],
         wildEncounters: [
            {
               name: 'African Rainforest',
               meeting_spot: 'Wild Encounter - Africa Meeting Spot',
               start_time: '2:00 PM',
               maximum_duration: 45,
            },
         ],
         animals: [
            {
               species: 'African Lion',
               exhibit: 'Africa Savanna',
            },
         ],
         attractions: [
            {
               name: 'Conservation Carousel',
               subtitle: 'Carousels are timeless and fun for all ages!',
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
   assert.match(text, /Unscheduled Items/);
   assert.match(text, /Animals \(1\)/);
   assert.match(text, /African Lion/);
   assert.match(text, /Attractions \(1\)/);
   assert.match(text, /Conservation Carousel/);
   assert.match(text, /Meet The Guardians \(0\)/);
   assert.match(text, /Wild Encounters \(0\)/);
   assert.ok(text.indexOf('Scheduled Items') < text.indexOf('Unscheduled Items'));
});

test('day planner renders zero-count unscheduled sections', () => {
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
   assert.match(text, /Meet The Guardians \(0\)/);
   assert.match(text, /Wild Encounters \(0\)/);
});

test('buildAnimalRows deduplicates species and renders visibility alerts', () => {
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
   ]);

   assert.equal(rows.length, 1);
   assert.equal(
      imageSrcFor(rows[0]),
      'images/details/animals/africa-savanna/african-lion.png'
   );
   assert.equal(textFor(rows[0], '.itin-panel-name'), 'African Lion');
   assert.equal(textFor(rows[0], '.itin-panel-meta'), 'Exhibit: Africa Savanna');
   assert.equal(
      textFor(rows[0], '.itin-panel-alert'),
      'Projected visibility changed from 90% to 60% on your new date.'
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

test('buildGuardiansRows and buildWildRows sort scheduled rows by start time', () => {
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
      talkRows.map((row) => textFor(row, '.itin-panel-name')),
      ['Early Talk', 'Late Talk']
   );
   assert.deepEqual(
      wildRows.map((row) => textFor(row, '.itin-panel-name')),
      ['Morning Encounter', 'Afternoon Encounter']
   );
});
