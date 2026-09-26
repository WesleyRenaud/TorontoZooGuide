import assert from 'node:assert/strict';
import { test } from 'node:test';

import { makeScheduledItem } from '../../../helpers/scheduledPillTestSetup.mjs';
import { ScheduledPillChecker } from '../../../../../scripts/itinerary/panel/components/scheduledPillChecker.js';
import { ScheduledPillLayoutHelper } from '../../../../../scripts/itinerary/panel/components/scheduledPillLayoutHelper.js';
import { Position } from '../../../../../scripts/shared/enums/position.js';
import { ScheduleItemKind } from '../../../../../scripts/shared/enums/scheduleItemKind.js';
import { TimelineLayoutConstants } from '../../../../../scripts/shared/timelineLayoutConstants.js';
import { ZooClockTimeHelper } from '../../../../../scripts/shared/zooClockTimeHelper.js';
import { Strings } from '../../../../../scripts/strings.js';

function _minutes(clockTime) {
   return ZooClockTimeHelper.parseMinutes(clockTime);
}

function _attractionItem(label, startMinutes, maximumDuration = 2, anchorSlotMinutes = _minutes('9:30')) {
   return {
      ...makeScheduledItem(label, startMinutes, maximumDuration, anchorSlotMinutes),
      scheduleItemKind: ScheduleItemKind.ATTRACTION.itemType,
      item: { name: label },
   };
}

function _nonModuleItem(label, startMinutes, maximumDuration = 2) {
   return {
      ...makeScheduledItem(label, startMinutes, maximumDuration),
      scheduleItemKind: 'entrance',
   };
}


test('Test_GetScheduledPillMinDisplayMinutes_TestThreshold_ExpectClusterMinutes', () => {
   const minutes = ScheduledPillChecker.getScheduledPillMinDisplayMinutes();

   assert.equal(minutes, TimelineLayoutConstants.TIMELINE_SCHEDULED_PILL_MIN_CLUSTER_MINUTES);
});


test('Test_ClusterShortScheduledItemsForDisplay_TestShortVisits_ExpectGrouped', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const capybara = 'Capybara';
   const panda = 'Red Panda';

   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem(capybara, startMinutes, 2, startMinutes),
      makeScheduledItem('Cheetah', startMinutes + 2, 2, startMinutes),
      makeScheduledItem(panda, startMinutes + 12, 2, startMinutes),
   ], minDisplayMinutes);

   assert.equal(clusteredItems.length, 2);
   assert.equal(
      clusteredItems.at(Position.FIRST).label,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(capybara, 1)
   );
   assert.equal(clusteredItems.at(Position.SECOND).label, panda);
});


test('Test_ClusterShortScheduledItemsForDisplay_TestUnderMin_ExpectPullsNext', () => {
   const startMinutes = _minutes('9:30');
   const cheetah = 'Cheetah';
   const rhino = 'Greater One-Horned Rhinoceros';

   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem('Capybara', startMinutes, 2, startMinutes),
      makeScheduledItem(cheetah, startMinutes + 2, 8, startMinutes),
      makeScheduledItem(rhino, startMinutes + 10, 8, startMinutes),
   ]);

   assert.equal(clusteredItems.length, 2);
   assert.equal(
      clusteredItems.at(Position.FIRST).label,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(cheetah, 1)
   );
   assert.equal(clusteredItems.at(Position.SECOND).label, rhino);
});


test('Test_ClusterShortScheduledItemsForDisplay_TestReadableVisits_ExpectSeparate', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = TimelineLayoutConstants.TIMELINE_SLOT_MINUTES;
   const capybara = 'Capybara';
   const cheetah = 'Cheetah';
   const panda = 'Red Panda';

   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem(capybara, startMinutes, durationMinutes, startMinutes),
      makeScheduledItem(cheetah, startMinutes + 4, durationMinutes, startMinutes),
      makeScheduledItem(panda, startMinutes + 5, durationMinutes, startMinutes),
   ]);

   assert.equal(clusteredItems.length, 3);
   assert.equal(clusteredItems.at(Position.FIRST).label, capybara);
   assert.equal(clusteredItems.at(Position.SECOND).label, cheetah);
   assert.equal(clusteredItems.at(Position.THIRD).label, panda);
});


