import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerTimelineView } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { DayPlannerScheduledPillOptions } from '../../../../../scripts/itinerary/panel/components/dayPlannerScheduledPillOptions.js';
import { DayPlannerTimelinePillAppender } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppender.js';
import { ItineraryPillView } from '../../../../../scripts/itinerary/panel/components/itineraryPillView.js';
import { SpeciesFragment } from '../../../../../scripts/overlays/speciesFragment.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { RegionColors } from '../../../../../scripts/shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_AttachScheduledEventCardMenu_TestMissingOrEmpty_ExpectNoOp', () => {
   DayPlannerTimelineView.attachScheduledEventCardMenu(null, { menuItems: [{ label: 'x' }] });
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
         60,
         0.25,
         { menuItems: [] },
         { species: 'Lion' }
      );
      assert.equal(block.className, 'itinerary-day-event');
      assert.equal(block.getAttribute('data-offset-fraction'), '0.25');
      assert.ok(row.classList.contains('itinerary-day-event-card'));
      assert.equal(applies.length, 1);
   } finally {
      RegionColors.applyRegionColorsToElement = originalApply;
      RegionColors.resolveRegionColorSlugForScheduledItem = originalResolve;
      DayPlannerTimelineView.attachScheduledEventCardMenu = originalAttach;
   }
});

test('Test_UsesScheduledTimelineEventBlock_TestKinds_ExpectBoolean', () => {
   const original = ScheduleItemKind.usesScheduledTimelineEventCard;
   ScheduleItemKind.usesScheduledTimelineEventCard = (kind) => kind === 'animals';

   try {
      assert.equal(
         DayPlannerTimelineView.usesScheduledTimelineEventBlock({
            row: document.createElement('div'),
            scheduleItemKind: 'animals',
         }),
         true
      );
      assert.equal(
         DayPlannerTimelineView.usesScheduledTimelineEventBlock({
            scheduleItemKind: 'animals',
         }),
         false
      );
   } finally {
      ScheduleItemKind.usesScheduledTimelineEventCard = original;
   }
});

test('Test_ResolveRenderGroupHelpers_TestLabelsTimesAndClicks_ExpectValues', () => {
   const group = {
      label: 'Grouped',
      items: [
         {
            label: 'Lion',
            scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
            item: { start_time: '10:00', end_time: '10:20', species: 'Lion' },
         },
         {
            label: 'Tiger',
            scheduleItemKind: ScheduleItemKind.ANIMAL.itemType,
            item: { start_time: '10:10', end_time: '10:30', species: 'Tiger' },
         },
      ],
   };

   assert.equal(DayPlannerTimelineView.resolveRenderGroupLabel(group), 'Grouped');
   assert.equal(
      DayPlannerTimelineView.resolveRenderGroupLabel({ items: group.items }),
      'Lion'
   );
   assert.equal(DayPlannerTimelineView.resolveRenderGroupStartTime(group), '10:00');
   assert.equal(DayPlannerTimelineView.resolveRenderGroupEndTime(group), '10:30');
   assert.equal(
      DayPlannerTimelineView.resolveRenderGroupEndTime({ items: [group.items[0]] }),
      '10:20'
   );
   assert.equal(DayPlannerTimelineView.resolveRenderGroupItem(group)?.species, 'Lion');
   assert.equal(DayPlannerTimelineView.resolveRenderGroupLabelClick(group), null);

   const singleAnimal = { items: [group.items[0]] };
   const originalOpen = SpeciesFragment.openAnimalSpeciesOverlay;
   const opens = [];
   SpeciesFragment.openAnimalSpeciesOverlay = (item) => {
      opens.push(item.species);
   };

   try {
      DayPlannerTimelineView.resolveRenderGroupLabelClick(singleAnimal)?.();
      assert.deepEqual(opens, ['Lion']);

      const attraction = {
         items: [{
            scheduleItemKind: 'attractions',
            item: { name: 'Carousel' },
         }],
      };
      assert.equal(DayPlannerTimelineView.resolveRenderGroupLabelClick(attraction), null);
      assert.equal(
         DayPlannerTimelineView.resolveScheduledItemLabelClick({
            scheduleItemKind: 'attractions',
         }),
         null
      );
   } finally {
      SpeciesFragment.openAnimalSpeciesOverlay = originalOpen;
   }
});

