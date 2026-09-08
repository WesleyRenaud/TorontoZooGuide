import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerView } from '../../../../../scripts/itinerary/panel/components/dayPlannerView.js';
import { DayPlannerController } from '../../../../../scripts/itinerary/panel/components/dayPlannerController.js';
import { DayPlannerPreviewBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerPreviewBuilder.js';
import { DayPlannerTimelinePillAppender } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelinePillAppender.js';
import { DayPlannerTimelineView } from '../../../../../scripts/itinerary/panel/components/dayPlannerTimelineView.js';
import { ScheduledPillRenderBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledPillRenderBuilder.js';
import { DayPlannerScheduleController } from '../../../../../scripts/itinerary/panel/dayPlannerScheduleController.js';
import { DayPlannerScheduledItems } from '../../../../../scripts/itinerary/panel/dayPlannerScheduledItems.js';
import { DayPlannerTimelineRenderer } from '../../../../../scripts/itinerary/panel/dayPlannerTimelineRenderer.js';
import { ItineraryItemFormatter } from '../../../../../scripts/itinerary/panel/itineraryItemFormatter.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

function _stubPreviewDeps({ timelineSlotStarts = [], scheduledSection = null, unscheduledSection = null } = {}) {
   const originals = {
      formatISODateFull: ItineraryItemFormatter.formatISODateFull,
      makeDayPlannerControls: DayPlannerController.makeDayPlannerControls,
      parseClockTimeMinutes: DayPlannerScheduleController.parseClockTimeMinutes,
      resolveDayPlannerTimelineStartMinutes: DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes,
      buildHalfHourSlotStarts: DayPlannerScheduleController.buildHalfHourSlotStarts,
      formatMinutesAsClockTime: DayPlannerScheduleController.formatMinutesAsClockTime,
      buildItineraryTimeMarkers: DayPlannerTimelineRenderer.buildItineraryTimeMarkers,
      buildTimelineSlotStarts: DayPlannerPreviewBuilder.buildTimelineSlotStarts,
      buildMarkersByAnchorSlot: DayPlannerTimelineRenderer.buildMarkersByAnchorSlot,
      buildScheduledItemRowsContext: DayPlannerScheduledItems.buildScheduledItemRowsContext,
      planScheduledPillRenderGroupsByAnchor: ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor,
      buildTimelinePointPillMarkers: DayPlannerPreviewBuilder.buildTimelinePointPillMarkers,
      appendScheduleActionButtons: DayPlannerPreviewBuilder.appendScheduleActionButtons,
      makeUnavailableMessage: DayPlannerTimelineView.makeUnavailableMessage,
      makeTimelineRow: DayPlannerTimelineView.makeTimelineRow,
      appendTimelineBoundaryLabel: DayPlannerTimelineView.appendTimelineBoundaryLabel,
      appendItineraryTimeMarkers: DayPlannerTimelinePillAppender.appendItineraryTimeMarkers,
      appendScheduledItems: DayPlannerTimelineView.appendScheduledItems,
      resolveTimelinePillLabel: DayPlannerTimelineRenderer.resolveTimelinePillLabel,
      makeItemsListSection: DayPlannerPreviewBuilder.makeItemsListSection,
      buildScheduledItinerary: DayPlannerScheduledItems.buildScheduledItinerary,
      buildUnscheduledItinerary: DayPlannerScheduledItems.buildUnscheduledItinerary,
   };

   ItineraryItemFormatter.formatISODateFull = () => 'June 15, 2026';
   DayPlannerController.makeDayPlannerControls = () => {
      const el = document.createElement('div');
      el.className = 'controls';
      return el;
   };
   DayPlannerScheduleController.parseClockTimeMinutes = (value) => {
      if (!value) return null;
      const [h, m] = String(value).split(':').map(Number);
      return (h * 60) + m;
   };
   DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes = () => 9 * 60 + 30;
   DayPlannerScheduleController.buildHalfHourSlotStarts = () => [570, 600];
   DayPlannerScheduleController.formatMinutesAsClockTime = (minutes) => `${minutes}`;
   DayPlannerTimelineRenderer.buildItineraryTimeMarkers = () => [];
   DayPlannerPreviewBuilder.buildTimelineSlotStarts = () => timelineSlotStarts;
   DayPlannerTimelineRenderer.buildMarkersByAnchorSlot = () => new Map();
   DayPlannerScheduledItems.buildScheduledItemRowsContext = () => ({
      itemsByStart: new Map(),
   });
   ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor = () => new Map([
      [570, [{ label: 'Lion' }]],
   ]);
   DayPlannerPreviewBuilder.buildTimelinePointPillMarkers = () => [];
   DayPlannerPreviewBuilder.appendScheduleActionButtons = (bar) => {
      bar.appendChild(document.createElement('button'));
   };
   DayPlannerTimelineView.makeUnavailableMessage = (message) => {
      const el = document.createElement('div');
      el.className = 'unavailable';
      el.textContent = message;
      return el;
   };
   DayPlannerTimelineView.makeTimelineRow = (label) => {
      const timeCell = document.createElement('div');
      timeCell.className = 'time';
      timeCell.textContent = label;
      return [timeCell, document.createElement('div')];
   };
   DayPlannerTimelineView.appendTimelineBoundaryLabel = () => {};
   DayPlannerTimelinePillAppender.appendItineraryTimeMarkers = () => {};
   DayPlannerTimelineView.appendScheduledItems = () => {};
   DayPlannerTimelineRenderer.resolveTimelinePillLabel = () => 'Open';
   DayPlannerPreviewBuilder.makeItemsListSection = (_itinerary, title) => {
      if (title.includes('Scheduled') && scheduledSection) {
         return scheduledSection;
      }
      if (title.includes('Unscheduled') && unscheduledSection) {
         return unscheduledSection;
      }
      return null;
   };
   DayPlannerScheduledItems.buildScheduledItinerary = () => ({ animals: [] });
   DayPlannerScheduledItems.buildUnscheduledItinerary = () => ({ animals: [] });

   return () => {
      Object.assign(ItineraryItemFormatter, {
         formatISODateFull: originals.formatISODateFull,
      });
      DayPlannerController.makeDayPlannerControls = originals.makeDayPlannerControls;
      DayPlannerScheduleController.parseClockTimeMinutes = originals.parseClockTimeMinutes;
      DayPlannerScheduleController.resolveDayPlannerTimelineStartMinutes = originals.resolveDayPlannerTimelineStartMinutes;
      DayPlannerScheduleController.buildHalfHourSlotStarts = originals.buildHalfHourSlotStarts;
      DayPlannerScheduleController.formatMinutesAsClockTime = originals.formatMinutesAsClockTime;
      DayPlannerTimelineRenderer.buildItineraryTimeMarkers = originals.buildItineraryTimeMarkers;
      DayPlannerPreviewBuilder.buildTimelineSlotStarts = originals.buildTimelineSlotStarts;
      DayPlannerTimelineRenderer.buildMarkersByAnchorSlot = originals.buildMarkersByAnchorSlot;
      DayPlannerScheduledItems.buildScheduledItemRowsContext = originals.buildScheduledItemRowsContext;
      ScheduledPillRenderBuilder.planScheduledPillRenderGroupsByAnchor = originals.planScheduledPillRenderGroupsByAnchor;
      DayPlannerPreviewBuilder.buildTimelinePointPillMarkers = originals.buildTimelinePointPillMarkers;
      DayPlannerPreviewBuilder.appendScheduleActionButtons = originals.appendScheduleActionButtons;
      DayPlannerTimelineView.makeUnavailableMessage = originals.makeUnavailableMessage;
      DayPlannerTimelineView.makeTimelineRow = originals.makeTimelineRow;
      DayPlannerTimelineView.appendTimelineBoundaryLabel = originals.appendTimelineBoundaryLabel;
      DayPlannerTimelinePillAppender.appendItineraryTimeMarkers = originals.appendItineraryTimeMarkers;
      DayPlannerTimelineView.appendScheduledItems = originals.appendScheduledItems;
      DayPlannerTimelineRenderer.resolveTimelinePillLabel = originals.resolveTimelinePillLabel;
      DayPlannerPreviewBuilder.makeItemsListSection = originals.makeItemsListSection;
      DayPlannerScheduledItems.buildScheduledItinerary = originals.buildScheduledItinerary;
      DayPlannerScheduledItems.buildUnscheduledItinerary = originals.buildUnscheduledItinerary;
   };
}

test('Test_MakeDayPlannerPreview_TestNoSlots_ExpectUnavailableMessage', () => {
   const restore = _stubPreviewDeps({ timelineSlotStarts: [] });

   try {
      const root = DayPlannerView.makeDayPlannerPreview(
         { date: '2026-06-15' },
         {},
         {},
         {
            onScheduleItemClick: () => {},
            onRebuildScheduleClick: () => {},
         }
      );

      assert.equal(root.className, 'itinerary-day-planner-content');
      assert.ok(root.querySelector('.unavailable'));
      const scheduleActions = root.querySelector('.itinerary-day-module-schedule-actions');
      assert.ok(scheduleActions);
      assert.ok(scheduleActions.children.length > 0);
      assert.equal(root.querySelector('.itinerary-day-timeline'), null);
   } finally {
      restore();
   }
});

test('Test_MakeDayPlannerPreview_TestSlots_ExpectTimelineAndLists', () => {
   const scheduled = document.createElement('div');
   scheduled.className = 'scheduled-list';
   const unscheduled = document.createElement('div');
   unscheduled.className = 'unscheduled-list';
   const restore = _stubPreviewDeps({
      timelineSlotStarts: [570, 600],
      scheduledSection: scheduled,
      unscheduledSection: unscheduled,
   });

   try {
      const root = DayPlannerView.makeDayPlannerPreview(
         {
            date: '2026-06-15',
            earlyAdmissionTime: '09:00',
            openTime: '09:30',
            lastAdmissionTime: '18:00',
            closeTime: '19:00',
         },
         { itineraryConfig: { visitBoundaryEventTypes: {} } },
         {},
         { scheduleHandlers: { onRemoveItineraryItem: () => {} } }
      );

      assert.ok(root.querySelector('.itinerary-day-timeline'));
      assert.ok(root.querySelector('.scheduled-list'));
      assert.ok(root.querySelector('.unscheduled-list'));
      assert.ok(root.querySelector('.controls'));
   } finally {
      restore();
   }
});

test('Test_MakeDayPlannerPreview_TestInvalidHoursObject_ExpectUsesEmptyHours', () => {
   const restore = _stubPreviewDeps({ timelineSlotStarts: [] });

   try {
      const root = DayPlannerView.makeDayPlannerPreview('not-an-object', {});
      assert.ok(root.querySelector('.unavailable'));
   } finally {
      restore();
   }
});