test('Test_ClusterShortScheduledItemsForDisplay_TestMaxDuration_ExpectOrdered', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const giraffe = 'Masai Giraffe';
   const cichlid = 'Lake Malawi Cichlid';

   const clusteredItems = ScheduledPillLayoutHelper.clusterShortScheduledItemsForDisplay([
      makeScheduledItem(cichlid, startMinutes, 2, startMinutes),
      makeScheduledItem(giraffe, startMinutes + 2, minDisplayMinutes, startMinutes),
   ], minDisplayMinutes);

   assert.equal(clusteredItems.length, 1);
   assert.equal(
      clusteredItems.at(Position.FIRST).label,
      Strings.itinerary.dayPlanner.scheduledPillGroupLabel(giraffe, 1)
   );
   assert.deepEqual(
      clusteredItems.at(Position.FIRST).clusterItems.map((item) => item.label),
      [giraffe, cichlid]
   );
});


test('Test_GetScheduledItemDurationMinutes_TestMissingEnd_ExpectMaximumDuration', () => {
   const maximumDuration = 12;
   const scheduledItem = {
      startMinutes: _minutes('9:30'),
      maximumDuration,
   };

   const duration = ScheduledPillLayoutHelper.getScheduledItemDurationMinutes(scheduledItem);

   assert.equal(duration, maximumDuration);
});


test('Test_GetClusterWallSpanMinutes_TestEmpty_ExpectZero', () => {
   const span = ScheduledPillLayoutHelper.getClusterWallSpanMinutes([]);

   assert.equal(span, 0);
});


test('Test_IsCarouselMergeableItem_TestAnimal_ExpectTrue', () => {
   const item = makeScheduledItem('African Lion', _minutes('9:30'), 2);

   const mergeable = ScheduledPillLayoutHelper.isCarouselMergeableItem(item);

   assert.equal(mergeable, true);
});


test('Test_CanMergeCarouselLayoutUnits_TestAnimals_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const left = makeScheduledItem('African Lion', startMinutes, 2);
   const right = makeScheduledItem('Amur Tiger', startMinutes + 2, 2);

   const canMerge = ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(left, right);

   assert.equal(canMerge, true);
});


test('Test_CanMergeCarouselLayoutUnits_TestNonModule_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const left = makeScheduledItem('African Lion', startMinutes, 2);
   const right = _nonModuleItem('Gate', startMinutes + 4);

   const canMerge = ScheduledPillLayoutHelper.canMergeCarouselLayoutUnits(left, right);

   assert.equal(canMerge, false);
});


test('Test_MergeLayoutUnits_TestTwoAnimals_ExpectCluster', () => {
   const startMinutes = _minutes('9:30');
   const left = makeScheduledItem('African Lion', startMinutes, 2);
   const right = makeScheduledItem('Amur Tiger', startMinutes + 2, 2);

   const merged = ScheduledPillLayoutHelper.mergeLayoutUnits(left, right);

   assert.ok(merged.clusterItems);
   assert.equal(merged.clusterItems.length, 2);
});


test('Test_MergeLayoutUnits_TestEmptyRight_ExpectLeftLabel', () => {
   const startMinutes = _minutes('9:30');
   const lion = 'African Lion';
   const left = makeScheduledItem(lion, startMinutes, 2);

   const merged = ScheduledPillLayoutHelper.mergeLayoutUnits(left, { clusterItems: [] });

   assert.equal(merged.label, lion);
});


test('Test_GetLayoutUnitStartMinutes_TestItem_ExpectStart', () => {
   const startMinutes = _minutes('9:30');
   const item = makeScheduledItem('African Lion', startMinutes, 2);

   const start = ScheduledPillLayoutHelper.getLayoutUnitStartMinutes(item);

   assert.equal(start, startMinutes);
});


test('Test_GetLayoutUnitEndMinutes_TestItem_ExpectEnd', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = 2;
   const item = makeScheduledItem('African Lion', startMinutes, durationMinutes);

   const end = ScheduledPillLayoutHelper.getLayoutUnitEndMinutes(item);

   assert.equal(end, startMinutes + durationMinutes);
});


test('Test_GetLayoutUnitWallSpanMinutes_TestItem_ExpectDuration', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = 2;
   const item = makeScheduledItem('African Lion', startMinutes, durationMinutes);

   const span = ScheduledPillLayoutHelper.getLayoutUnitWallSpanMinutes(item);

   assert.equal(span, durationMinutes);
});


