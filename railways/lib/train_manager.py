from railways.models import Train, Bookings

# We manage tickets availability of each train in
# a segment tree. This reduces load on database for
# queries, and also since query complexity is O(log n).
#
# These segment trees are periodically synchronized.
# Each train has a single segment tree assoicated with
# it.
class TrainManager:
    # We make TreeManager singleton to maintain state of data.
    tree_manager = None

    def __new__(cls):
        if cls.tree_manager is None:
            cls.tree_manager = super(TrainManager, cls).__new__(cls)
            cls.tree_manager.trains = {}
            cls.tree_manager.sizes = {}
        return cls.tree_manager

    # We first try to populate each segment tree of train
    # with the total capacity. Then we iteratae through
    # each row of bookings to update it to reflect the
    # final tree upon which queries are made.
    def reload_trains_data(self):
        trains = Train.objects.all()
        trains_data = [train.to_dict() for train in trains]

        for train in trains_data:
            train_id = train.get("id")
            source = train.get("source")
            destination = train.get("destination")
            seats = train.get("seats")

            self.trains[train_id] = SegmentTree(seats)
            self.seats[train_id] = seats
            self.trains[train_id].build(seats, train_id, source, destination)
        
        self.sync_with_db()

    def get_available_seats(self, train_id, start, end):
        return self.trains[train_id].query(start, end)

    # decrements tickets as per Bookings table.
    def sync_with_db(self):
        bookings = Bookings.objects.filter(status=Bookings.CONFIRMED)
        bookings_data = [booking.to_dict() for booking in bookings]

        for booking in bookings_data:
            train_id = booking.get("train")
            source = booking.get("source")
            destination = booking.get("destination")
            seats = booking.get("seats")

            self.trains[train_id].range_update(source, destination, seats)


class SegmentTree:
    def __init__(self, seats):
        self.n = seats
        self.tree = [0] * (4 * self.n)
        self.build(seats, 0, 0, self.n - 1)

    def build(self, seats, node, start, end):
        if start == end:
            self.tree[node] = seats
        else:
            mid = (start + end) // 2
            left_child, right_child = 2 * node + 1, 2 * node + 2
            self.build(seats, left_child, start, mid)
            self.build(seats, right_child, mid + 1, end)
            self.tree[node] = min(self.tree[left_child], self.tree[right_child])

    def range_update(self, l, r, decrement, node=0, start=0, end=None):
        if end is None:
            end = self.n - 1
        if r < start or l > end:
            return
        if start == end:
            self.tree[node] -= decrement
            return

        mid = (start + end) // 2
        left_child, right_child = 2 * node + 1, 2 * node + 2
        self.range_update(l, r, decrement, left_child, start, mid)
        self.range_update(l, r, decrement, right_child, mid + 1, end)
        self.tree[node] = min(self.tree[left_child], self.tree[right_child])

    # Since number of seats available between two stations is
    # min of number of seats available between adjacent stations.
    def query(self, l, r, node=0, start=0, end=None):
        if end is None:
            end = self.n - 1
        if r < start or l > end:
            return float('inf')
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_child, right_child = 2 * node + 1, 2 * node + 2
        return min(self.query(l, r, left_child, start, mid),
                   self.query(l, r, right_child, mid + 1, end))
