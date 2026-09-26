import assert from 'node:assert/strict';
import { test } from 'node:test';

import { DayPlannerScheduleController } from '../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerTimelineRenderer } from '../../../../scripts/itinerary/panel/dayPlannerTimelineRenderer.js';
import { DayPlannerTimelineView } from '../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { DayPlannerTimelinePillPlacer } from '../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillPlacer.js';
import { ItineraryItemFormatter } from '../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { WildEncounterScheduleItemKey } from '../../../../scripts/itinerary/selectors/wildEncounterSelector/wildEncounterScheduleItemKey.js';
import { TimelineLayoutConstants } from '../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../scripts/shared/zooClockTimeHelper.js';
import { Position } from '../../../../scripts/shared/enums/position.js';
import { ValueNormalizer } from '../../../../scripts/api/valueNormalizer.js';
import {
   TEST_ITINERARY_CONFIG,
   installPanelRowsTestHooks,
} from '../../helpers/panelRowsTestSetup.mjs';

installPanelRowsTestHooks();


test('Test_FormatISODateLong_TestValidDate_ExpectLongDate', () => {
   const iso = '2026-06-15';

   const formatted = ItineraryItemFormatter.formatISODateLong(iso);

   assert.match(formatted, /June 15, 2026/);
});


test('Test_FormatISODateLong_TestInvalidDate_ExpectEmpty', () => {
   const iso = 'not-a-date';

   const formatted = ItineraryItemFormatter.formatISODateLong(iso);

   assert.equal(formatted, '');
});


test('Test_FormatISODateFull_TestValidDate_ExpectFullDate', () => {
   const iso = '2026-06-20';

   const formatted = ItineraryItemFormatter.formatISODateFull(iso);

   assert.equal(
      formatted,
      new Intl.DateTimeFormat('en-CA', {
         weekday: 'long',
         month: 'long',
         day: 'numeric',
         year: 'numeric',
      }).format(new Date(2026, 6 - 1, 20))
   );
});


test('Test_FormatISODateFull_TestInvalidDate_ExpectFallbackInput', () => {
   const iso = 'not-a-date';
   const fallback = 'Fallback Date';

   const formatted = ItineraryItemFormatter.formatISODateFull(iso, fallback);

   assert.equal(formatted, iso);
});


test('Test_FormatClockTime_TestMorning_ExpectDisplayTime', () => {
   const clockTime = '09:30';

   const formatted = ItineraryItemFormatter.formatClockTime(clockTime);

   assert.equal(formatted, ZooClockTimeHelper.formatClockTime(clockTime));
});


test('Test_FormatClockTime_TestWithSeconds_ExpectDisplayTime', () => {
   const clockTime = '09:30:30';

   const formatted = ItineraryItemFormatter.formatClockTime(clockTime);

   assert.equal(formatted, ZooClockTimeHelper.formatClockTime(clockTime));
});


test('Test_FormatClockTime_TestEvening_ExpectDisplayTime', () => {
   const clockTime = '19:00';

   const formatted = ItineraryItemFormatter.formatClockTime(clockTime);

   assert.equal(formatted, ZooClockTimeHelper.formatClockTime(clockTime));
});


test('Test_FormatClockTime_TestEmpty_ExpectFallback', () => {
   const clockTime = '';
   const fallback = 'Fallback Time';

   const formatted = ItineraryItemFormatter.formatClockTime(clockTime, fallback);

   assert.equal(formatted, fallback);
});


test('Test_FormatClockTime_TestInvalid_ExpectInput', () => {
   const clockTime = 'not-a-clock';

   const formatted = ItineraryItemFormatter.formatClockTime(clockTime);

   assert.equal(formatted, clockTime);
});


test('Test_ParseClockTimeMinutes_TestHoursMinutes_ExpectMinutes', () => {
   const clockTime = '09:30';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 9 * 60 + 30);
});


test('Test_ParseClockTimeMinutes_TestHoursMinutesSeconds_ExpectFractionalMinutes', () => {
   const clockTime = '09:30:30';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 9 * 60 + 30.5);
});


