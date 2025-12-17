% ----------------------------
% weather.pl
% ----------------------------

% Facts
warm.
raining.
sunny.
pleasant.
% pleasant should not be there as no statement mentions so

% Rules
enjoy :- sunny, warm.
strawberry_picking :- warm, pleasant.
not_strawberry_picking :- raining.
wet :- raining.

% Resolution: remove implications
remove_implications(implies(and(sunny,warm),enjoy),or(not(sunny),or(not(warm),enjoy))).
remove_implications(implies(and(warm,pleasant),strawberry_picking),or(not(warm),or(not(pleasant),strawberry_picking))).
remove_implications(implies(raining,not_strawberry_picking),or(not(raining),not_strawberry_picking)).
remove_implications(implies(raining,wet),or(not(raining),wet)).
