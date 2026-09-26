import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerActionFeedbackFragment } from '../../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { DayPlannerPreviewBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerPreviewBuilder.js';
import { ScheduleItemView } from '../../../../../scripts/itinerary/panel/components/scheduleItemView.js';
import { DayPlannerActionPresenter } from '../../../../../scripts/itinerary/panel/dayPlannerActionPresenter.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { ItineraryPanelSectionBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilder.js';
import { SectionConfigs } from '../../../../../scripts/itinerary/panel/sectionConfigs.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

function _createElement(tag, className, text) {
   const el = document.createElement(tag);
   if (className) el.className = className;
   if (text != null) el.textContent = text;
   return el;
}

installDomTestHooks();


test('Test_ResolveSectionShowEditButton_TestAllowedKey_ExpectTrue', () => {
   const sectionKey = 'animals';

   const showEdit = DayPlannerPreviewBuilder.resolveSectionShowEditButton(sectionKey, {
      editButtonSectionKeys: [sectionKey, 'attractions'],
   });

   assert.equal(showEdit, true);
});


test('Test_ResolveSectionShowEditButton_TestMissingKey_ExpectFalse', () => {
   const showEdit = DayPlannerPreviewBuilder.resolveSectionShowEditButton('wildEncounters', {
      editButtonSectionKeys: ['animals'],
   });

   assert.equal(showEdit, false);
});


test('Test_ResolveSectionShowEditButton_TestShowEditFalse_ExpectFalse', () => {
   const showEdit = DayPlannerPreviewBuilder.resolveSectionShowEditButton('animals', {
      showEditButton: false,
   });

   assert.equal(showEdit, false);
});


test('Test_ResolveSectionShowEditButton_TestDefault_ExpectTrue', () => {
   const showEdit = DayPlannerPreviewBuilder.resolveSectionShowEditButton('animals');

   assert.equal(showEdit, true);
});


test('Test_MakeItemsListSection_TestEmptyConfigs_ExpectNull', () => {
   const originalBuild = SectionConfigs.buildSectionConfigs;

   SectionConfigs.buildSectionConfigs = () => [];

   try {
      const section = DayPlannerPreviewBuilder.makeItemsListSection({});

      assert.equal(section, null);
   } finally {
      SectionConfigs.buildSectionConfigs = originalBuild;
   }
});


test('Test_MakeItemsListSection_TestSections_ExpectWrapperWithTitle', () => {
   const originalBuild = SectionConfigs.buildSectionConfigs;
   const originalEl = ItineraryPanelHelper.el;
   const originalMake = ItineraryPanelSectionBuilder.makeSection;
   const originalResolve = DayPlannerPreviewBuilder.resolveSectionShowEditButton;
   const title = 'Scheduled';
   const sectionCalls = [];

   SectionConfigs.buildSectionConfigs = () => [
      { key: 'animals', title: 'Animals' },
   ];
   ItineraryPanelHelper.el = _createElement;
   DayPlannerPreviewBuilder.resolveSectionShowEditButton = () => false;
   ItineraryPanelSectionBuilder.makeSection = (config) => {
      sectionCalls.push(config);
      return _createElement('div', 'section');
   };

   try {
      const wrapper = DayPlannerPreviewBuilder.makeItemsListSection(
         { animals: [] },
         title,
         { showEditButton: true }
      );

      assert.equal(wrapper.className, 'itinerary-day-items-sections');
      assert.equal(wrapper.querySelector('.itinerary-day-items-title')?.textContent, title);
      assert.equal(sectionCalls.length, 1);
      assert.equal(sectionCalls.at(Position.FIRST).showEditButton, false);
   } finally {
      SectionConfigs.buildSectionConfigs = originalBuild;
      ItineraryPanelHelper.el = originalEl;
      ItineraryPanelSectionBuilder.makeSection = originalMake;
      DayPlannerPreviewBuilder.resolveSectionShowEditButton = originalResolve;
   }
});


