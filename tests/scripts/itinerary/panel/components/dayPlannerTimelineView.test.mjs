import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelineView } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { DayPlannerScheduledPillOptions } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { DayPlannerTimelinePillAppender } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppender.js';
import { ItineraryPillView } from '../../../../../scripts/itinerary/panel/components/itineraryPillView.js';
import { SpeciesFragment } from '../../../../../scripts/overlays/speciesFragment.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { RegionColors } from '../../../../../scripts/shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();


test('Test_AttachScheduledEventCardMenu_TestMissingRow_ExpectNoOp', () => {
   DayPlannerTimelineView.attachScheduledEventCardMenu(null, { menuItems: [{ label: 'Remove' }] });
});


test('Test_AttachScheduledEventCardMenu_TestEmptyItems_ExpectNoOp', () => {
   const row = document.createElement('div');

   DayPlannerTimelineView.attachScheduledEventCardMenu(row, { menuItems: [] });

   assert.equal(row.children.length, 0);
});


test('Test_AttachScheduledEventCardMenu_TestItems_ExpectMenuBound', () => {
   const originalBuild = ItineraryPillView.buildPillMenuNodes;
   const originalBind = ItineraryPillView.bindPillMenu;
   const binds = [];

   ItineraryPillView.buildPillMenuNodes = () => ({
      menu: document.createElement('div'),
      menuButton: document.createElement('button'),
      menuPanel: document.createElement('div'),
   });
   ItineraryPillView.bindPillMenu = (...args) => {
      binds.push(args);
   };

   try {
      const row = document.createElement('div');
      DayPlannerTimelineView.attachScheduledEventCardMenu(row, {
         menuAriaLabel: 'Menu',
         menuItems: [{ label: 'Unschedule', onAction: () => {} }],
      });

      assert.ok(row.classList.contains('itinerary-day-event-card--with-menu'));
      assert.equal(binds.length, 1);
   } finally {
      ItineraryPillView.buildPillMenuNodes = originalBuild;
      ItineraryPillView.bindPillMenu = originalBind;
   }
});


test('Test_MakeScheduledItemBlock_TestOffsetAndColors_ExpectBlock', () => {
   const originalApply = RegionColors.applyRegionColorsToElement;
   const originalResolve = RegionColors.resolveRegionColorSlugForScheduledItem;
   const originalAttach = DayPlannerTimelineView.attachScheduledEventCardMenu;
   const offsetFraction = 0.25;
   const applies = [];

   RegionColors.resolveRegionColorSlugForScheduledItem = () => 'africa';
   RegionColors.applyRegionColorsToElement = (...args) => {
      applies.push(args);
   };
   DayPlannerTimelineView.attachScheduledEventCardMenu = () => {};

   try {
      const row = document.createElement('div');
      const block = DayPlannerTimelineView.makeScheduledItemBlock(
         row,
         TimelineLayoutConstants.TIMELINE_SLOT_MINUTES * 2,
         offsetFraction,
         { menuItems: [] },
         { species: 'African Lion' }
      );

      assert.equal(block.className, 'itinerary-day-event');
      assert.equal(block.getAttribute('data-offset-fraction'), String(offsetFraction));
      assert.ok(row.classList.contains('itinerary-day-event-card'));
      assert.equal(applies.length, 1);
   } finally {
      RegionColors.applyRegionColorsToElement = originalApply;
      RegionColors.resolveRegionColorSlugForScheduledItem = originalResolve;
      DayPlannerTimelineView.attachScheduledEventCardMenu = originalAttach;
   }
});


test('Test_UsesScheduledTimelineEventBlock_TestMatchingKind_ExpectTrue', () => {
   const original = ScheduleItemKind.usesScheduledTimelineEventCard;
   const scheduleItemKind = ScheduleItemKind.ANIMAL.itemType;

   ScheduleItemKind.usesScheduledTimelineEventCard = (kind) => kind === scheduleItemKind;

   try {
      const usesBlock = DayPlannerTimelineView.usesScheduledTimelineEventBlock({
         row: document.createElement('div'),
         scheduleItemKind,
      });

      assert.equal(usesBlock, true);
   } finally {
      ScheduleItemKind.usesScheduledTimelineEventCard = original;
   }
});


test('Test_UsesScheduledTimelineEventBlock_TestMissingRow_ExpectFalse', () => {
   const original = ScheduleItemKind.usesScheduledTimelineEventCard;
   const scheduleItemKind = ScheduleItemKind.ANIMAL.itemType;

   ScheduleItemKind.usesScheduledTimelineEventCard = (kind) => kind === scheduleItemKind;

   try {
      const usesBlock = DayPlannerTimelineView.usesScheduledTimelineEventBlock({
         scheduleItemKind,
      });

      assert.equal(usesBlock, false);
   } finally {
      ScheduleItemKind.usesScheduledTimelineEventCard = original;
   }
});