test('Test_AreConsecutiveLayoutUnits_TestTouching_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const durationMinutes = 2;
   const first = makeScheduledItem('African Lion', startMinutes, durationMinutes);
   const second = makeScheduledItem('Amur Tiger', startMinutes + durationMinutes, durationMinutes);

   const consecutive = ScheduledPillLayoutHelper.areConsecutiveLayoutUnits(first, second);

   assert.equal(consecutive, true);
});


test('Test_IsUnderMinDisplayLayoutUnit_TestShort_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const item = makeScheduledItem('African Lion', startMinutes, 2);

   const underMin = ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(item, minDisplayMinutes);

   assert.equal(underMin, true);
});


test('Test_IsUnderMinDisplayLayoutUnit_TestLong_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const item = makeScheduledItem('African Lion', startMinutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);

   const underMin = ScheduledPillLayoutHelper.isUnderMinDisplayLayoutUnit(item, minDisplayMinutes);

   assert.equal(underMin, false);
});


test('Test_UnderMinLayoutUnitsNeedMerge_TestNear_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const left = makeScheduledItem('African Lion', startMinutes, 2);
   const nearRight = makeScheduledItem('Amur Tiger', startMinutes + 4, 2);

   const needsMerge = ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
      left,
      nearRight,
      minDisplayMinutes
   );

   assert.equal(needsMerge, true);
});


test('Test_UnderMinLayoutUnitsNeedMerge_TestFar_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const left = makeScheduledItem('African Lion', startMinutes, 2);
   const farRight = makeScheduledItem('Grizzly Bear', startMinutes + 20, 2);

   const needsMerge = ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
      left,
      farRight,
      minDisplayMinutes
   );

   assert.equal(needsMerge, false);
});


test('Test_UnderMinLayoutUnitsNeedMerge_TestNonFinite_ExpectFalse', () => {
   const minDisplayMinutes = 8;
   const nearRight = makeScheduledItem('Amur Tiger', _minutes('9:30') + 4, 2);

   const needsMerge = ScheduledPillLayoutHelper.underMinLayoutUnitsNeedMerge(
      { startMinutes: Number.NaN },
      nearRight,
      minDisplayMinutes
   );

   assert.equal(needsMerge, false);
});


test('Test_MergeConsecutiveUnderMinDisplayLayoutUnits_TestShortChain_ExpectMerged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const units = [
      makeScheduledItem('African Lion', startMinutes, 2),
      makeScheduledItem('Amur Tiger', startMinutes + 2, 2),
      makeScheduledItem('Grizzly Bear', startMinutes + 10, 2),
   ];

   const consecutive = ScheduledPillLayoutHelper.mergeConsecutiveUnderMinDisplayLayoutUnits(
      units,
      minDisplayMinutes
   );

   assert.equal(consecutive.length, 2);
});


test('Test_MergeUnderMinDisplayLayoutUnits_TestNearby_ExpectChanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;

   const underMin = ScheduledPillLayoutHelper.mergeUnderMinDisplayLayoutUnits([
      makeScheduledItem('African Lion', startMinutes, 2),
      makeScheduledItem('Amur Tiger', startMinutes + 4, 2),
      makeScheduledItem('Grizzly Bear', startMinutes + 20, 2),
   ], minDisplayMinutes);

   assert.equal(underMin.changed, true);
   assert.ok(underMin.layoutUnits.length < 3);
});


test('Test_MergeUnderMinDisplayLayoutUnits_TestAbsorbPrevious_ExpectChanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;

   const absorbPrevious = ScheduledPillLayoutHelper.mergeUnderMinDisplayLayoutUnits([
      makeScheduledItem('African Lion', startMinutes, 10),
      makeScheduledItem('Amur Tiger', startMinutes + 8, 2),
   ], minDisplayMinutes);

   assert.equal(absorbPrevious.changed, true);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestOrphan_ExpectAbsorbed', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const head = [
      makeScheduledItem('Amur Tiger', startMinutes, 2),
      makeScheduledItem('African Lion', startMinutes + 2, 10),
   ];

   const absorbedHead = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(head, minDisplayMinutes);

   assert.equal(absorbedHead.length, 1);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestAlone_ExpectUnchanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const alone = [makeScheduledItem('African Lion', startMinutes, 2)];

   const absorbed = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(alone, minDisplayMinutes);

   assert.deepEqual(absorbed, alone);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestNonConsecutive_ExpectUnchanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const units = [
      makeScheduledItem('Amur Tiger', startMinutes, 2),
      makeScheduledItem('African Lion', startMinutes + 10, 10),
   ];

   const absorbed = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(units, minDisplayMinutes);

   assert.deepEqual(absorbed, units);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestNonMergeable_ExpectUnchanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const units = [
      makeScheduledItem('Amur Tiger', startMinutes, 2),
      _nonModuleItem('Gate', startMinutes + 2, 10),
   ];

   const absorbed = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(units, minDisplayMinutes);

   assert.deepEqual(absorbed, units);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestLongHead_ExpectUnchanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const units = [
      makeScheduledItem('African Lion', startMinutes, 10),
      makeScheduledItem('Amur Tiger', startMinutes + 10, 10),
   ];

   const absorbed = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(units, minDisplayMinutes);

   assert.deepEqual(absorbed, units);
});