test('Test_ParseClockTimeMinutes_TestMorningDisplay_ExpectMinutes', () => {
   const clockTime = '10:00 AM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 10 * 60);
});


test('Test_ParseClockTimeMinutes_TestMorningSeconds_ExpectFractionalMinutes', () => {
   const clockTime = '10:00:30 AM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 10 * 60 + 0.5);
});


test('Test_ParseClockTimeMinutes_TestAfternoon_ExpectMinutes', () => {
   const clockTime = '1:30 PM';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, 13 * 60 + 30);
});


test('Test_ParseClockTimeMinutes_TestInvalid_ExpectNull', () => {
   const clockTime = 'bad-time';

   const minutes = DayPlannerScheduleController.parseClockTimeMinutes(clockTime);

   assert.equal(minutes, null);
});


test('Test_FormatMinutesAsClockTime_TestEvening_ExpectDisplayTime', () => {
   const minutes = 19 * 60;

   const clockTime = DayPlannerScheduleController.formatMinutesAsClockTime(minutes);

   assert.equal(clockTime, ZooClockTimeHelper.formatClockTime('19:00'));
});


test('Test_BuildArrivalTimeBounds_TestEarlyAdmission_ExpectBounds', () => {
   const earlyAdmissionTime = '09:00';
   const lastAdmissionTime = '18:00';
   const hours = {
      earlyAdmissionTime,
      openTime: '09:30',
      lastAdmissionTime,
   };

   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);

   assert.deepEqual(bounds, {
      minMinutes: DayPlannerScheduleController.parseClockTimeMinutes(earlyAdmissionTime),
      maxMinutes: DayPlannerScheduleController.parseClockTimeMinutes(lastAdmissionTime),
      minScheduleTime: earlyAdmissionTime,
      maxScheduleTime: lastAdmissionTime,
      minClockTime: ZooClockTimeHelper.formatClockTime(earlyAdmissionTime),
      maxClockTime: ZooClockTimeHelper.formatClockTime(lastAdmissionTime),
   });
});


test('Test_BuildArrivalTimeBounds_TestOpenAndLastAdmission_ExpectBounds', () => {
   const openTime = '09:30';
   const lastAdmissionTime = '17:00';
   const hours = { openTime, lastAdmissionTime };

   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);

   assert.deepEqual(bounds, {
      minMinutes: DayPlannerScheduleController.parseClockTimeMinutes(openTime),
      maxMinutes: DayPlannerScheduleController.parseClockTimeMinutes(lastAdmissionTime),
      minScheduleTime: openTime,
      maxScheduleTime: lastAdmissionTime,
      minClockTime: ZooClockTimeHelper.formatClockTime(openTime),
      maxClockTime: ZooClockTimeHelper.formatClockTime(lastAdmissionTime),
   });
});


test('Test_IsArrivalTimeWithinBounds_TestAtEarlyAdmission_ExpectTrue', () => {
   const hours = {
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);
   const arrivalTime = ZooClockTimeHelper.formatClockTime(hours.earlyAdmissionTime);

   const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds(arrivalTime, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsArrivalTimeWithinBounds_TestBeforeEarlyAdmission_ExpectFalse', () => {
   const hours = {
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);
   const arrivalTime = '8:45 AM';

   const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds(arrivalTime, bounds);

   assert.equal(isWithin, false);
});


test('Test_IsArrivalTimeWithinBounds_TestAtLastAdmission_ExpectTrue', () => {
   const hours = {
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);
   const arrivalTime = ZooClockTimeHelper.formatClockTime(hours.lastAdmissionTime);

   const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds(arrivalTime, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsArrivalTimeWithinBounds_TestAfterLastAdmission_ExpectFalse', () => {
   const hours = {
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      lastAdmissionTime: '18:00',
   };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);
   const arrivalTime = '6:15 PM';

   const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds(arrivalTime, bounds);

   assert.equal(isWithin, false);
});


test('Test_IsArrivalTimeWithinBounds_TestBlank_ExpectTrue', () => {
   const hours = {
      openTime: '09:30',
      lastAdmissionTime: '17:00',
   };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);

   const isWithin = DayPlannerScheduleController.isArrivalTimeWithinBounds('', bounds);

   assert.equal(isWithin, true);
});


