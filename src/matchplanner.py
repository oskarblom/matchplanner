import md5
import collections

class Position(object):
    Forward = "Forward"
    RightMidfield = "RightMidfield"
    Defender = "Defender"
    LeftMidfield = "LeftMidfield"
    GoalKeeper = "GoalKeeper"
    Bench = "Bench"
    
    @staticmethod
    def from_index(index):
        assert index >= 0 and index <= 4
        return {
            0:  Position.Forward,
            1:  Position.RightMidfield,
            2:  Position.Defender,
            3:  Position.LeftMidfield,
        }[index]

class PlayerGroup(object):
    def __init__(self, name, player_names, slots):
        self.name = name
        self.player_names = player_names
        self.slots = slots

    def generate_positions(self):
        # TODO: Seed to make deterministic
        # seed = md5.new("".join(sorted(self.player_names))
        assert len(self.player_names) >= 5
        assert len(self.player_names) <= 9
        return {
            Position.Forward: self.player_names[0],
            Position.RightMidfield: self.player_names[1],
            Position.Defender: self.player_names[2],
            Position.LeftMidfield: self.player_names[3],
        }, self.player_names[4:]

class MatchSlot(object):
    def __init__(self, opponent, time):
        self.opponent = opponent
        self.time = time

class Period(object):
    def __init__(self, num, positions, bench):
        self.num = num
        self.positions = positions
        self.bench = bench
    
    @staticmethod
    def rotated_positions(positions):
        return {
            Position.Forward: positions[Position.LeftMidfield],
            Position.RightMidfield: positions[Position.Forward],
            Position.Defender: positions[Position.RightMidfield],
            Position.LeftMidfield: positions[Position.Defender]
        }

    @classmethod
    def from_previous(cls, prev_period):
        new_postions = Period.rotated_positions(prev_period.positions)
        new_bench = []
        for i, benched_player in enumerate(prev_period.bench):
            swap_position = Position.from_index(i)
            new_bench.append(prev_period.positions[swap_position])
            new_postions[swap_position] = benched_player

        return cls(prev_period.num + 1, new_postions, new_bench)


class Match(object):
    def __init__(self, periods, slot, goalkeeper):
        self.periods = periods
        self.slot = slot
        self.goalkeeper = goalkeeper

def main(player_groups):
    group_match_map = collections.defaultdict(list)
    for group in player_groups:
        for slot in group.slots:
            periods = []
            positions, bench = group.generate_positions()
            period = Period(1, positions, bench)
            periods.append(period)
            for _ in range(0, 2):
                period = Period.from_previous(period)
                periods.append(period)
            match = Match(periods, slot, "foo")
            group_match_map[group.name].append(match)

    return group_match_map

if __name__ == "__main__":
    red_slots = [
        MatchSlot("VSK", "08:00"),
        MatchSlot("VP", "09:00"),
        MatchSlot("UIF", "10:00")
    ]
    red_group = PlayerGroup(
        "red", 
        [
        "Tilda",
        "Elsa",
        "Alma",
        "Sally",
        "Sanna",
        "Ebba",
        "Mira"
        ], 
        red_slots)

    player_groups = [
        red_group
    ]

    matches = main(player_groups)
    print matches["red"][0].periods[0].positions
    print matches["red"][0].periods[1].positions
    print matches["red"][0].periods[2].positions
