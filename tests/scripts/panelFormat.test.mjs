import assert from 'node:assert/strict';
import { test } from 'node:test';

import {
   TIMELINE_POINT_PILL_HEIGHT_PX,
   TIMELINE_SLOT_HEIGHT_PX,
} from '../../scripts/shared/constants.js';
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
   resolveDayPlannerTimelineStartMinutes,
   resolveDepartureTimeValidationError,
} from '../../scripts/itinerary/panel/dayPlannerSchedule.js';
import { timelineSlotRowHeightFraction } from '../../scripts/itinerary/panel/components/dayPlannerTimeline.js';
import { DayPlannerTimelineMarkers } from '../../scripts/itinerary/panel/dayPlannerTimelineMarkers.js';
import { DayPlannerTimelinePillPlacement } from '../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacement.js';
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

test.describe('itinerary panel format and schedule', () => {
   installPanelRowsTestHooks();

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
      assert.equal(
         resolveDayPlannerTimelineStartMinutes(
            { openTime: '09:30', closeTime: '19:00' },
            {
               arrivalTime: '9:30 AM',
               wildEncounters: [
                  {
                     name: 'Mornings in Malaysia',
                     start_time: '8:45 AM',
                     end_time: '9:45 AM',
                  },
               ],
            }
         ),
         525
      );
      assert.deepEqual(
         buildHalfHourSlotStarts(
            resolveDayPlannerTimelineStartMinutes(
               { openTime: '09:30', closeTime: '19:00' },
               {
                  wildEncounters: [
                     {
                        name: 'Mornings in Malaysia',
                        start_time: '8:45 AM',
                        end_time: '9:45 AM',
                     },
                  ],
               }
            ),
            1140
         ).slice(0, 3),
         [525, 540, 570]
      );
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
            timeOrderInvalid: 'order',
         }
      ), 'order');
      assert.deepEqual(buildHalfHourSlotStarts(570, 720), [
         570,
         600,
         630,
         660,
         690,
      ]);
      assert.equal(timelineSlotRowHeightFraction(2), 2 / 30);
      assert.equal(timelineSlotRowHeightFraction(15), 0.5);
      assert.equal(timelineSlotRowHeightFraction(30), 1);
      assert.equal(timelineSlotRowHeightFraction(0), 1);
      assert.equal(timelineSlotRowHeightFraction(null), 1);
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
         region: '  Front Courtyard  ',
      }).infoLink, 'https://www.torontozoo.com/tickets/carousel');
      assert.deepEqual(
         normalizeAttraction({
            name: 'Zoomobile',
            region: 'Front Courtyard',
         }),
         {
            name: 'Zoomobile',
            subtitle: '',
            region: 'Front Courtyard',
            location: '',
            price: '',
            open_time: null,
            close_time: null,
            infoLink: null,
            removalReason: null,
         }
      );
      assert.equal(normalizeTalk({ name: '  Amur Tiger  ' }).name, 'Amur Tiger');
      assert.deepEqual(
         normalizeTalk({
            name: 'New World Primates',
            linked_animals: [
               { species: '  Golden Lion Tamarin  ', exhibit: '  Americas Pavilion  ' },
               { species: '', exhibit: 'Americas Pavilion' },
               { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
            ],
         }).linked_animals,
         [
            { species: 'Golden Lion Tamarin', exhibit: 'Americas Pavilion' },
            { species: 'Two-Toed Sloth', exhibit: 'Americas Pavilion' },
         ]
      );
      assert.deepEqual(normalizeTalk({ name: 'Unmapped Talk' }).linked_animals, []);
      assert.equal(normalizeWild({ name: '  African Rainforest  ' }).name, 'African Rainforest');
   });
   
   test('timeline markers anchor to the preceding half-hour slot', () => {
      const slotStarts = buildHalfHourSlotStarts(570, 1140);
      const markersByAnchor = DayPlannerTimelineMarkers.buildMarkersByAnchorSlot(
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
   
      assert.equal(DayPlannerTimelineMarkers.findTimelineAnchorSlot(parseClockTimeMinutes('11:35'), slotStarts), 690);
      assert.equal(DayPlannerTimelineMarkers.computeMarkerOffsetFraction(695, 690, 720), 1 / 6);
      assert.deepEqual(markersByAnchor.get(690), [{
         label: 'Arrival',
         offsetFraction: 1 / 6,
         kind: 'arrival',
      }]);
   });
   test('DayPlannerTimelinePillPlacement.computeStripHorizontalOffsetIndex shifts later overlapping strips', () => {
      const pointPillVerticalSpanFraction = (
         TIMELINE_POINT_PILL_HEIGHT_PX / TIMELINE_SLOT_HEIGHT_PX
      );
   
      assert.equal(
         DayPlannerTimelinePillPlacement.computeStripHorizontalOffsetIndex([], 0.5, pointPillVerticalSpanFraction),
         0
      );
      assert.equal(DayPlannerTimelinePillPlacement.computeStripHorizontalOffsetIndex([
         { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
      ], 0.67, pointPillVerticalSpanFraction), 1);
      assert.equal(DayPlannerTimelinePillPlacement.computeStripHorizontalOffsetIndex([
         { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
         { offsetFraction: 0.67, horizontalOffsetIndex: 1 },
      ], 0.6, pointPillVerticalSpanFraction), 2);
   });
   
   test('DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex shifts later overlapping placements', () => {
      assert.equal(DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex([], 0.5, 0.5), 0);
      assert.equal(DayPlannerTimelinePillPlacement.computeTimelineHorizontalOffsetIndex([
         { offsetFraction: 0.5, durationFraction: 0.5, horizontalOffsetIndex: 0 },
      ], 0.67, 0.5), 1);
   });
});