test('Test_ResolveDayPlannerTimelineStartMinutes_TestEarlierEncounter_ExpectEncounter', () => {
   const encounterTime = '8:45 AM';
   const hours = { openTime: '09:30', closeTime: '19:00' };
   const itinerary = {
      arrivalTime: '9:30 AM',
      wildEncounters: [{
         name: 'Mornings in Malaysia',
         start_time: encounterTime,
         end_time: '9:45 AM',
      }],
   };

   const minutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(hours, itinerary);

   assert.equal(minutes, DayPlannerScheduleController.parseClockTimeMinutes(encounterTime));
});


test('Test_BuildHalfHourSlotStarts_TestResolvedStart_ExpectLeadingSlots', () => {
   const encounterTime = '8:45 AM';
   const closeTime = '19:00';
   const startMinutes = DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes(
      { openTime: '09:30', closeTime },
      {
         wildEncounters: [{
            name: 'Mornings in Malaysia',
            start_time: encounterTime,
            end_time: '9:45 AM',
         }],
      }
   );
   const endMinutes = DayPlannerScheduleController.parseClockTimeMinutes(closeTime);

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(startMinutes, endMinutes);

   assert.deepEqual(slots.slice(0, 3), [
      startMinutes,
      9 * 60,
      9 * 60 + 30,
   ]);
});


test('Test_BuildDepartureTimeBounds_TestHours_ExpectBounds', () => {
   const openTime = '09:30';
   const closeTime = '18:00';
   const hours = { openTime, closeTime };

   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);

   assert.deepEqual(bounds, {
      minMinutes: DayPlannerScheduleController.parseClockTimeMinutes(openTime),
      maxMinutes: DayPlannerScheduleController.parseClockTimeMinutes(closeTime),
      minScheduleTime: openTime,
      maxScheduleTime: closeTime,
      minClockTime: ZooClockTimeHelper.formatClockTime(openTime),
      maxClockTime: ZooClockTimeHelper.formatClockTime(closeTime),
   });
});


test('Test_IsDepartureTimeWithinBounds_TestAtOpen_ExpectTrue', () => {
   const hours = { openTime: '09:30', closeTime: '18:00' };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);
   const departureTime = ZooClockTimeHelper.formatClockTime(hours.openTime);

   const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds(departureTime, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsDepartureTimeWithinBounds_TestBeforeOpen_ExpectFalse', () => {
   const hours = {
      earlyAdmissionTime: '09:00',
      openTime: '09:30',
      closeTime: '19:00',
   };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);
   const departureTime = '9:00 AM';

   const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds(departureTime, bounds);

   assert.equal(isWithin, false);
});


test('Test_IsDepartureTimeWithinBounds_TestAtClose_ExpectTrue', () => {
   const hours = { openTime: '09:30', closeTime: '18:00' };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);
   const departureTime = ZooClockTimeHelper.formatClockTime(hours.closeTime);

   const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds(departureTime, bounds);

   assert.equal(isWithin, true);
});


test('Test_IsDepartureTimeWithinBounds_TestAfterClose_ExpectFalse', () => {
   const hours = { openTime: '09:30', closeTime: '18:00' };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);
   const departureTime = '6:15 PM';

   const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds(departureTime, bounds);

   assert.equal(isWithin, false);
});


test('Test_IsDepartureTimeWithinBounds_TestBlank_ExpectTrue', () => {
   const hours = { openTime: '09:30', closeTime: '18:00' };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);

   const isWithin = DayPlannerScheduleController.isDepartureTimeWithinBounds('', bounds);

   assert.equal(isWithin, true);
});


