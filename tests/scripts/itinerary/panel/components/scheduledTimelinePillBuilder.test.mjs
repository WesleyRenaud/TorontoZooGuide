import assert from 'node:assert/strict';
import test from 'node:test';

import { ScheduledTimelinePillBuilder } from '../../../../../scripts/itinerary/panel/components/scheduledTimelinePillBuilder.js';
import { ItineraryPillView } from '../../../../../scripts/itinerary/panel/components/itineraryPillView.js';
import { OpenTimelineView } from '../../../../../scripts/itinerary/panel/components/openTimelineView.js';
import { ScheduledPillPresenter } from '../../../../../scripts/itinerary/panel/scheduledPillPresenter.js';
import { RegionColors } from '../../../../../scripts/shared/regionColors.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { Strings } from '../../../../../scripts/strings.js';
import { installDomTestHooks } from '../../../helpers/domTestSetup.mjs';

installDomTestHooks();

test('Test_ApplyScheduledPillRegionColors_TestItem_ExpectDelegate', () => {
   const originalResolve = RegionColors.resolveRegionColorSlugForScheduledItem;
   const originalApply = RegionColors.applyRegionColorsToElement;
   const applies = [];

   RegionColors.resolveRegionColorSlugForScheduledItem = () => 'africa';
   RegionColors.applyRegionColorsToElement = (...args) => {
      applies.push(args);
   };

   try {
      const pill = document.createElement('div');
      ScheduledTimelinePillBuilder.applyScheduledPillRegionColors(pill, { region: 'Africa' });
      assert.equal(applies.length, 1);
      assert.equal(applies[0][1], 'africa');
   } finally {
      RegionColors.resolveRegionColorSlugForScheduledItem = originalResolve;
      RegionColors.applyRegionColorsToElement = originalApply;
   }
});

test('Test_ApplyScheduledPillDuration_TestFiniteAndFallback_ExpectCssVar', () => {
   const pill = document.createElement('div');
   ScheduledTimelinePillBuilder.applyScheduledPillDuration(pill, 45, 30);
   assert.equal(
      pill.style['--itinerary-scheduled-pill-duration-fraction']
         ?? pill.attributes?.['style:--itinerary-scheduled-pill-duration-fraction'],
      '1.5'
   );
   assert.equal(pill.getAttribute('data-duration-fraction'), '1.5');

   const pill2 = document.createElement('div');
   ScheduledTimelinePillBuilder.applyScheduledPillDuration(pill2, 30, 0);
   assert.equal(
      pill2.getAttribute('data-duration-fraction'),
      String(30 / TimelineLayoutConstants.TIMELINE_SLOT_MINUTES)
   );
});

test('Test_MakeScheduledPillArrowButton_TestDirections_ExpectLabels', () => {
   const previous = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton('Previous', 'previous');
   const next = ScheduledTimelinePillBuilder.makeScheduledPillArrowButton('Next', 'next');

   assert.equal(previous.textContent, '‹');
   assert.equal(next.textContent, '›');
   assert.equal(previous.getAttribute('aria-label'), 'Previous');
   assert.ok(previous.className.includes('previous'));
   assert.ok(next.className.includes('next'));
});

test('Test_ReplaceGroupedScheduledPillLabel_TestSuffix_ExpectCount', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   OpenTimelineView.createPillLabelNode = (label) => {
      const el = document.createElement('span');
      el.className = 'label';
      el.textContent = label;
      return el;
   };

   try {
      const mount = document.createElement('div');
      mount.appendChild(document.createElement('span'));
      ScheduledTimelinePillBuilder.replaceGroupedScheduledPillLabel(mount, {
         label: 'Lion',
         suffixCount: 2,
      });
      assert.equal(mount.querySelector('.label')?.textContent, 'Lion');
      assert.equal(
         mount.querySelector('.itinerary-day-scheduled-pill-count')?.textContent,
         Strings.itinerary.dayPlanner.scheduledPillMoreCount(2)
      );
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
   }
});

test('Test_ResolveWrappedGroupIndex_TestWrap_ExpectIndex', () => {
   assert.equal(ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(0, 0), 0);
   assert.equal(ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(-1, 3), 2);
   assert.equal(ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(3, 3), 0);
   assert.equal(ScheduledTimelinePillBuilder.resolveWrappedGroupIndex(1, 3), 1);
});

