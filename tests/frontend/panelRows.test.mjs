import assert from 'node:assert/strict';
import { afterEach, beforeEach, test } from 'node:test';

import {
   buildAnimalRows,
   buildAttractionRows,
   buildGuardiansRows,
   buildWildRows,
} from '../../scripts/itinerary/panel/rows.js';
import {
   buildHalfHourSlotStarts,
   formatMinutesAsClockTime,
   parseClockTimeMinutes,
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

function createNode(tagName, className = '', textContent = '') {
   const children = [];
   const listeners = {};

   return {
      tagName,
      className,
      textContent,
      children,
      listeners,
      appendChild(child) {
         children.push(child);
         return child;
      },
      addEventListener(eventName, handler) {
         listeners[eventName] = handler;
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
   };
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
   };
   globalThis.window = {
      open: () => {},
   };
});

afterEach(() => {
   delete globalThis.document;
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
   assert.equal(parseClockTimeMinutes('bad-time'), null);
   assert.equal(formatMinutesAsClockTime(1140), '7:00 PM');
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
         time_of_day: '13:30',
      },
   ]);
   const [wildRow] = buildWildRows([
      {
         name: 'African Rainforest',
         meeting_spot: 'Wild Encounter - Africa Meeting Spot',
         time_of_day: '14:00',
      },
   ]);

   assert.equal(textFor(talkRow, '.itin-panel-name'), 'Amur Tiger');
   assert.equal(
      imageSrcFor(talkRow),
      'images/details/guardians-talks/amur-tiger.png'
   );
   assert.equal(textFor(talkRow, '.itin-panel-meta'), 'Location: Eurasia Wilds');
   assert.equal(textFor(wildRow, '.itin-panel-name'), 'African Rainforest');
   assert.equal(
      imageSrcFor(wildRow),
      'images/details/wild-encounters/african-rainforest.png'
   );
   assert.equal(
      textFor(wildRow, '.itin-panel-meta'),
      'Meeting Spot: Wild Encounter - Africa Meeting Spot'
   );
});
