from nameko.rpc import rpc


class OddSquarerService:
    name = "odd_squarer_service"

    @rpc
    def square_odd_numbers(self, numbers):
        # Square the odd numbers in the list
        return [x * x if x % 2 == 1 else x for x in numbers]
