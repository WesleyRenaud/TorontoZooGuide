from __future__ import annotations

from collections.abc import Callable

import pytest

from api.giftshops.domain.gift_shop_builder import GiftShopBuilder
from api.restaurants.domain.restaurant_builder import RestaurantBuilder
from api.types import Types


LikelihoodCalculator = Callable[ [ Types.SeasonalMultiplier ], int ]


@pytest.mark.parametrize(
   'calculate_likelihood',
   [
      RestaurantBuilder.calculate_likelihood,
      GiftShopBuilder.calculate_likelihood,
   ]
)
def test_simple_likelihood_calculators_clamp_and_round(
      calculate_likelihood: LikelihoodCalculator ) -> None:
   assert calculate_likelihood( None ) == 100
   assert calculate_likelihood( -0.5 ) == 0
   assert calculate_likelihood( 0.444 ) == 44
   assert calculate_likelihood( 1.5 ) == 100
