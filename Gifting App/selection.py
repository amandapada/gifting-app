class GiftCurator:
    def __init__(self, gifts):
        self.gifts = gifts

    def curate_gift_box(self, interest, gender, budget):
        # Filter gifts by interest and gender
        filtered_gifts = [gift for gift in self.gifts if gift.interest == interest and gift.gender == gender]

        # Sort gifts by price in ascending order
        filtered_gifts.sort(key=lambda x: x.price)

        # Initialize the gift box
        gift_box = []

        # Iterate over the filtered gifts until the budget is exhausted
        for gift in filtered_gifts:
            if gift.price <= budget:
                gift_box.append(gift)
                budget -= gift.price
            else:
                break

        return gift_box

class Gift:
    def __init__(self, name, price, interest, gender):
        self.name = name
        self.price = price
        self.interest = interest
        self.gender = gender