test('Test_ResolveRenderGroupPillOptions_TestSingleAndGrouped_ExpectDelegates', () => {
   const originalSingle = DayPlannerScheduledPillOptions.resolveScheduledPillOptions;
   const originalGrouped = DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions;
   const calls = [];

   DayPlannerScheduledPillOptions.resolveScheduledPillOptions = (...args) => {
      calls.push(['single', args[0].label]);
      return { menuItems: [] };
   };
   DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = (...args) => {
      calls.push(['grouped', args[0].length]);
      return { menuItems: [] };
   };

   try {
      DayPlannerTimelineView.resolveRenderGroupPillOptions({
         items: [{ label: 'One' }],
      });
      DayPlannerTimelineView.resolveRenderGroupPillOptions({
         items: [{ label: 'One' }, { label: 'Two' }],
      });
      assert.deepEqual(calls, [
         ['single', 'One'],
         ['grouped', 2],
      ]);
   } finally {
      DayPlannerScheduledPillOptions.resolveScheduledPillOptions = originalSingle;
      DayPlannerScheduledPillOptions.resolveGroupedScheduledPillOptions = originalGrouped;
   }
});

test('Test_TimelineSlotRowHeightFractionAndMakeTimelineRow_TestSpan_ExpectCssVars', () => {
   assert.equal(
      DayPlannerTimelineView.timelineSlotRowHeightFraction(60),
      60 / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES
   );
   assert.equal(
      DayPlannerTimelineView.timelineSlotRowHeightFraction(Number.NaN),
      1
   );

   const [timeCell, gridLine] = DayPlannerTimelineView.makeTimelineRow('9:30 AM', 45);
   assert.equal(timeCell.className, 'itinerary-day-time');
   assert.equal(gridLine.className, 'itinerary-day-grid-line');
   assert.equal(
      timeCell.style['--itinerary-slot-row-height-fraction']
         ?? timeCell.attributes?.['style:--itinerary-slot-row-height-fraction'],
      '1.5'
   );
});

test('Test_AppendTimelineBoundaryLabelAndUnavailable_TestArgs_ExpectNodes', () => {
   const timeCell = document.createElement('div');
   DayPlannerTimelineView.appendTimelineBoundaryLabel(timeCell, '');
   assert.equal(timeCell.children.length, 0);
   DayPlannerTimelineView.appendTimelineBoundaryLabel(timeCell, 'Open');
   assert.equal(
      timeCell.querySelector('.itinerary-day-time-boundary-label')?.textContent,
      'Open'
   );

   const message = DayPlannerTimelineView.makeUnavailableMessage('Hours unavailable');
   assert.equal(message.className, 'itinerary-day-unavailable');
   assert.equal(message.textContent, 'Hours unavailable');
});

test('Test_AppendScheduledItems_TestEventBlockAndPill_ExpectAppends', () => {
   const originalUses = DayPlannerTimelineView.usesScheduledTimelineEventBlock;
   const originalMake = DayPlannerTimelineView.makeScheduledItemBlock;
   const originalOptions = DayPlannerScheduledPillOptions.resolveScheduledPillOptions;
   const originalAppend = DayPlannerTimelinePillAppender.appendScheduledDurationPill;
   const blocks = [];
   const pills = [];

   DayPlannerTimelineView.usesScheduledTimelineEventBlock = (item) => item.useBlock;
   DayPlannerTimelineView.makeScheduledItemBlock = (...args) => {
      blocks.push(args[0]);
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
               maximumDuration: 30,
               offsetFraction: 0,
               item: { species: 'Lion' },
            }],
         },
         {
            label: 'Talk',
            durationMinutes: 30,
            items: [{
               useBlock: false,
               label: 'Talk',
               item: { start_time: '11:00', end_time: '11:30' },
            }],
         },
      ]);

      assert.equal(blocks.length, 1);
      assert.deepEqual(pills, ['Talk']);
      assert.ok(gridLine.querySelector('.block'));
   } finally {
      DayPlannerTimelineView.usesScheduledTimelineEventBlock = originalUses;
      DayPlannerTimelineView.makeScheduledItemBlock = originalMake;
      DayPlannerScheduledPillOptions.resolveScheduledPillOptions = originalOptions;
      DayPlannerTimelinePillAppender.appendScheduledDurationPill = originalAppend;
   }
});
