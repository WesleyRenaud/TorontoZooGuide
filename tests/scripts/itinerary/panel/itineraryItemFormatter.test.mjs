import assert from 'node:assert/strict';
import { test } from 'node:test';

import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerTimelineView } from '../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { DayPlannerTimelineRenderer } from '../../../../scripts/itinerary/panel/dayPlannerTimelineRenderer.js';
import { DayPlannerTimelinePillPlacer } from '../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacer.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { WildEncounterScheduleItemKey } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
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

installPanelRowsTestHooks();

test('Test_FormatPanelHelpers_TestDatesTimesAndItems_ExpectNormalized', () => {
   assert.match(ItineraryItemFormatter.formatISODateLong('2026-06-15'), /June 15, 2026/);
   assert.equal(ItineraryItemFormatter.formatISODateLong('not-a-date'), '');
   assert.equal(ItineraryItemFormatter.formatISODateFull('2026-06-20'), 'Saturday, June 20, 2026');
   assert.equal(ItineraryItemFormatter.formatISODateFull('not-a-date', 'Fallback Date'), 'not-a-date');
   assert.equal(ItineraryItemFormatter.formatClockTime('09:30'), '9:30 AM');
   assert.equal(ItineraryItemFormatter.formatClockTime('09:30:30'), '9:30:30 AM');
   assert.equal(ItineraryItemFormatter.formatClockTime('19:00'), '7:00 PM');
   assert.equal(ItineraryItemFormatter.formatClockTime('', 'Fallback Time'), 'Fallback Time');
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('09:30'), 570);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('09:30:30'), 570.5);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('10:00 AM'), 600);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('10:00:30 AM'), 600.5);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('1:30 PM'), 810);
   assert.equal(DayPlannerScheduleController.parseClockTimeMinutes('bad-time'), null);
   assert.equal(DayPlannerScheduleController.formatMinutesAsClockTime(1140), '7:00 PM');
   assert.deepEqual(DayPlannerScheduleController.buildArrivalTimeBounds({
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
   assert.deepEqual(DayPlannerScheduleController.buildArrivalTimeBounds({
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
   assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('9:00 AM', DayPlannerScheduleController.buildArrivalTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   })), true);
   assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('8:45 AM', DayPlannerScheduleController.buildArrivalTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   })), false);
   assert.equal(
      DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(
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
      DayPlannerScheduleController.buildHalfHourSlotStarts(
         DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(
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
   assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('6:00 PM', DayPlannerScheduleController.buildArrivalTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   })), true);
   assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('6:15 PM', DayPlannerScheduleController.buildArrivalTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   })), false);
   assert.equal(DayPlannerScheduleController.isArrivalTimeWithinBounds('', DayPlannerScheduleController.buildArrivalTimeBounds({
      openTime: '09:30',
      lastAdmissionTime: '17:00',
   })), true);
   assert.deepEqual(DayPlannerScheduleController.buildDepartureTimeBounds({
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
   assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('9:30 AM', DayPlannerScheduleController.buildDepartureTimeBounds({
      openTime: '09:30',
      closeTime: '18:00',
   })), true);
   assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('9:00 AM', DayPlannerScheduleController.buildDepartureTimeBounds({
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      closeTime: '19:00',
   })), false);
   assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('6:00 PM', DayPlannerScheduleController.buildDepartureTimeBounds({
      openTime: '09:30',
      closeTime: '18:00',
   })), true);
   assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('6:15 PM', DayPlannerScheduleController.buildDepartureTimeBounds({
      openTime: '09:30',
      closeTime: '18:00',
   })), false);
   assert.equal(DayPlannerScheduleController.isDepartureTimeWithinBounds('', DayPlannerScheduleController.buildDepartureTimeBounds({
      openTime: '09:30',
      closeTime: '18:00',
   })), true);
   assert.equal(DayPlannerScheduleController.areItineraryScheduleTimesOrdered('9:30 AM', '5:00 PM'), true);
   assert.equal(DayPlannerScheduleController.areItineraryScheduleTimesOrdered('5:00 PM', '5:00 PM'), false);
   assert.equal(DayPlannerScheduleController.areItineraryScheduleTimesOrdered('5:15 PM', '5:00 PM'), false);
   assert.equal(DayPlannerScheduleController.areItineraryScheduleTimesOrdered('', '5:00 PM'), true);
   assert.equal(DayPlannerScheduleController.resolveDepartureTimeValidationError(
      '9:30 AM',
      DayPlannerScheduleController.buildDepartureTimeBounds({ openTime: '09:30', closeTime: '18:00' }),
      '9:30 AM',
      {
         departureTimeInvalid: 'hours',
         departureTimeAfterArrivalInvalid: 'order',
      }
   ), 'order');
   assert.equal(DayPlannerScheduleController.resolveArrivalTimeValidationError(
      '5:00 PM',
      DayPlannerScheduleController.buildArrivalTimeBounds({
         openTime: '09:30',
         lastAdmissionTime: '17:00',
      }),
      '5:00 PM',
      {
         arrivalTimeInvalid: 'hours',
         timeOrderInvalid: 'order',
      }
   ), 'order');
   assert.deepEqual(DayPlannerScheduleController.buildHalfHourSlotStarts(570, 720), [
      570,
      600,
      630,
      660,
      690,
   ]);
   assert.equal(DayPlannerTimelineView.timelineSlotRowHeightFraction(2), 2 / 30);
   assert.equal(DayPlannerTimelineView.timelineSlotRowHeightFraction(15), 0.5);
   assert.equal(DayPlannerTimelineView.timelineSlotRowHeightFraction(30), 1);
   assert.equal(DayPlannerTimelineView.timelineSlotRowHeightFraction(0), 1);
   assert.equal(DayPlannerTimelineView.timelineSlotRowHeightFraction(null), 1);
   assert.deepEqual(ItineraryItemFormatter.normalizeAnimal({
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
   assert.equal(ItineraryItemFormatter.normalizeAttraction({
      name: '  Conservation Carousel  ',
      info_link: '  https://www.torontozoo.com/tickets/carousel  ',
      region: '  Front Courtyard  ',
   }).infoLink, 'https://www.torontozoo.com/tickets/carousel');
   assert.deepEqual(
      ItineraryItemFormatter.normalizeAttraction({
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
   assert.equal(ItineraryItemFormatter.normalizeTalk({ name: '  Amur Tiger  ' }).name, 'Amur Tiger');
   assert.deepEqual(
      ItineraryItemFormatter.normalizeTalk({
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
   assert.deepEqual(ItineraryItemFormatter.normalizeTalk({ name: 'Unmapped Talk' }).linked_animals, []);
   assert.equal(ItineraryItemFormatter.normalizeWild({ name: '  African Rainforest  ' }).name, 'African Rainforest');
   assert.equal(ItineraryItemFormatter.normalizeNonNegativeNumber(-1), null);
   assert.equal(ItineraryItemFormatter.normalizeNonNegativeNumber('4'), 4);
   assert.equal(ItineraryItemFormatter.parseDurationMinutes(''), null);
   assert.equal(ItineraryItemFormatter.parseDurationMinutes('0'), null);
   assert.equal(ItineraryItemFormatter.parseDurationMinutes('abc'), null);
   assert.equal(ItineraryItemFormatter.parseDurationMinutes('25.4'), 25);
   assert.equal(ItineraryItemFormatter.formatClockTime('not-a-clock'), 'not-a-clock');
   assert.deepEqual(
      ItineraryItemFormatter.normalizeTransportation({
         name: 'Zoomobile',
         legs: [{
            from_station: '  A  ',
            to_station: '  B  ',
            start_time: ' 10:00 AM ',
            end_time: ' 10:15 AM ',
         }],
         stations: [{
            name: '  Main Station  ',
            transportation: '  Zoomobile  ',
            role: ' hub ',
            type: ' stop ',
            description: '  Board here  ',
            x_coord: '12',
            y_coord: '34',
         }],
      }).legs,
      [{
         from_station: 'A',
         to_station: 'B',
         start_time: '10:00 AM',
         end_time: '10:15 AM',
      }]
   );
   assert.deepEqual(
      ItineraryItemFormatter.normalizeGuardiansTalkForSave({
         name: '  Lion Talk  ',
         start_time: ' 11:00 AM ',
         end_time: ' 11:20 AM ',
         location: 'ignored',
      }),
      {
         name: 'Lion Talk',
         start_time: '11:00 AM',
         end_time: '11:20 AM',
      }
   );
   assert.deepEqual(ItineraryItemFormatter.normalizeItineraryNamesForSave(null), []);
   assert.deepEqual(
      ItineraryItemFormatter.normalizeItineraryNamesForSave(['  Carousel  ', '']),
      ['Carousel']
   );
   const morningsInMalaysiaRow = {
      name: 'Mornings in Malaysia',
      start_time: '8:45 AM',
      end_time: '9:45 AM',
   };
   const morningsInMalaysiaWire = WildEncounterScheduleItemKey.fromRow(morningsInMalaysiaRow).toWire();
   assert.equal(
      ItineraryItemFormatter.normalizeWildEncounterForSave(morningsInMalaysiaWire),
      morningsInMalaysiaWire
   );
   assert.equal(ItineraryItemFormatter.normalizeWildEncounterForSave(''), '');
   assert.equal(
      ItineraryItemFormatter.normalizeWildEncounterForSave(morningsInMalaysiaRow),
      morningsInMalaysiaWire
   );
   assert.deepEqual(ItineraryItemFormatter.normalizeWildEncounterListForSave(null), []);
   assert.deepEqual(
      ItineraryItemFormatter.normalizeWildEncounterListForSave([
         morningsInMalaysiaWire,
         '',
      ]),
      [morningsInMalaysiaWire]
   );
});

test('Test_FindTimelineAnchorSlot_TestPrecedingHalfHour_ExpectAnchored', () => {
   const slotStarts = DayPlannerScheduleController.buildHalfHourSlotStarts(570, 1140);
   const markersByAnchor = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
      [
         {
            startMinutes: DayPlannerScheduleController.parseClockTimeMinutes('11:35'),
            label: 'Arrival',
            kind: TEST_ITINERARY_CONFIG.visitBoundaryEventTypes.arrival,
         },
      ],
      slotStarts,
      1140
   );

   assert.equal(DayPlannerTimelineRenderer.findTimelineAnchorSlot(DayPlannerScheduleController.parseClockTimeMinutes('11:35'), slotStarts), 690);
   assert.equal(DayPlannerTimelineRenderer.computeMarkerOffsetFraction(695, 690, 720), 1 / 6);
   assert.deepEqual(markersByAnchor.get(690), [{
      label: 'Arrival',
      offsetFraction: 1 / 6,
      kind: 'arrival',
   }]);
});
test('Test_ComputeStripHorizontalOffsetIndex_TestOverlappingStrips_ExpectShifted', () => {
   const pointPillVerticalSpanFraction = (
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );

   assert.equal(
      DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex([], 0.5, pointPillVerticalSpanFraction),
      0
   );
   assert.equal(DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex([
      { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
   ], 0.67, pointPillVerticalSpanFraction), 1);
   assert.equal(DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex([
      { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
      { offsetFraction: 0.67, horizontalOffsetIndex: 1 },
   ], 0.6, pointPillVerticalSpanFraction), 2);
});

test('Test_ComputeTimelineHorizontalOffsetIndex_TestOverlappingPlacements_ExpectShifted', () => {
   assert.equal(DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex([], 0.5, 0.5), 0);
   assert.equal(DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex([
      { offsetFraction: 0.5, durationFraction: 0.5, horizontalOffsetIndex: 0 },
   ], 0.67, 0.5), 1);
});