test('Test_ResolveRenderGroupLabel_TestGroupedLabel_ExpectLabel', () => {
   const label = 'Grouped';
   const group = { label, items: [{ label: 'African Lion' }] };

   const groupLabel = DayPlannerTimelineView.resolveRenderGroupLabel(group);

   assert.equal(groupLabel, label);
});


test('Test_ResolveRenderGroupLabel_TestFirstItem_ExpectItemLabel', () => {
   const lion = 'African Lion';
   const items = [{ label: lion }, { label: 'Amur Tiger' }];

   const groupLabel = DayPlannerTimelineView.resolveRenderGroupLabel({ items });

   assert.equal(groupLabel, lion);
});


test('Test_ResolveRenderGroupStartTime_TestItems_ExpectEarliest', () => {
   const startTime = '10:00';
   const group = {
      items: [
         { item: { start_time: startTime, end_time: '10:20' } },
         { item: { start_time: '10:10', end_time: '10:30' } },
      ],
   };

   const resolved = DayPlannerTimelineView.resolveRenderGroupStartTime(group);

   assert.equal(resolved, startTime);
});


test('Test_ResolveRenderGroupEndTime_TestItems_ExpectLatest', () => {
   const endTime = '10:30';
   const group = {
      items: [
         { item: { start_time: '10:00', end_time: '10:20' } },
         { item: { start_time: '10:10', end_time: endTime } },
      ],
   };

   const resolved = DayPlannerTimelineView.resolveRenderGroupEndTime(group);

   assert.equal(resolved, endTime);
});


test('Test_ResolveRenderGroupEndTime_TestSingleItem_ExpectItemEnd', () => {
   const endTime = '10:20';
   const group = {
      items: [{ item: { start_time: '10:00', end_time: endTime } }],
   };

   const resolved = DayPlannerTimelineView.resolveRenderGroupEndTime(group);

   assert.equal(resolved, endTime);
});


test('Test_ResolveRenderGroupItem_TestFirst_ExpectSpecies', () => {
   const species = 'African Lion';
   const group = {
      items: [
         { item: { species } },
         { item: { species: 'Amur Tiger' } },
      ],
   };

   const item = DayPlannerTimelineView.resolveRenderGroupItem(group);

   assert.equal(item?.species, species);
});


test('Test_ResolveRenderGroupLabelClick_TestGrouped_ExpectNull', () => {
   const group = {
      items: [
         { scheduleItemKind: ScheduleItemKind.ANIMAL.itemType, item: { species: 'African Lion' } },
         { scheduleItemKind: ScheduleItemKind.ANIMAL.itemType, item: { species: 'Amur Tiger' } },
      ],
   };

   const onClick = DayPlannerTimelineView.resolveRenderGroupLabelClick(group);

   assert.equal(onClick, null);
});


test('Test_ResolveRenderGroupLabelClick_TestSingleAnimal_ExpectOpensOverlay', () => {
   const species = 'African Lion';
   const singleAnimal = {
      items: [{
         scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
         item: { species },
      }],
   };
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   const opens = [];

   SpeciesFragment.openAnimalSpeciesOverlay = (item) => {
      opens.push(item.species);
   };

   try {
      DayPlannerTimelineView.resolveRenderGroupLabelClick(singleAnimal)?.();

      assert.deepEqual(opens, [species]);
   } finally {
      SpeciesFragment.openAnimalSpeciesOverlay = originalOpen;
   }
});


test('Test_ResolveRenderGroupLabelClick_TestAttraction_ExpectNull', () => {
   const attraction = {
      items: [{
         scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
         item: { name: 'Conservation Carousel' },
      }],
   };

   const onClick = DayPlannerTimelineView.resolveRenderGroupLabelClick(attraction);

   assert.equal(onClick, null);
});


test('Test_ResolveScheduledItemLabelClick_TestAttraction_ExpectNull', () => {
   const onClick = DayPlannerTimelineView.resolveScheduledItemLabelClick({
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
   });

   assert.equal(onClick, null);
});


test('Test_ResolveRenderGroupPillOptions_TestSingle_ExpectDelegates', () => {
   const originalSingle = DayPlannerScheduledPillOptions.resolveScheduledPillOptions;
   const originalGrouped = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions;
   const label = 'African Lion';
   const calls = [];

   DayPlannerScheduledPillOptions.resolveScheduledPillOptions = (...args) => {
      calls.push(['single', args.at(Position.FIRST).label]);
      return { menuItems: [] };
   };
   DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = () => ({ menuItems: [] });

   try {
      DayPlannerTimelineView.resolveRenderGroupPillOptions({
         items: [{ label }],
      });

      assert.deepEqual(calls, [['single', label]]);
   } finally {
      DayPlannerScheduledPillOptions.resolveScheduledPillOptions = originalSingle;
      DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = originalGrouped;
   }
});