test('Test_AreItineraryScheduleTimesOrdered_TestArrivalBeforeDeparture_ExpectTrue', () => {
   const arrivalTime = '9:30 AM';
   const departureTime = '5:00 PM';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, true);
});


test('Test_AreItineraryScheduleTimesOrdered_TestSameTime_ExpectFalse', () => {
   const clockTime = '5:00 PM';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      clockTime,
      clockTime
   );

   assert.equal(isOrdered, false);
});


test('Test_AreItineraryScheduleTimesOrdered_TestArrivalAfterDeparture_ExpectFalse', () => {
   const arrivalTime = '5:15 PM';
   const departureTime = '5:00 PM';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, false);
});


test('Test_AreItineraryScheduleTimesOrdered_TestBlankArrival_ExpectTrue', () => {
   const arrivalTime = '';
   const departureTime = '5:00 PM';

   const isOrdered = DayPlannerScheduleController.areItineraryScheduleTimesOrdered(
      arrivalTime,
      departureTime
   );

   assert.equal(isOrdered, true);
});


test('Test_ResolveDepartureTimeValidationError_TestSameAsArrival_ExpectOrder', () => {
   const clockTime = '9:30 AM';
   const hours = { openTime: '09:30', closeTime: '18:00' };
   const bounds = DayPlannerScheduleController.buildDepartureTimeBounds(hours);
   const messages = {
      departureTimeInvalid: 'hours',
      departureTimeAfterArrivalInvalid: 'order',
   };

   const error = DayPlannerScheduleController.resolveDepartureTimeValidationError(
      clockTime,
      bounds,
      clockTime,
      messages
   );

   assert.equal(error, messages.departureTimeAfterArrivalInvalid);
});


test('Test_ResolveArrivalTimeValidationError_TestSameAsDeparture_ExpectOrder', () => {
   const clockTime = '5:00 PM';
   const hours = { openTime: '09:30', lastAdmissionTime: '17:00' };
   const bounds = DayPlannerScheduleController.buildArrivalTimeBounds(hours);
   const messages = {
      arrivalTimeInvalid: 'hours',
      timeOrderInvalid: 'order',
   };

   const error = DayPlannerScheduleController.resolveArrivalTimeValidationError(
      clockTime,
      bounds,
      clockTime,
      messages
   );

   assert.equal(error, messages.timeOrderInvalid);
});


test('Test_BuildHalfHourSlotStarts_TestMorningRange_ExpectSlots', () => {
   const startMinutes = 9 * 60 + 30;
   const endMinutes = 12 * 60;

   const slots = DayPlannerScheduleController.buildHalfHourSlotStarts(startMinutes, endMinutes);

   assert.deepEqual(slots, [
      startMinutes,
      startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
      10 * 60 + 30,
      11 * 60,
      11 * 60 + 30,
   ]);
});


test('Test_TimelineSlotRowHeightFraction_TestTwoMinutes_ExpectFraction', () => {
   const slotSpanMinutes = 2;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, slotSpanMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);
});


test('Test_TimelineSlotRowHeightFraction_TestFifteenMinutes_ExpectHalf', () => {
   const slotSpanMinutes = 15;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, slotSpanMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);
});


test('Test_TimelineSlotRowHeightFraction_TestFullSlot_ExpectOne', () => {
   const slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, 1);
});


test('Test_TimelineSlotRowHeightFraction_TestZero_ExpectOne', () => {
   const slotSpanMinutes = 0;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, 1);
});


test('Test_TimelineSlotRowHeightFraction_TestNull_ExpectOne', () => {
   const slotSpanMinutes = null;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, 1);
});


test('Test_NormalizeAnimal_TestWhitespace_ExpectTrimmed', () => {
   const species = 'African Lion';
   const exhibit = 'Africa Savanna';
   const likelihoodBefore = '0.9';
   const likelihoodAfter = '60';
   const animal = {
      species: `  ${species}  `,
      exhibit: `  ${exhibit}  `,
      likelihoodBefore,
      likelihoodAfter,
   };

   const normalized = ItineraryItemFormatter.normalizeAnimal(animal);

   assert.deepEqual(normalized, {
      species,
      exhibit,
      link: null,
      removalReason: null,
      likelihoodBefore: ValueNormalizer.normalizeNumber(likelihoodBefore),
      likelihoodAfter: ValueNormalizer.normalizeNumber(likelihoodAfter),
   });
});


