Student Name: Pobitro Bhattacharya
ID: 12341580
Lab: Prolog
File: weather.pl

Explanation

These are the known true conditions.

Rules
    enjoy :- sunny, warm.
    strawberry_picking :- warm, pleasant.
    not_strawberry_picking :- raining.
    wet :- raining.


These rules describe logical relationships:

    You will enjoy if it is sunny and warm.

    You will do strawberry picking if it is warm and pleasant.

    You will not do strawberry picking if it is raining.

    You will get wet if it is raining.

Queries and Results

Query: ?- not_strawberry_picking.
Result: true.
Reason: It is raining (fact)so it is true , and according to the rule, if it is raining, you are not doing strawberry picking.

Query: ?- enjoy.
Result: true.
Reason: It is both sunny and warm, so both of  conditions are for enjoyment is satisfied.

Query: ?- wet.
Result: true.
Reason: Since it is raining, the rule wet :- raining. is satisfied.



Conclusion

All queries evaluate to true, as the provided facts meet the logical requirements specified in the rules.
Hence, each query is successfully satisfied based on the given conditions.