test('Test_ResolveRenderGroupPillOptions_TestGrouped_ExpectDelegates', () => {
   const originalSingle = DayPlannerScheduledPillOptions.resolveScheduledPillOptions;
   const originalGrouped = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions;
   const items = [{ label: 'African Lion' }, { label: 'Amur Tiger' }];
   const calls = [];

   DayPlannerScheduledPillOptions.resolveScheduledPillOptions = () => ({ menuItems: [] });
   DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = (...args) => {
      calls.push(['grouped', args.at(Position.FIRST).length]);
      return { menuItems: [] };
   };

   try {
      DayPlannerTimelineView.resolveRenderGroupPillOptions({ items });

      assert.deepEqual(calls, [['grouped', items.length]]);
   } finally {
      DayPlannerScheduledPillOptions.resolveScheduledPillOptions = originalSingle;
      DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = originalGrouped;
   }
});


test('Test_TimelineSlotRowHeightFraction_TestSpan_ExpectScaled', () => {
   const slotSpanMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES * 2;

   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(slotSpanMinutes);

   assert.equal(fraction, slotSpanMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);
});


test('Test_TimelineSlotRowHeightFraction_TestNaN_ExpectOne', () => {
   const fraction = DayPlannerTimelineView.timelineSlotRowHeightFraction(Number.NaN);

   assert.equal(fraction, 1);
});


test('Test_MakeTimelineRow_TestSpan_ExpectCssVars', () => {
   const label = ZooClockTimeHelper.formatClockTime('09:30');
   const slotSpanMinutes = 45;

   const [timeCell, gridLine] = DayPlannerTimelineView.makeTimelineRow(label, slotSpanMinutes);

   assert.equal(timeCell.className, 'itinerary-day-time');
   assert.equal(gridLine.className, 'itinerary-day-grid-line');
   assert.equal(
      timeCell.style['--itinerary-slot-row-height-fraction']
         ?? timeCell.attributes?.['style:--itinerary-slot-row-height-fraction'],
      String(slotSpanMinutes / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
   );
});


test('Test_AppendTimelineBoundaryLabel_TestEmpty_ExpectNoLabel', () => {
   const timeCell = document.createElement('div');

   DayPlannerTimelineView.appendTimelineBoundaryLabel(timeCell, '');

   assert.equal(timeCell.children.length, 0);
});


test('Test_AppendTimelineBoundaryLabel_TestLabel_ExpectNode', () => {
   const timeCell = document.createElement('div');
   const label = 'Open';

   DayPlannerTimelineView.appendTimelineBoundaryLabel(timeCell, label);

   assert.equal(
      timeCell.querySelector('.itinerary-day-time-boundary-label')?.textContent,
      label
   );
});


test('Test_MakeUnavailableMessage_TestText_ExpectNode', () => {
   const text = 'Hours unavailable';

   const message = DayPlannerTimelineView.makeUnavailableMessage(text);

   assert.equal(message.className, 'itinerary-day-unavailable');
   assert.equal(message.textContent, text);
});


test('Test_AppendScheduledItems_TestEventBlockAndPill_ExpectAppends', () => {
   const originalUses = DayPlannerTimelineView.usesScheduledTimelineEventBlock;
   const originalMake = DayPlannerTimelineView.makeScheduledItemBlock;
   const originalOptions = DayPlannerScheduledPillOptions.resolveScheduledPillOptions;
   const originalAppend = DayPlannerTimelinePillAppender.appendScheduledDurationPill;
   const talkLabel = 'Wildlife Talk';
   const blocks = [];
   const pills = [];

   DayPlannerTimelineView.usesScheduledTimelineEventBlock = (item) => item.useBlock;
   DayPlannerTimelineView.makeScheduledItemBlock = (...args) => {
      blocks.push(args.at(Position.FIRST));
      const el = document.createElement('div');
      el.className = 'block';
      return el;
   };
   DayPlannerScheduledPillOptions.resolveScheduledPillOptions = () => ({ menuItems: [] });
   DayPlannerTimelinePillAppender.appendScheduledDurationPill = (_grid, options) => {
      pills.push(options.label);
   };

   try {
      const gridLine = document.createElement('div');
      DayPlannerTimelineView.appendScheduledItems(gridLine, [
         {
            items: [{
               useBlock: true,
               row: document.createElement('div'),
               maximumDuration: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
               offsetFraction: 0,
               item: { species: 'African Lion' },
            }],
         },
         {
            label: talkLabel,
            durationMinutes: TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
            items: [{
               useBlock: false,
               label: talkLabel,
               item: { start_time: '11:00', end_time: '11:30' },
            }],
         },
      ]);

      assert.equal(blocks.length, 1);
      assert.deepEqual(pills, [talkLabel]);
      assert.ok(gridLine.querySelector('.block'));
   } finally {
      DayPlannerTimelineView.usesScheduledTimelineEventBlock = originalUses;
      DayPlannerTimelineView.makeScheduledItemBlock = originalMake;
      DayPlannerScheduledPillOptions.resolveScheduledPillOptions = originalOptions;
      DayPlannerTimelinePillAppender.appendScheduledDurationPill = originalAppend;
   }
});
