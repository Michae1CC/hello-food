class HandlingEvent:

    def __init__(
        self,
        id_: int,
        delivery_id: int,
        to_address_id: int,
        from_address_id: int,
        completion_time: int,
    ) -> None:
        super().__init__()
        self.id = id_
        self.delivery_id = delivery_id
        self.to_address_id = to_address_id
        self.from_address_id = from_address_id
        self.completion_time = completion_time