test('Test_IsTailOrphanLayoutUnit_TestOrphan_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const tailOrphan = {
      ...makeScheduledItem('Amur Tiger', startMinutes + 25, 2, startMinutes),
      slotEndMinutes: startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };

   const isOrphan = ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(tailOrphan, minDisplayMinutes);

   assert.equal(isOrphan, true);
});


test('Test_IsTailOrphanLayoutUnit_TestLong_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const item = makeScheduledItem('African Lion', startMinutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES);

   const isOrphan = ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(item, minDisplayMinutes);

   assert.equal(isOrphan, false);
});


test('Test_IsTailOrphanLayoutUnit_TestMissingSlot_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const item = {
      ...makeScheduledItem('African Lion', startMinutes, 2),
      slotEndMinutes: undefined,
      anchorSlotMinutes: undefined,
   };

   const isOrphan = ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(item, minDisplayMinutes);

   assert.equal(isOrphan, false);
});


test('Test_AbsorbTailOrphanLayoutUnits_TestOrphan_ExpectAbsorbed', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const tailOrphan = {
      ...makeScheduledItem('Amur Tiger', startMinutes + 25, 2, startMinutes),
      slotEndMinutes: startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };

   const absorbedTail = ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
      makeScheduledItem('African Lion', startMinutes, 10),
      tailOrphan,
   ], minDisplayMinutes);

   assert.equal(absorbedTail.length, 1);
});


test('Test_AbsorbTailOrphanLayoutUnits_TestNonModulePrevious_ExpectKept', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const gate = 'Gate';
   const tail = 'Amur Tiger';
   const tailOrphan = {
      ...makeScheduledItem(tail, startMinutes + 25, 2, startMinutes),
      slotEndMinutes: startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };

   const absorbed = ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
      _nonModuleItem(gate, startMinutes, 10),
      tailOrphan,
   ], minDisplayMinutes);

   assert.deepEqual(absorbed.map((item) => item.label), [gate, tail]);
});


test('Test_GetEarliestScheduledItemByStartTime_TestEmpty_ExpectNull', () => {
   const earliest = ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime([]);

   assert.equal(earliest, null);
});


test('Test_IsAnimalScheduledItem_TestAnimal_ExpectTrue', () => {
   const item = makeScheduledItem('African Lion', _minutes('9:30'));

   const isAnimal = ScheduledPillLayoutHelper.isAnimalScheduledItem(item);

   assert.equal(isAnimal, true);
});


test('Test_AreAdjacentOrOverlappingScheduledItems_TestOverlap_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const left = makeScheduledItem('African Lion', startMinutes, 10);
   const right = makeScheduledItem('Amur Tiger', startMinutes + 5, 10);

   const overlaps = ScheduledPillLayoutHelper.areAdjacentOrOverlappingScheduledItems(left, right);

   assert.equal(overlaps, true);
});


test('Test_AreAdjacentOrOverlappingScheduledItems_TestNonFinite_ExpectFalse', () => {
   const right = makeScheduledItem('Amur Tiger', _minutes('9:30') + 5);

   const overlaps = ScheduledPillLayoutHelper.areAdjacentOrOverlappingScheduledItems(
      { startMinutes: Number.NaN },
      right
   );

   assert.equal(overlaps, false);
});


test('Test_CanGroupScheduledItemsByViewingWalkNode_TestSharedNode_ExpectTrue', () => {
   const startMinutes = _minutes('9:30');
   const nodeId = 'node-lion';
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, nodeId);
   const sharedNodeB = makeScheduledItem('Amur Tiger', startMinutes + 5, 10, startMinutes, nodeId);

   const canGroup = ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
      sharedNodeA,
      sharedNodeB
   );

   assert.equal(canGroup, true);
});


