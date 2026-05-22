class GiftShopScheduleOverride:
   def __init__(
         self,
         gift_shop,
         start_date,
         end_date,
         is_closed,
         message ):
      self.gift_shop = gift_shop
      self.start_date = start_date
      self.end_date = end_date
      self.is_closed = is_closed
      self.message = message
