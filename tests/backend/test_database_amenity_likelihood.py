from __future__ import annotations

from collections.abc import Callable

import pytest

from api.attractions.logic.attraction import calculate_attraction_likelihood
from api.giftshops.domain.gift_shop import calculate_gift_shop_likelihood
from api.restaurants.domain.restaurant import calculate_restaurant_likelihood
from api.types import SeasonalMultiplier


LikelihoodCalculator = Callable[ [ SeasonalMultiplier ], int ]


@pytest.mark.parametrize(
   'calculate_likelihood',
   [
      calculate_restaurant_likelihood,
      calculate_gift_shop_likelihood,
      calculate_attraction_likelihood
   ]
)
def test_simple_likelihood_calculators_clamp_and_round(
      calculate_likelihood: LikelihoodCalculator ) -> None:
   assert calculate_likelihood( None ) == 100
   assert calculate_likelihood( -0.5 ) == 0
   assert calculate_likelihood( 0.444 ) == 44
   assert calculate_likelihood( 1.5 ) == 100