test('Test_CanGroupScheduledItemsByViewingWalkNode_TestAttraction_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const nodeId = 'node-lion';
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, nodeId);
   const otherKind = _attractionItem('Conservation Carousel', startMinutes + 10, 10);

   const canGroup = ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
      sharedNodeA,
      otherKind
   );

   assert.equal(canGroup, false);
});


test('Test_CanGroupScheduledItemsByViewingWalkNode_TestNonAnimalPrevious_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const attraction = _attractionItem('Conservation Carousel', startMinutes, 10);
   const animal = makeScheduledItem('African Lion', startMinutes + 5, 10, startMinutes, 'node-lion');

   const canGroup = ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
      attraction,
      animal
   );

   assert.equal(canGroup, false);
});


test('Test_CanGroupScheduledItemsByViewingWalkNode_TestEmptyNode_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, 'node-lion');
   const emptyNode = makeScheduledItem('Grizzly Bear', startMinutes + 5, 10, startMinutes, '');

   const canGroup = ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
      sharedNodeA,
      emptyNode
   );

   assert.equal(canGroup, false);
});


test('Test_CanGroupScheduledItemsByViewingWalkNode_TestDifferentNode_ExpectFalse', () => {
   const startMinutes = _minutes('9:30');
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, 'node-lion');
   const otherNode = makeScheduledItem('Grizzly Bear', startMinutes + 5, 10, startMinutes, 'node-bear');

   const canGroup = ScheduledPillLayoutHelper.canGroupScheduledItemsByViewingWalkNode(
      sharedNodeA,
      otherNode
   );

   assert.equal(canGroup, false);
});


test('Test_FlushViewingWalkNodeClusterItems_TestItems_ExpectClusters', () => {
   const startMinutes = _minutes('9:30');
   const nodeId = 'node-lion';
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, nodeId);
   const sharedNodeB = makeScheduledItem('Amur Tiger', startMinutes + 5, 10, startMinutes, nodeId);
   const clusters = [];

   ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems([sharedNodeA], clusters);
   ScheduledPillLayoutHelper.flushViewingWalkNodeClusterItems([sharedNodeA, sharedNodeB], clusters);

   assert.equal(clusters.length, 2);
   assert.ok(clusters.at(Position.SECOND).clusterItems);
});


test('Test_CompareScheduledItemsForLayout_TestLabels_ExpectOrder', () => {
   const startMinutes = _minutes('9:30');
   const laterLabel = makeScheduledItem('Zebra', startMinutes);
   const earlierLabel = makeScheduledItem('African Lion', startMinutes);

   const comparison = ScheduledPillLayoutHelper.compareScheduledItemsForLayout(
      laterLabel,
      earlierLabel
   );

   assert.ok(comparison > 0);
});


test('Test_ClusterScheduledAnimalItemsByViewingWalkNode_TestSharedNodes_ExpectClusters', () => {
   const startMinutes = _minutes('9:30');
   const laterStart = _minutes('10:00');
   const sharedNodeA = makeScheduledItem('African Lion', startMinutes, 10, startMinutes, 'node-lion');
   const sharedNodeB = makeScheduledItem('Amur Tiger', startMinutes + 5, 10, startMinutes, 'node-lion');

   const walkClusters = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode([
      sharedNodeB,
      sharedNodeA,
      makeScheduledItem('Snow Leopard', laterStart, 10, laterStart, 'node-leopard'),
      makeScheduledItem('Amur Leopard', laterStart + 5, 10, laterStart, 'node-leopard'),
   ]);

   assert.ok(walkClusters.some((item) => item.clusterItems?.length === 2));
});


test('Test_ClusterScheduledAnimalItemsByViewingWalkNode_TestRejoin_ExpectMerged', () => {
   const startMinutes = _minutes('9:30');
   const nodeId = 'node-rejoin';
   const longFirst = makeScheduledItem('African Lion', startMinutes, TimelineLayoutConstants.TIMELINE_SLOT_MINUTES, startMinutes, nodeId);
   const shortSecond = makeScheduledItem('Amur Tiger', startMinutes + 10, 5, startMinutes, nodeId);
   const overlapsCluster = makeScheduledItem('Snow Leopard', startMinutes + 20, 10, startMinutes, nodeId);

   const clusters = ScheduledPillLayoutHelper.clusterScheduledAnimalItemsByViewingWalkNode([
      longFirst,
      shortSecond,
      overlapsCluster,
   ]);

   assert.equal(clusters.length, 1);
   assert.equal(clusters.at(Position.FIRST).clusterItems?.length, 3);
});


