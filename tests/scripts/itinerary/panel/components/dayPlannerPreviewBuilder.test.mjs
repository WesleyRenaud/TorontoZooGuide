import assert from 'node:assert/strict';
import test from 'node:test';

import { DayPlannerActionFeedbackFragment } from '../../../../../scripts/itinerary/panel/components/dayPlannerActionFeedbackFragment.js';
import { DayPlannerPreviewBuilder } from '../../../../../scripts/itinerary/panel/components/dayPlannerPreviewBuilder.js';
import { ScheduleItemView } from '../../../../../scripts/itinerary/panel/components/scheduleItemView.js';
import { DayPlannerActionPresenter } from '../../../../../scripts/itinerary/panel/dayPlannerActionPresenter.js';
import { ItineraryPanelHelper } from '../../../../../scripts/itinerary/panel/itineraryPanelHelper.js';
import { ItineraryPanelSectionBuilder } from '../../../../../scripts/itinerary/panel/components/itineraryPanelSectionBuilder.js';
import { SectionConfigs } from '../../../../../scripts/itinerary/panel/sectionConfigs.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ResolveSectionShowEditButton_TestKeysAndDefault_ExpectBoolean', () => {
   assert.equal(
      DayPlannerPreviewBuilder.resolveSectionShowEditButton('animals', {
         editButtonSectionKeys: ['animals', 'attractions'],
      }),
      true
   );
   assert.equal(
      DayPlannerPreviewBuilder.resolveSectionShowEditButton('wildEncounters', {
         editButtonSectionKeys: ['animals'],
      }),
      false
   );
   assert.equal(
      DayPlannerPreviewBuilder.resolveSectionShowEditButton('animals', {
         showEditButton: false,
      }),
      false
   );
   assert.equal(
      DayPlannerPreviewBuilder.resolveSectionShowEditButton('animals'),
      true
   );
});

test('Test_MakeItemsListSection_TestEmptyConfigs_ExpectNull', () => {
   const originalBuild = SectionConfigs.buildSectionConfigs;
   SectionConfigs.buildSectionConfigs = () => [];

   try {
      assert.equal(DayPlannerPreviewBuilder.makeItemsListSection({}), null);
   } finally {
      SectionConfigs.buildSectionConfigs = originalBuild;
   }
});

test('Test_MakeItemsListSection_TestSections_ExpectWrapperWithTitle', () => {
   const originalBuild = SectionConfigs.buildSectionConfigs;
   const originalEl = ItineraryPanelHelper.el;
   const originalMake = ItineraryPanelSectionBuilder.makeSection;
   const originalResolve = DayPlannerPreviewBuilder.resolveSectionShowEditButton;
   const sectionCalls = [];

   SectionConfigs.buildSectionConfigs = () => [
      { key: 'animals', title: 'Animals' },
   ];
   ItineraryPanelHelper.el = (tag, className, text) => {
      const el = document.createElement(tag);
      if (className) el.className = className;
      if (text != null) el.textContent = text;
      return el;
   };
   DayPlannerPreviewBuilder.resolveSectionShowEditButton = () => false;
   ItineraryPanelSectionBuilder.makeSection = (config) => {
      sectionCalls.push(config);
      const section = document.createElement('div');
      section.className = 'section';
      return section;
   };

   try {
      const wrapper = DayPlannerPreviewBuilder.makeItemsListSection(
         { animals: [] },
         'Scheduled',
         { showEditButton: true }
      );

      assert.equal(wrapper.className, 'itinerary-day-items-sections');
      assert.equal(wrapper.querySelector('.itinerary-day-items-title')?.textContent, 'Scheduled');
      assert.equal(sectionCalls.length, 1);
      assert.equal(sectionCalls[0].showEditButton, false);
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
   const runCalls = [];
   const bannerCalls = [];

   DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = () => ({
      variant: 'success',
      message: 'ok',
   });
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
   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackSlot = (container) => {
      const slot = document.createElement('div');
      slot.className = 'feedback-slot';
      container.appendChild(slot);
      return slot;
   };
   DayPlannerActionFeedbackFragment.appendDayPlannerActionFeedbackBanner = (slot, feedback) => {
      bannerCalls.push({ slotClass: slot.className, feedback });
   };

   const container = document.createElement('div');
   const scheduleClicks = [];
   const rebuildClicks = [];
   const unscheduleClicks = [];

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
            scheduleItemButton: 'Schedule',
            rebuildScheduleButton: 'Rebuild',
            rebuildScheduleButtonBusy: 'Rebuilding',
            unscheduleAllButton: 'Unschedule all',
            unscheduleAllButtonBusy: 'Unscheduling',
         },
      });

      assert.ok(container.querySelector('.actions-bar'));
      container.querySelectorAll('button')[0].listeners.click();
      assert.deepEqual(scheduleClicks, [true]);

      container.querySelectorAll('button')[1].listeners.click();
      assert.deepEqual(runCalls, ['Rebuild']);
      assert.deepEqual(rebuildClicks, [true]);

      container.querySelectorAll('button')[2].listeners.click();
      assert.deepEqual(unscheduleClicks, [true]);
      assert.deepEqual(bannerCalls[0].feedback, { variant: 'success', message: 'ok' });
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
   DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = () => null;
   const container = document.createElement('div');

   try {
      DayPlannerPreviewBuilder.appendScheduleActionButtons(container, {});
      assert.equal(container.children.length, 0);
   } finally {
      DayPlannerActionPresenter.consumePendingDayPlannerActionFeedback = originalConsume;
   }
});

test('Test_BuildTimelinePointPillMarkers_TestFiniteValues_ExpectStartMinutes', () => {
   assert.deepEqual(
      DayPlannerPreviewBuilder.buildTimelinePointPillMarkers({
         earlyAdmissionMinutes: 540,
         openMinutes: 570,
         lastAdmissionMinutes: null,
         closeMinutes: 1140,
         itineraryTimeMarkers: [
            { startMinutes: 600 },
            { startMinutes: Number.NaN },
         ],
      }),
      [
         { startMinutes: 540 },
         { startMinutes: 570 },
         { startMinutes: 1140 },
         { startMinutes: 600 },
      ]
   );
});

test('Test_BuildTimelineSlotStarts_TestCloseAppended_ExpectSorted', () => {
   assert.deepEqual(
      DayPlannerPreviewBuilder.buildTimelineSlotStarts([570, 600], 630),
      [570, 600, 630]
   );
   assert.deepEqual(
      DayPlannerPreviewBuilder.buildTimelineSlotStarts([570, 600, 630], 630),
      [570, 600, 630]
   );
});