test('Test_NormalizeAttraction_TestInfoLink_ExpectTrimmed', () => {
   const name = 'Conservation Carousel';
   const infoLink = 'https://www.torontozoo.com/tickets/carousel';
   const region = 'Front Courtyard';
   const attraction = {
      name: `  ${name}  `,
      info_link: `  ${infoLink}  `,
      region: `  ${region}  `,
   };

   const normalized = ItineraryItemFormatter.normalizeAttraction(attraction);

   assert.equal(normalized.infoLink, infoLink);
});


test('Test_NormalizeAttraction_TestDefaults_ExpectEmptyFields', () => {
   const name = 'Zoomobile';
   const region = 'Front Courtyard';
   const attraction = { name, region };

   const normalized = ItineraryItemFormatter.normalizeAttraction(attraction);

   assert.deepEqual(normalized, {
      name,
      subtitle: '',
      region,
      location: '',
      price: '',
      open_time: null,
      close_time: null,
      infoLink: null,
      removalReason: null,
   });
});


test('Test_NormalizeTalk_TestWhitespace_ExpectTrimmedName', () => {
   const name = 'Amur Tiger';
   const talk = { name: `  ${name}  ` };

   const normalized = ItineraryItemFormatter.normalizeTalk(talk);

   assert.equal(normalized.name, name);
});


test('Test_NormalizeTalk_TestLinkedAnimals_ExpectTrimmedNamed', () => {
   const firstSpecies = 'Golden Lion Tamarin';
   const exhibit = 'Americas Pavilion';
   const secondSpecies = 'Two-Toed Sloth';
   const talk = {
      name: 'New World Primates',
      linked_animals: [
         { species: `  ${firstSpecies}  `, exhibit: `  ${exhibit}  ` },
         { species: '', exhibit },
         { species: secondSpecies, exhibit },
      ],
   };

   const normalized = ItineraryItemFormatter.normalizeTalk(talk);

   assert.deepEqual(normalized.linked_animals, [
      { species: firstSpecies, exhibit },
      { species: secondSpecies, exhibit },
   ]);
});


test('Test_NormalizeTalk_TestUnmapped_ExpectEmptyLinkedAnimals', () => {
   const talk = { name: 'Unmapped Talk' };

   const normalized = ItineraryItemFormatter.normalizeTalk(talk);

   assert.deepEqual(normalized.linked_animals, []);
});


test('Test_NormalizeWild_TestWhitespace_ExpectTrimmedName', () => {
   const name = 'African Rainforest';
   const encounter = { name: `  ${name}  ` };

   const normalized = ItineraryItemFormatter.normalizeWild(encounter);

   assert.equal(normalized.name, name);
});


test('Test_NormalizeNonNegativeNumber_TestNegative_ExpectNull', () => {
   const value = -1;

   const number = ItineraryItemFormatter.normalizeNonNegativeNumber(value);

   assert.equal(number, null);
});


test('Test_NormalizeNonNegativeNumber_TestNumericString_ExpectNumber', () => {
   const value = '4';

   const number = ItineraryItemFormatter.normalizeNonNegativeNumber(value);

   assert.equal(number, Number(value));
});


test('Test_ParseDurationMinutes_TestEmpty_ExpectNull', () => {
   const value = '';

   const minutes = ItineraryItemFormatter.parseDurationMinutes(value);

   assert.equal(minutes, null);
});


test('Test_ParseDurationMinutes_TestZero_ExpectNull', () => {
   const value = '0';

   const minutes = ItineraryItemFormatter.parseDurationMinutes(value);

   assert.equal(minutes, null);
});