test('Test_BuildGroupedScheduledPill_TestNavigation_ExpectActiveIndex', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const originalBuild = ItineraryPillView.buildPillMenuNodes;
   const originalBind = ItineraryPillView.bindPillMenu;

   OpenTimelineView.createPillLabelNode = (label) => {
      const el = document.createElement('span');
      el.textContent = label;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => true;
   ItineraryPillView.buildPillMenuNodes = () => ({
      menu: document.createElement('div'),
      menuButton: document.createElement('button'),
      menuPanel: document.createElement('div'),
   });
   ItineraryPillView.bindPillMenu = () => {};

   try {
      const pill = ScheduledTimelinePillBuilder.buildGroupedScheduledPill(
         [
            {
               label: 'Lion',
               item: { species: 'Lion' },
               menuItems: [{ label: 'Unschedule', onAction: () => {} }],
            },
            {
               label: 'Tiger',
               item: { species: 'Tiger' },
               menuItems: [],
            },
         ],
         40,
         { menuAriaLabel: 'Menu' }
      );

      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--grouped'));
      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(pill.getAttribute('data-group-size'), '2');
      assert.equal(pill.getAttribute('data-active-group-index'), '0');

      pill.querySelector('.itinerary-day-scheduled-pill-toggle--next')?.listeners.click({
         stopPropagation() {},
      });
      assert.equal(pill.getAttribute('data-active-group-index'), '1');

      pill.querySelector('.itinerary-day-scheduled-pill-toggle--previous')?.listeners.click({
         stopPropagation() {},
      });
      assert.equal(pill.getAttribute('data-active-group-index'), '0');
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
      ItineraryPillView.buildPillMenuNodes = originalBuild;
      ItineraryPillView.bindPillMenu = originalBind;
   }
});

test('Test_BuildScheduledPillWithMenu_TestExtended_ExpectMenuBound', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;
   const originalBuild = ItineraryPillView.buildPillMenuNodes;
   const originalBind = ItineraryPillView.bindPillMenu;
   const binds = [];

   OpenTimelineView.createPillLabelNode = (label) => {
      const el = document.createElement('span');
      el.textContent = label;
      return el;
   };
   ScheduledPillPresenter.isExtendedScheduledPill = () => true;
   ItineraryPillView.buildPillMenuNodes = () => ({
      menu: document.createElement('div'),
      menuButton: document.createElement('button'),
      menuPanel: document.createElement('div'),
   });
   ItineraryPillView.bindPillMenu = (...args) => {
      binds.push(args);
   };

   try {
      const pill = ScheduledTimelinePillBuilder.buildScheduledPillWithMenu('Lion', 40, {
         startTime: '10:00',
         endTime: '10:40',
         menuItems: [{ label: 'Unschedule', onAction: () => {} }],
         menuAriaLabel: 'Menu',
      });
      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--with-menu'));
      assert.ok(pill.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.equal(binds.length, 1);
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
      ItineraryPillView.buildPillMenuNodes = originalBuild;
      ItineraryPillView.bindPillMenu = originalBind;
   }
});

test('Test_BuildScheduledPillWithoutMenu_TestCompactAndExtended_ExpectLayouts', () => {
   const originalCreate = OpenTimelineView.createPillLabelNode;
   const originalExtended = ScheduledPillPresenter.isExtendedScheduledPill;

   OpenTimelineView.createPillLabelNode = (label) => {
      const el = document.createElement('span');
      el.className = 'itinerary-day-scheduled-pill-label';
      el.textContent = label;
      return el;
   };

   try {
      ScheduledPillPresenter.isExtendedScheduledPill = () => false;
      const compact = ScheduledTimelinePillBuilder.buildScheduledPillWithoutMenu('Lion', 15, {
         startTime: '10:00',
         endTime: '10:15',
      });
      assert.equal(compact.tagName, 'span');
      assert.equal(compact.className, 'itinerary-day-scheduled-pill');

      ScheduledPillPresenter.isExtendedScheduledPill = () => true;
      const extended = ScheduledTimelinePillBuilder.buildScheduledPillWithoutMenu('Lion', 40, {
         startTime: '10:00',
         endTime: '10:40',
      });
      assert.ok(extended.classList.contains('itinerary-day-scheduled-pill--extended'));
      assert.ok(extended.querySelector('.itinerary-day-scheduled-pill-header'));
   } finally {
      OpenTimelineView.createPillLabelNode = originalCreate;
      ScheduledPillPresenter.isExtendedScheduledPill = originalExtended;
   }
});