test('Test_AppendScheduleActionButtons_TestHandlersAndFeedback_ExpectBar', () => {
   const originalConsume = DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback;
   const originalMakeButton = ScheduleItemView.makeScheduleItemButton;
   const originalMakeBar = ScheduleItemView.makeScheduleActionsBar;
   const originalRun = ScheduleItemView.runScheduleItemButtonAction;
   const originalAppendSlot = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot;
   const originalAppendBanner = DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner;
   const feedback = { variant: 'success', message: 'ok' };
   const scheduleLabel = 'Schedule';
   const rebuildLabel = 'Rebuild';
   const unscheduleLabel = 'Unschedule all';
   const runCalls = [];
   const bannerCalls = [];
   const container = document.createElement('div');
   const scheduleClicks = [];
   const rebuildClicks = [];
   const unscheduleClicks = [];

   DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = () => feedback;
   ScheduleItemView.makeScheduleItemButton = ({ label, variant, onClick }) => {
      const button = document.createElement('button');
      button.textContent = label;
      button.dataset.variant = variant || '';
      if (onClick) {
         button.addEventListener('click', onClick);
      }
      return button;
   };
   ScheduleItemView.makeScheduleActionsBar = (buttons) => {
      const bar = document.createElement('div');
      bar.className = 'actions-bar';
      buttons.forEach((button) => bar.appendChild(button));
      return bar;
   };
   ScheduleItemView.runScheduleItemButtonAction = async (button, action) => {
      runCalls.push(button.textContent);
      await action();
   };
   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot = (feedbackContainer) => {
      const slot = document.createElement('div');
      slot.className = 'feedback-slot';
      feedbackContainer.appendChild(slot);
      return slot;
   };
   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner = (slot, bannerFeedback) => {
      bannerCalls.push({ slotClass: slot.className, feedback: bannerFeedback });
   };

   try {
      DayPlannerPreviewBuilder.appendScheduleActionButtons(container, {
         onScheduleItemClick: () => {
            scheduleClicks.push(true);
         },
         onRebuildScheduleClick: async () => {
            rebuildClicks.push(true);
         },
         onUnscheduleAllItemsClick: async () => {
            unscheduleClicks.push(true);
         },
         strings: {
            scheduleItemButton: scheduleLabel,
            rebuildScheduleButton: rebuildLabel,
            rebuildScheduleButtonBusy: 'Rebuilding',
            unscheduleAllButton: unscheduleLabel,
            unscheduleAllButtonBusy: 'Unscheduling',
         },
      });
      const buttons = container.querySelectorAll('button');
      buttons[Position.FIRST].listeners.click();
      buttons[Position.SECOND].listeners.click();
      buttons[Position.THIRD].listeners.click();

      assert.ok(container.querySelector('.actions-bar'));
      assert.deepEqual(scheduleClicks, [true]);
      assert.deepEqual(runCalls, [rebuildLabel, unscheduleLabel]);
      assert.deepEqual(rebuildClicks, [true]);
      assert.deepEqual(unscheduleClicks, [true]);
      assert.deepEqual(bannerCalls.at(Position.FIRST).feedback, feedback);
   } finally {
      DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = originalConsume;
      ScheduleItemView.makeScheduleItemButton = originalMakeButton;
      ScheduleItemView.makeScheduleActionsBar = originalMakeBar;
      ScheduleItemView.runScheduleItemButtonAction = originalRun;
      DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot = originalAppendSlot;
      DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner = originalAppendBanner;
   }
});


test('Test_AppendScheduleActionButtons_TestNoHandlers_ExpectEmpty', () => {
   const originalConsume = DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback;
   const container = document.createElement('div');

   DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = () => null;

   try {
      DayPlannerPreviewBuilder.appendScheduleActionButtons(container, {});

      assert.equal(container.children.length, 0);
   } finally {
      DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = originalConsume;
   }
});


test('Test_BuildTimelinePointPillMarkers_TestFiniteValues_ExpectStartMinutes', () => {
   const earlyAdmissionMinutes = ZooClockTimeHelper.parseMinutes('9:00');
   const openMinutes = ZooClockTimeHelper.parseMinutes('9:30');
   const closeMinutes = ZooClockTimeHelper.parseMinutes('19:00');
   const itineraryStart = ZooClockTimeHelper.parseMinutes('10:00');

   const markers = DayPlannerPreviewBuilder.buildTimelinePointPillMarkers({
      earlyAdmissionMinutes,
      openMinutes,
      lastAdmissionMinutes: null,
      closeMinutes,
      itineraryTimeMarkers: [
         { startMinutes: itineraryStart },
         { startMinutes: Number.NaN },
      ],
   });

   assert.deepEqual(markers, [
      { startMinutes: earlyAdmissionMinutes },
      { startMinutes: openMinutes },
      { startMinutes: closeMinutes },
      { startMinutes: itineraryStart },
   ]);
});


test('Test_BuildTimelineSlotStarts_TestCloseAppended_ExpectSorted', () => {
   const firstSlot = ZooClockTimeHelper.parseMinutes('9:30');
   const secondSlot = ZooClockTimeHelper.parseMinutes('10:00');
   const closeMinutes = ZooClockTimeHelper.parseMinutes('10:30');

   const slotStarts = DayPlannerPreviewBuilder.buildTimelineSlotStarts(
      [firstSlot, secondSlot],
      closeMinutes
   );

   assert.deepEqual(slotStarts, [firstSlot, secondSlot, closeMinutes]);
});


test('Test_BuildTimelineSlotStarts_TestCloseAlreadyPresent_ExpectUnchanged', () => {
   const firstSlot = ZooClockTimeHelper.parseMinutes('9:30');
   const secondSlot = ZooClockTimeHelper.parseMinutes('10:00');
   const closeMinutes = ZooClockTimeHelper.parseMinutes('10:30');
   const slotStarts = [firstSlot, secondSlot, closeMinutes];

   const result = DayPlannerPreviewBuilder.buildTimelineSlotStarts(slotStarts, closeMinutes);

   assert.deepEqual(result, slotStarts);
});