test('Test_NormalizeLayoutUnitsForDisplay_TestUnderMinChain_ExpectNormalized', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;

   const normalized = ScheduledPillLayoutHelper.normalizeLayoutUnitsForDisplay([
      makeScheduledItem('African Lion', startMinutes, 2),
      makeScheduledItem('Amur Tiger', startMinutes + 2, 2),
      makeScheduledItem('Grizzly Bear', startMinutes + 4, 2),
   ], minDisplayMinutes);

   assert.equal(normalized.length, 1);
});


test('Test_ClusterScheduledItemsByDuration_TestAlias_ExpectDelegates', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const items = [
      makeScheduledItem('Capybara', startMinutes, 2, startMinutes),
      makeScheduledItem('Cheetah', startMinutes + 2, 2, startMinutes),
   ];

   const byDuration = ScheduledPillLayoutHelper.clusterScheduledItemsByDuration(items, minDisplayMinutes);
   const byAlias = ScheduledPillLayoutHelper.clusterScheduledItemsByStartTimeProximity(items, minDisplayMinutes);

   assert.equal(byDuration.length, 1);
   assert.deepEqual(byAlias.map((item) => item.label), byDuration.map((item) => item.label));
});


test('Test_GetScheduledItemDurationMinutes_TestNaNStart_ExpectMaximumDuration', () => {
   const maximumDuration = 12;

   const duration = ScheduledPillLayoutHelper.getScheduledItemDurationMinutes({
      startMinutes: Number.NaN,
      maximumDuration,
   });

   assert.equal(duration, maximumDuration);
});


test('Test_GetClusterWallSpanMinutes_TestItems_ExpectSpan', () => {
   const startMinutes = _minutes('9:30');
   const firstDuration = 10;
   const secondStartOffset = 5;
   const secondDuration = 10;

   const span = ScheduledPillLayoutHelper.getClusterWallSpanMinutes([
      makeScheduledItem('African Lion', startMinutes, firstDuration),
      makeScheduledItem('Amur Tiger', startMinutes + secondStartOffset, secondDuration),
   ]);

   assert.equal(span, secondStartOffset + secondDuration);
});


test('Test_MergeLayoutUnits_TestSingleItem_ExpectItem', () => {
   const startMinutes = _minutes('9:30');
   const item = _attractionItem('Conservation Carousel', startMinutes, 10);

   const merged = ScheduledPillLayoutHelper.mergeLayoutUnits(item, {
      clusterItems: [],
      startMinutes: startMinutes + 10,
      maximumDuration: 0,
   });

   assert.ok(merged);
});


test('Test_AbsorbHeadOrphanLayoutUnits_TestNonModuleHead_ExpectUnchanged', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const units = [
      _nonModuleItem('Gate', startMinutes, 2),
      _attractionItem('Conservation Carousel', startMinutes + 2, 10),
   ];

   const absorbed = ScheduledPillLayoutHelper.absorbHeadOrphanLayoutUnits(units, minDisplayMinutes);

   assert.deepEqual(absorbed, units);
});


test('Test_IsTailOrphanAndAbsorb_TestSlotEnd_ExpectMergedOrKept', () => {
   const startMinutes = _minutes('9:30');
   const minDisplayMinutes = 8;
   const orphan = {
      ...makeScheduledItem('Amur Tiger', startMinutes + 28, 2, startMinutes),
      slotEndMinutes: startMinutes + TimelineLayoutConstants.TIMELINE_SLOT_MINUTES,
   };

   const isOrphan = ScheduledPillLayoutHelper.isTailOrphanLayoutUnit(orphan, minDisplayMinutes);
   const absorbed = ScheduledPillLayoutHelper.absorbTailOrphanLayoutUnits([
      _attractionItem('Conservation Carousel', startMinutes, 20),
      orphan,
   ], minDisplayMinutes);

   assert.equal(isOrphan, true);
   assert.ok(Array.isArray(absorbed));
});


test('Test_GetEarliestScheduledItemByStartTime_TestItems_ExpectEarliest', () => {
   const early = 'African Lion';
   const lateStart = _minutes('10:00');
   const earlyStart = _minutes('9:30');

   const earliest = ScheduledPillLayoutHelper.getEarliestScheduledItemByStartTime([
      makeScheduledItem('Amur Tiger', lateStart, 10),
      makeScheduledItem(early, earlyStart, 10),
   ]);

   assert.equal(earliest.label, early);
});