test('Test_ParseDurationMinutes_TestNonNumeric_ExpectNull', () => {
   const value = 'abc';

   const minutes = ItineraryItemFormatter.parseDurationMinutes(value);

   assert.equal(minutes, null);
});


test('Test_ParseDurationMinutes_TestDecimal_ExpectRounded', () => {
   const value = '25.4';

   const minutes = ItineraryItemFormatter.parseDurationMinutes(value);

   assert.equal(minutes, Math.round(Number(value)));
});


test('Test_NormalizeTransportation_TestLegs_ExpectTrimmed', () => {
   const fromStation = 'A';
   const toStation = 'B';
   const startTime = '10:00 AM';
   const endTime = '10:15 AM';
   const transportation = {
      name: 'Zoomobile',
      legs: [{
         from_station: `  ${fromStation}  `,
         to_station: `  ${toStation}  `,
         start_time: ` ${startTime} `,
         end_time: ` ${endTime} `,
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
   };

   const normalized = ItineraryItemFormatter.normalizeTransportation(transportation);

   assert.deepEqual(normalized.legs, [{
      from_station: fromStation,
      to_station: toStation,
      start_time: startTime,
      end_time: endTime,
   }]);
});


test('Test_NormalizeGuardiansTalkForSave_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Lion Talk';
   const startTime = '11:00 AM';
   const endTime = '11:20 AM';
   const talk = {
      name: `  ${name}  `,
      start_time: ` ${startTime} `,
      end_time: ` ${endTime} `,
      location: 'ignored',
   };

   const saved = ItineraryItemFormatter.normalizeGuardiansTalkForSave(talk);

   assert.deepEqual(saved, {
      name,
      start_time: startTime,
      end_time: endTime,
   });
});


test('Test_NormalizeItineraryNamesForSave_TestNull_ExpectEmpty', () => {
   const items = null;

   const names = ItineraryItemFormatter.normalizeItineraryNamesForSave(items);

   assert.deepEqual(names, []);
});


test('Test_NormalizeItineraryNamesForSave_TestWhitespace_ExpectTrimmed', () => {
   const name = 'Carousel';
   const items = [`  ${name}  `, ''];

   const names = ItineraryItemFormatter.normalizeItineraryNamesForSave(items);

   assert.deepEqual(names, [name]);
});


test('Test_NormalizeWildEncounterForSave_TestWire_ExpectSame', () => {
   const morningsInMalaysiaRow = {
      name: 'Mornings in Malaysia',
      start_time: '8:45 AM',
      end_time: '9:45 AM',
   };
   const wire = WildEncounterScheduleItemKey.fromRow(morningsInMalaysiaRow).toWire();

   const saved = ItineraryItemFormatter.normalizeWildEncounterForSave(wire);

   assert.equal(saved, wire);
});


test('Test_NormalizeWildEncounterForSave_TestEmpty_ExpectEmpty', () => {
   const value = '';

   const saved = ItineraryItemFormatter.normalizeWildEncounterForSave(value);

   assert.equal(saved, value);
});


test('Test_NormalizeWildEncounterForSave_TestRow_ExpectWire', () => {
   const morningsInMalaysiaRow = {
      name: 'Mornings in Malaysia',
      start_time: '8:45 AM',
      end_time: '9:45 AM',
   };

   const saved = ItineraryItemFormatter.normalizeWildEncounterForSave(morningsInMalaysiaRow);

   assert.equal(saved, WildEncounterScheduleItemKey.fromRow(morningsInMalaysiaRow).toWire());
});


test('Test_NormalizeWildEncounterListForSave_TestNull_ExpectEmpty', () => {
   const items = null;

   const saved = ItineraryItemFormatter.normalizeWildEncounterListForSave(items);

   assert.deepEqual(saved, []);
});


test('Test_NormalizeWildEncounterListForSave_TestWireAndBlank_ExpectWire', () => {
   const morningsInMalaysiaRow = {
      name: 'Mornings in Malaysia',
      start_time: '8:45 AM',
      end_time: '9:45 AM',
   };
   const wire = WildEncounterScheduleItemKey.fromRow(morningsInMalaysiaRow).toWire();

   const saved = ItineraryItemFormatter.normalizeWildEncounterListForSave([wire, '']);

   assert.deepEqual(saved, [wire]);
});


test('Test_FindTimelineAnchorSlot_TestPrecedingHalfHour_ExpectAnchored', () => {
   const startTime = '11:35';
   const startMinutes = DayPlannerScheduleController.parseClockTimeMinutes(startTime);
   const slotStarts = DayPlannerScheduleController.buildHalfHourSlotStarts(9 * 60 + 30, 19 * 60);
   const closeMinutes = 19 * 60;
   const label = 'Arrival';
   const kind = TEST_ITINERARY_CONFIG.visitBoundaryEventTypes.arrival;

   const markersByAnchor = DayPlannerTimelineRenderer.buildMarkersByAnchorSlot(
      [{ startMinutes, label, kind }],
      slotStarts,
      closeMinutes
   );

   const anchor = DayPlannerTimelineRenderer.findTimelineAnchorSlot(startMinutes, slotStarts);
   const slotEnd = DayPlannerTimelineRenderer.findTimelineSlotEndMinutes(
      anchor,
      slotStarts,
      closeMinutes
   );

   assert.equal(anchor, 11 * 60 + 30);
   assert.equal(
      DayPlannerTimelineRenderer.computeMarkerOffsetFraction(11 * 60 + 35, anchor, slotEnd),
      (11 * 60 + 35 - anchor) / (slotEnd - anchor)
   );
   assert.deepEqual(markersByAnchor.get(anchor), [{
      label,
      offsetFraction: DayPlannerTimelineRenderer.computeMarkerOffsetFraction(
         startMinutes,
         anchor,
         slotEnd
      ),
      kind,
   }]);
});


test('Test_ComputeStripHorizontalOffsetIndex_TestEmpty_ExpectZero', () => {
   const pointPillVerticalSpanFraction = (
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
      / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );

   const index = DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex(
      [],
      0.5,
      pointPillVerticalSpanFraction
   );

   assert.equal(index, 0);
});


test('Test_ComputeStripHorizontalOffsetIndex_TestOneOverlap_ExpectShifted', () => {
   const pointPillVerticalSpanFraction = (
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
      / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
   const placements = [{ offsetFraction: 0.5, horizontalOffsetIndex: 0 }];

   const index = DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex(
      placements,
      0.67,
      pointPillVerticalSpanFraction
   );

   assert.equal(index, 1);
});


test('Test_ComputeStripHorizontalOffsetIndex_TestTwoOverlaps_ExpectSecondShift', () => {
   const pointPillVerticalSpanFraction = (
      TimelineLayoutConstants.TIMELINE_POINT_PILL_HEIGHT_PX
      / TimelineLayoutConstants.TIMELINE_SLOT_HEIGHT_PX
   );
   const placements = [
      { offsetFraction: 0.5, horizontalOffsetIndex: 0 },
      { offsetFraction: 0.67, horizontalOffsetIndex: 1 },
   ];

   const index = DayPlannerTimelinePillPlacer.computeStripHorizontalOffsetIndex(
      placements,
      0.6,
      pointPillVerticalSpanFraction
   );

   assert.equal(index, 2);
});


test('Test_ComputeTimelineHorizontalOffsetIndex_TestEmpty_ExpectZero', () => {
   const index = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex([], 0.5, 0.5);

   assert.equal(index, 0);
});


test('Test_ComputeTimelineHorizontalOffsetIndex_TestOverlap_ExpectShifted', () => {
   const placements = [{ offsetFraction: 0.5, durationFraction: 0.5, horizontalOffsetIndex: 0 }];

   const index = DayPlannerTimelinePillPlacer.computeTimelineHorizontalOffsetIndex(
      placements,
      0.67,
      0.5
   );

   assert.equal(index, 1);
});
